from bson import ObjectId
import json
from pathlib import Path

from fastapi import APIRouter, Request, HTTPException
from app.schemas.portfolio import PortfolioSchema

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/sample", response_model=PortfolioSchema)
def get_sample_portfolio():
    # portfolio.py is in app/api/v1/
    # so parents[2] -> app/
    app_dir = Path(__file__).resolve().parents[2]
    sample_path = app_dir / "samples" / "portfolio_v1.json"

    with sample_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Validate with Pydantic (will throw 422-ish error if invalid)
    portfolio = PortfolioSchema.model_validate(data)

    # Return JSON using original keys (aliases like "color-palette")
    return portfolio.model_dump(by_alias=True)

@router.post("/")
async def create_portfolio(portfolio: PortfolioSchema, request: Request, user_id : str):
    db = request.app.mongodb
    # In a real app, you'd save this to MongoDB
    portfolio_dict = portfolio.model_dump(by_alias=True)
    
    portfolio_data = {
        "user_id" : user_id,
        **portfolio_dict
    }

    result = await db["portfolios"].insert_one(portfolio_data)
    
    return {
        "message": "Portfolio saved successfully",
        "id": str(result.inserted_id)
    }

@router.get("/{portfolio_id}", response_model=PortfolioSchema)
async def get_portfolio(portfolio_id: str, request: Request):
    db = request.app.mongodb
    
    if not ObjectId.is_valid(portfolio_id):
        raise HTTPException(status_code=400, detail="Invalid portfolio ID format")
    
    portfolio_data = await db["portfolios"].find_one({"_id": ObjectId(portfolio_id)})

    if not portfolio_data:
        raise HTTPException(status_code=404, detail="Portfolio with id '{}' was not found".format(portfolio_id))
    
    validated_data = PortfolioSchema.model_validate(portfolio_data)

    return validated_data

@router.patch("/{portfolio_id}", response_model=PortfolioSchema)
async def update_portfolio(portfolio_id: str, portfolio: PortfolioSchema, request: Request):
    db = request.app.mongodb
    
    if not ObjectId.is_valid(portfolio_id):
        raise HTTPException(status_code=400, detail="Invalid portfolio ID format")
    
    portfolio_data = await db["portfolios"].find_one({"_id": ObjectId(portfolio_id)})
    
    if not portfolio_data:
        raise HTTPException(status_code=404, detail="Portfolio with id '{}' was not found".format(portfolio_id))
    
    updated_data = portfolio.model_dump(by_alias=True)
    updated_data.pop("_id", None)
    
    result = await db["portfolios"].update_one({"_id": ObjectId(portfolio_id)}, {"$set": updated_data})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Portfolio with id '{}' was not found".format(portfolio_id))
    
    return portfolio