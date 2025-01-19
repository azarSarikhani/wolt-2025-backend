from pydantic import BaseModel, Field




class Delivery(BaseModel):
    fee: int
    distance: int


class ResponseItem(BaseModel):
    total_price: int = Field(description="total price")
    small_order_surcharge: int = Field(description="small order surcharge")
    cart_value: int = Field(description="cart value")
    delivery: Delivery

class InternalError(BaseModel):
    detail: str
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "detail": "What a Terrible Failure"
            }]
        }
    }


class BadRequest(BaseModel):
    detail: str
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "detail": "delivery is not possible"
            }]
        }
    }


class ValidationError(BaseModel):
    detail: str
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "detail": "Input parameter not valid"
            }]
        }
    }