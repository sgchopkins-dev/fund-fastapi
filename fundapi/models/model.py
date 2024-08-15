from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

from enum import Enum

#add classes in here
class Currency(str, Enum):
    """
    Used to provide validation options for different currencies
    """
    GBP = "GBP"
    USD = "USD"
    EUR = "EUR"

class Price_Engine(str, Enum):
    """
    Used to provide validation options for different methods of pricing lookup
    FT will be used by the scraper to call an FT related scraper function
    Static will be used by the scraper to bypass
    """
    FT = "FT"
    ST = "Static"

class Platform(str, Enum):
    """
    Used to provide validation options for certain Fund Platforms
    """
    HL = "Hargreaves Lansdown"
    Fidelity = "Fidelity"
    IV = "InvestEngine"
    III = "Interactive Investor"
    AJ = "AJ Bell Youinvest"
    CAP = "Citigroup CAP"
    PEN = "Pension"

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class FundModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", )
    name: str = Field(...)
    type: str = Field(...)
    fclass: Optional[str]
    platform: Platform = Field(...)
    currency: Currency = Field(...)
    platform_charges: float = Field(...)
    fund_charges: float = Field(...)
    price_engine: Price_Engine = Field(...)
    url: str = Field(..., max_length=400)
    portfolio: str = Field(...)
    units: float = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Baillie Gifford American",
                "type": "Accumulation",
                "fclass": "Class B",
                "platform": "Hargreaves Lansdown",
                "currency": "GBP",
                "platform_charges": 0.45,
                "fund_charges": 0.51,
                "price_engine": "FT",
                "url": "https://markets.ft.com/data/funds/tearsheet/summary?s=GB0006061963:GBX",
                "portfolio": "Alison - HL (ISA)",
                "units": 29.859
            }
        }

class UpdateFundModel(BaseModel):
    name: Optional[str]
    type: Optional[str]
    fclass: Optional[str]
    platform: Optional[Platform]
    currency: Optional[Currency]
    platform_charges: Optional[float]
    fund_charges: Optional[float]
    price_engine: Optional[Price_Engine]
    url: Optional[str]
    portfolio: Optional[str]
    units: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Baillie Gifford American",
                "type": "Accumulation",
                "fclass": "Class B",
                "platform": "Hargreaves Lansdown",
                "currency": "GBP",
                "platform_charges": 0.45,
                "fund_charges": 0.51,
                "price_engine": "FT",
                "url": "https://markets.ft.com/data/funds/tearsheet/summary?s=GB0006061963:GBX",
                "portfolio": "Alison - HL (ISA)",
                "units": 29.859
            }
        }

        