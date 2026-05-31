from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from datetime import date
from app.core.supabase import get_supabase
from app.services.ai_analyzer import analyze_daily_news
import anthropic

router = APIRouter()


@router.get("/")
def list_summaries(limit: int = Query(7, le=30)):
    db = get_supabase()
    return db.table("daily_summaries").select("*, stock_picks(*)").order("date", desc=True).limit(limit).execute().data


@router.get("/today")
def today_summary():
    db = get_supabase()
    today = date.today().isoformat()
    result = db.table("daily_summaries").select("*, stock_picks(*)").eq("date", today).execute().data
    return result[0] if result else None


@router.post("/analyze")
async def trigger_analysis(analysis_date: date | None = None):
    try:
        result = await analyze_daily_news(analysis_date)
        return result
    except anthropic.AuthenticationError:
        return JSONResponse(status_code=402, content={"error": "Anthropic API key ไม่ถูกต้อง"})
    except anthropic.BadRequestError as e:
        if "credit balance" in str(e):
            return JSONResponse(status_code=402, content={
                "error": "เครดิต Anthropic หมด",
                "detail": "กรุณาเติมที่ console.anthropic.com/settings/billing"
            })
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
