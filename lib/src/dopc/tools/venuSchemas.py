from pydantic import BaseModel, Field
from typing import Tuple, List


class StaticInfo(BaseModel):
    COORDINATES: Tuple[float, float] = Field(description="COORDINATES")


class DynamicInfo(BaseModel):
    ORDER_MINIMUM_NO_SURCHARGE: int
    BASE_PRICE: int
    DISTANCE_RANGES: List[dict]
