from pydantic import BaseModel, Field


class SuccessfulFeeCalculationResposneSchema(BaseModel):
    result: dict = Field(description="details")


class HTTPError(BaseModel):
    detail: str
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "detail": "What a Terrible Failure"
            }]
        }
    }