from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# ใช้ absolute path เพื่อให้โหลด .env ได้ไม่ว่า cwd จะเป็นอะไร
_ENV_FILE = Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), env_ignore_empty=True, extra="ignore")

    supabase_url: str
    supabase_key: str
    anthropic_api_key: str
    cors_origins: list[str] = ["http://localhost:3000"]

    # News sources (RSS)
    news_sources: list[str] = [
        # ไทย
        "https://www.bangkokpost.com/rss/data/business.xml",
        "https://feeds.thairath.co.th/thairath-money.xml",
        "https://rss.prachachat.net/category/finance/feed",
        # ต่างประเทศ
        "https://feeds.reuters.com/reuters/businessNews",
        "https://feeds.reuters.com/reuters/technologyNews",
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        # Yahoo Finance
        "https://finance.yahoo.com/rss/topfinstories",
        "https://finance.yahoo.com/rss/2.0/headline?s=^SET.BK&region=US&lang=en-US",
    ]

    # Scheduler
    news_fetch_hour: int = 6
    analysis_hour: int = 7


settings = Settings()
