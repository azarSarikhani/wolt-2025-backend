import logging
import uvicorn
import numpy as np
from typing import Annotated
from dopc.tools.Venue import Venue
from dopc.tools.logs import getConsoleLoger
from dopc.tools.priceCalculator import priceCalculator
from dopc.tools.responseSchemas import SuccessfulFeeCalculationResposneSchema, HTTPError
from fastapi import FastAPI, HTTPException, Query
from logging import Logger


appLogger: Logger = getConsoleLoger('app')

app = FastAPI(title="Delivery fee calculator app",
              description="Delivery fee calculator app with fastAPI",
              summary="Delivery fee calculator app with fastAPI",
              version="1.0.0")


@app.get("/api/v1/delivery-order-price",
         responses={200: {"model": SuccessfulFeeCalculationResposneSchema},
                    400: {"model": HTTPError,
                          "description": "delivery is not possible"},
                    422: {"model": HTTPError, "description": "Validation error for query parameters"},
                    500: {"model": HTTPError,
                          "description": "In case something goes wrong"}})
def calculate_delivery_fee(
    					  venue_slug: Annotated[str, Query(min_length=1, description="The venue slug must be a non-empty string")],
    					  cart_value: Annotated[int, Query(ge=0, description="The total value of the cart, must be a positive integer")],
    					  user_lat: Annotated[float, Query(ge=-90, le=90, description="The user's latitude, between -90 and 90 degrees")],
   						  user_lon: Annotated[float, Query(ge=-180, le=180, description="The user's longitude, between -180 and 180 degrees")] ):
    try:
        query_inputs = {'venue_slug': venue_slug, 'cart_value': cart_value, 'user_lat': user_lat, 'user_lon': user_lon}
        venue = Venue(venue_slug=query_inputs.get('venue_slug'))
        response_dynamic = venue.getDynamicIfo()
        dynamic_info= venue.parseVenueDynamicInfo(response_dynamic)
        response_static = venue.getStaticicIfo()
        static_info= venue.parseVenueStaticInfo(response_static)
        distance , delivery_price = priceCalculator(query_inputs, static_info, dynamic_info)
        small_order_surcharge = dynamic_info.get('ORDER_MINIMUM_NO_SURCHARGE') -  query_inputs.get('cart_value')
        if delivery_price:
            result = {
                "total_price": cart_value + delivery_price,
                "small_order_surcharge": max(small_order_surcharge, 0),
                "cart_value": cart_value,
                "delivery": {
                    "fee": delivery_price,
                    "distance": distance
                }
            }
            return result
        # calculate_fee()
    except Exception as e:
        appLogger.error(e)
        raise HTTPException(
            status_code=500,
            detail="A Terrible Failure happened in calculating the fee"
        )


if __name__ == "__main__":
    print("this function is happy to be called directly.")
    config = uvicorn.Config("app:app", port=5000, log_level="info", reload=False, host='0.0.0.0')
    server = uvicorn.Server(config)
    server.run()