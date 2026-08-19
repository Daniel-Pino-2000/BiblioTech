from pydantic import BaseModel, Field

class CreditCardCreate(BaseModel):
    card_number: str = Field(min_length=12, max_length=25)
    card_holder_name: str
    exp_month: int = Field(ge=1, le=12)
    exp_year: int = Field(ge=2024, le=2100)
