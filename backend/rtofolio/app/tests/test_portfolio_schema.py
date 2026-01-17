import json
from app.schemas.portfolio import PortfolioSchema


def test_portfolio_schema_is_valid():
    with open("app/samples/portfolio_v1.json", "r") as f:
        sample_data = json.load(f)

    portfolio = PortfolioSchema.model_validate(sample_data)

    # basic sanity checks
    assert portfolio.theme.maxWidth is not None
    assert len(portfolio.sections) > 0
