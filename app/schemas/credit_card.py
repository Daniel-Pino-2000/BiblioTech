from pydantic import BaseModel, Field, field_validator, ConfigDict


class CreditCardCreate(BaseModel):
    # Accepted at the API boundary but never persisted in full;
    # the service layer stores only the last 4 digits.
    card_number: str = Field(min_length=12, max_length=19)
    card_holder_name: str
    exp_month: int = Field(ge=1, le=12)
    exp_year: int = Field(ge=2024, le=2100)

    @field_validator("card_number")
    @classmethod
    def digits_only(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("card_number must contain digits only")
        return value


class CreditCardResponse(BaseModel):
    id: int
    last4: str
    card_holder_name: str
    exp_month: int
    exp_year: int

    model_config = ConfigDict(from_attributes=True)
