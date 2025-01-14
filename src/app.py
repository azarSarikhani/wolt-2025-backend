import logging
import uvicorn
from tools.priceCalculator import priceCalculator
from tools.loadDb import load_db
from schemas.resposne_schemas import SuccessfulFeeCalculationResposneSchema, HTTPError
from fastapi import FastAPI, HTTPException
from schemas.FeeCalcRequestSchema import FeeCalcRequestSchema