from fastapi import FastAPI, Depends, UploadFile, File, Form, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from src.core.config import settings
from src.agents import ClassifierAgent, ExplainerAgent, FormGuideAgent, RiskScannerAgent, ExpungementAgent
from src.memory.db import DatabaseManager
from src.payments.stripe_client import StripeClient
from src.payments import check_access
from src.ingestion import ingest_document
from src.core.escalation import EscalationRouter
from src.platforms.florida_courts import PDFAGenerator, CountyRouter, ManualFilingHelper
from src.platforms.notifications import NotificationService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = ClassifierAgent()
explainer = ExplainerAgent()
form_guide = FormGuideAgent()
risk_scanner = RiskScannerAgent()
expungement = ExpungementAgent()
db = DatabaseManager()
stripe_client = StripeClient()
escalator = EscalationRouter()
notifications = NotificationService()

async def verify_api_key(x_api_key: str = Header(None)):
    if settings.API_KEY and x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0", "product": "LegalClear"}

@app.post("/user", dependencies=[Depends(verify_api_key)])
async def create_user(email: str = Form(...), preferred_language: str = Form('en')):
    user = db.get_or_create_user(email, preferred_language)
    cust_id = stripe_client.create_or_get_customer(email)
    # in real usage, update db with cust_id
    return {"user_id": user.get('id'), "email": email, "subscription_status": user.get("subscription_status"), "free_doc_used": user.get("free_doc_used"), "preferred_language": preferred_language}

@app.get("/user/{user_id}", dependencies=[Depends(verify_api_key)])
async def get_user(user_id: str):
    return db.get_user(user_id)

@app.post("/user/{user_id}/push-token", dependencies=[Depends(verify_api_key)])
async def save_push_token(user_id: str, expo_token: str = Form(...), platform: str = Form(...)):
    db.save_push_token(user_id, expo_token, platform)
    return {"saved": True}

@app.post("/subscribe/{user_id}", dependencies=[Depends(verify_api_key)])
async def subscribe(user_id: str, success_url: str = Form(...), cancel_url: str = Form(...)):
    user = db.get_user(user_id)
    res = stripe_client.create_subscription_checkout(user.get('email', ''), user_id, success_url, cancel_url)
    return res

@app.post("/upload", dependencies=[Depends(verify_api_key)])
async def upload_document(file: UploadFile = File(...), user_id: str = Form(...), user_language: str = Form('en')):
    content = await file.read()
    doc = await ingest_document(content, file.filename)
    classification = await classifier.classify(doc)
    escalation = escalator.route(classification, user_language)
    tier = classifier.get_price_tier(doc)
    
    user = db.get_user(user_id)
    # mock a session internally since logic expects one
    session = {"payment_status": "pending"}
    
    access = check_access(user, session)
    
    if access['allowed']:
        s_id = db.create_session(user_id, file.filename, doc['token_estimate'], tier['tier'], 0, access['payment_type'])
        d_id = db.create_document(s_id, doc['text'])
        db.save_results(d_id, classification, {}, {}, {}, {}, escalation, user_language)
        return {"session_id": s_id, "document_id": d_id, "classification": classification, "escalation": escalation, "price_tier": tier, "requires_payment": False, "client_secret": None, "pre_analysis_warning": escalation.get('pre_analysis_warning'), "language": user_language}
    else:
        s_id = db.create_session(user_id, file.filename, doc['token_estimate'], tier['tier'], tier['price_usd'], "payg")
        d_id = db.create_document(s_id, doc['text'])
        db.save_results(d_id, classification, {}, {}, {}, {}, escalation, user_language)
        intent = stripe_client.create_payment_intent(tier['price_usd'], s_id, user.get('email',''), {"document_id": d_id})
        return {"session_id": s_id, "document_id": d_id, "classification": classification, "escalation": escalation, "price_tier": tier, "requires_payment": True, "client_secret": intent.get('client_secret'), "pre_analysis_warning": escalation.get('pre_analysis_warning'), "language": user_language}

import asyncio

@app.post("/process/{document_id}", dependencies=[Depends(verify_api_key)])
async def process_document(document_id: str):
    doc = db.get_document(document_id)
    if not doc or not doc.get('id'):
        raise HTTPException(status_code=404, detail="Document not found")
        
    sess = db.get_session(doc.get('session_id'))
    text = doc.get('document_text', '')
    classification = doc.get('classification', {})
    escalation = doc.get('escalation', {})
    lang = doc.get('language', 'en')
    
    # Run Agents Concurrently
    tasks = [
        explainer.explain({"text": text}, classification, lang),
        risk_scanner.scan({"text": text}, classification, lang),
        form_guide.guide({"text": text}, classification, lang)
    ]
    results = await asyncio.gather(*tasks)
    explanation, risk_scan, form_guide_res = results
    
    db.save_results(
        document_id, 
        classification, 
        explanation, 
        form_guide_res, 
        risk_scan, 
        {}, 
        escalation, 
        lang
    )
    
    await notifications.notify_document_ready(sess.get('user_id', ''), "doc_completed")
    return {"status": "complete", "document_id": document_id}

@app.post("/chat/{document_id}", dependencies=[Depends(verify_api_key)])
async def chat(document_id: str, question: str = Form(...), user_language: str = Form('en')):
    history = db.get_history(document_id)
    doc_info = db.get_document(document_id)
    ans = await explainer.answer_question({}, {}, {}, question, history, user_language)
    db.save_message(document_id, 'user', question, user_language)
    db.save_message(document_id, 'assistant', ans['answer'], user_language)
    return ans

@app.post("/eligibility")
async def eligibility(jurisdiction: str = Form(...), offense_description: str = Form(...), years_since_offense: int = Form(...), lang: str = Form('en')):
    res = await expungement.check_eligibility(jurisdiction, offense_description, years_since_offense, lang)
    return res

@app.get("/document/{document_id}", dependencies=[Depends(verify_api_key)])
async def get_document(document_id: str):
    return db.get_document(document_id)

@app.get("/documents/{user_id}", dependencies=[Depends(verify_api_key)])
async def get_user_documents(user_id: str):
    return db.get_user_documents(user_id)

@app.post("/florida-filing/prepare", dependencies=[Depends(verify_api_key)])
async def prepare_fl_filing(document_id: str = Form(...), case_data: str = Form(...), county: str = Form(...), lang: str = Form('en')):
    import json as sys_json
    c_data = sys_json.loads(case_data)
    gen = PDFAGenerator()
    packet = gen.generate_packet(c_data, f"/tmp/{document_id}")
    router_info = CountyRouter().route(county)
    inst = ManualFilingHelper.get_instructions(county, lang)
    dl = ManualFilingHelper.get_deep_link_button(county)
    return {"packet_ready": True, "files": packet, "county_info": router_info, "instructions": inst, "deep_link_button": dl, "disclaimer": inst.get('disclaimer')}

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe_client.verify_webhook(payload, sig_header)
        # Handle events internally
        return {"received": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
