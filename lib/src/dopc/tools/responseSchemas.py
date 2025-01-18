from pydantic import BaseModel, Field


class SuccessfulFeeCalculationResposneSchema(BaseModel):
    delivery_fee: int = Field(description="Calculated delivery fee in the \
    lowest denomination of the local currency.")


class HTTPError(BaseModel):
    detail: str
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "detail": "What a Terrible Failure"
            }]
        }
    }