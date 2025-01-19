from pydantic import BaseModel, Field
from typing import Tuple


class SttaicInfo(BaseModel):
    COORDINATES: Tuple[float, float] = Field(description="COORDINATES")
