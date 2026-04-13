from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_SMALL: str = "price_xxx"
    STRIPE_PRICE_MEDIUM: str = "price_xxx"
    STRIPE_PRICE_LARGE: str = "price_xxx"
    STRIPE_SUBSCRIPTION_PRICE_ID: str = "price_xxx"
    API_KEY: str = ""
    ENVIRONMENT: str = "development"
    EXPO_PUSH_TOKEN_TABLE: str = "push_tokens"
    MESSAGING_PLATFORM: str = ""

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == 'development'

settings = Settings()
