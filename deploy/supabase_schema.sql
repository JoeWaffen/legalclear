-- LegalClear Supabase Core Schema Initialization

-- 1. Users Table
CREATE TABLE public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    subscription_status TEXT DEFAULT 'free',
    subscription_id TEXT,
    free_doc_used BOOLEAN DEFAULT FALSE,
    preferred_language TEXT DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. Sessions Table
CREATE TABLE public.sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    document_filename TEXT,
    document_token_count INTEGER,
    price_tier TEXT,
    price_paid_usd INTEGER,
    payment_type TEXT,
    payment_status TEXT DEFAULT 'pending',
    stripe_payment_intent TEXT,
    stripe_subscription_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 3. Documents Table
CREATE TABLE public.documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES public.sessions(id) ON DELETE CASCADE,
    document_text TEXT,
    classification JSONB DEFAULT '{}'::jsonb,
    explanation JSONB DEFAULT '{}'::jsonb,
    form_guide JSONB DEFAULT '{}'::jsonb,
    risk_scan JSONB DEFAULT '{}'::jsonb,
    expungement_guide JSONB DEFAULT '{}'::jsonb,
    escalation JSONB DEFAULT '{}'::jsonb,
    language TEXT DEFAULT 'en',
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 4. Chat Messages Table
CREATE TABLE public.chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES public.documents(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    language TEXT DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 5. Push Tokens Table
CREATE TABLE public.push_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    expo_token TEXT NOT NULL,
    platform TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 6. Usage Stats Table
CREATE TABLE public.usage_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_category TEXT,
    jurisdiction TEXT,
    language TEXT,
    price_tier TEXT,
    processing_time_seconds FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Note: Because Supabase creates Data APIs automatically using PostgREST, we need to instruct it to refresh its schema cache manually after creating tables.
NOTIFY pgrst, 'reload schema';
