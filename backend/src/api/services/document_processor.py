from fastapi import HTTPException, BackgroundTasks
from src.payments import check_access

class DocumentProcessingService:
    def __init__(
        self,
        db,
        classifier,
        explainer,
        risk_scanner,
        form_guide,
        expungement,
        escalation_router,
        notifications,
        form_categories
    ):
        self.db = db
        self.classifier = classifier
        self.explainer = explainer
        self.risk_scanner = risk_scanner
        self.form_guide = form_guide
        self.expungement = expungement
        self.escalation_router = escalation_router
        self.notifications = notifications
        self.form_categories = form_categories

    async def process(self, session_id: str, background_tasks: BackgroundTasks, lang: str = "en"):
        session = self.db.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        user = self.db.get_user(session["user_id"])
        access = check_access(user, session)
        if not access["allowed"]:
            raise HTTPException(status_code=402, detail="Payment required")

        docs = self.db.client.table("documents").select("*").eq("session_id", session_id).execute()
        if not docs.data:
            raise HTTPException(status_code=404, detail="Document not found")

        doc_record = docs.data[0]
        document_id = doc_record["id"]
        document_text = doc_record["document_text"]

        doc = {"text": document_text}
        classification = await self.classifier.classify(doc)

        explanation = await self.explainer.explain(doc, classification, lang)
        risk_scan = await self.risk_scanner.scan(doc, classification, lang)

        form_results = {}
        if classification.get("document_category") in self.form_categories:
            form_results = await self.form_guide.guide(doc, classification, lang)

        exp_results = {}
        if classification.get("document_category") == "expungement_petition":
            exp_results = await self.expungement.guide(doc, classification, lang)

        escalation = self.escalation_router.route(classification, lang)

        self.db.save_results(
            document_id=document_id,
            classification=classification,
            explanation=explanation,
            form_guide=form_results,
            risk_scan=risk_scan,
            expungement_guide=exp_results,
            escalation=escalation,
            language=lang
        )

        if access["payment_type"] == "free":
            self.db.mark_free_doc_used(user["id"])

        self.db.log_usage(
            category=classification.get("document_category", "unknown"),
            jurisdiction=classification.get("jurisdiction_name", "unknown"),
            language=lang,
            price_tier=session.get("price_tier", "small"),
            processing_time=0.0
        )

        # Notify
        background_tasks.add_task(self.notifications.send_push, user["id"], "Analysis Complete", "Your document analysis is ready to view.")

        return {
            "document_id": document_id,
            "classification": classification,
            "explanation": explanation,
            "risk_scan": risk_scan,
            "form_guide": form_results,
            "expungement": exp_results,
            "escalation": escalation
        }
