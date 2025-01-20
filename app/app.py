import uvicorn
from logging import Logger
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query, status
from dopc.tools.Venue import Venue
from dopc.tools.logs import getConsoleLoger
from dopc.tools.priceCalculator import priceCalculator
from dopc.tools.responseSchemas import ResponseItem, InternalError, BadRequest, ValidationError
from dopc.tools.venuSchemas import StaticInfo, DynamicInfo

appLogger: Logger = getConsoleLoger('app')

app = FastAPI(title="Delivery fee calculator app",
              description="Delivery fee calculator app with fastAPI",
              summary="Delivery fee calculator app with fastAPI",
              version="1.0.0")


def queryVenue(query_inputs: dict) -> tuple[dict]:
    venue = Venue(venue_slug=query_inputs.get('venue_slug'))
    response_dynamic = venue.getDynamicIfo()
    dynamic_info: DynamicInfo = venue.parseVenueDynamicInfo(response_dynamic)
    response_static = venue.getStaticicIfo()
    static_info: StaticInfo = venue.parseVenueStaticInfo(response_static)
    return dynamic_info, static_info


@app.get("/api/v1/delivery-order-price",
         responses={200: {"model": ResponseItem},
                    400: {"model": BadRequest,
                          "description": "delivery is not possible"},
                    422: {"model": ValidationError, "description": "Validation error for query parameters"},
                    500: {"model": InternalError,
                          "description": "In case something goes wrong"}})
def calculate_delivery_fee(
                            venue_slug: Annotated[str, Query(min_length=1, description="The venue slug")],
                            cart_value: Annotated[int, Query(ge=0, description="The total value of the cart")],
                            user_lat: Annotated[float, Query(ge=-90, le=90, description="The user's latitude")],
                            user_lon: Annotated[float, Query(ge=-180, le=180, description="The user's longitude")]):
    try:
        query_inputs = {'venue_slug': venue_slug, 'cart_value': cart_value, 'user_lat': user_lat, 'user_lon': user_lon}
        dynamic_info, static_info = queryVenue(query_inputs)
        distance, delivery_price = priceCalculator(query_inputs, static_info, dynamic_info)
        small_order_surcharge = dynamic_info.get('ORDER_MINIMUM_NO_SURCHARGE') - query_inputs.get('cart_value')
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
            return ResponseItem(
                    total_price=result.get('total_price'),
                    small_order_surcharge=result.get('small_order_surcharge'),
                    cart_value=result.get('cart_value'),
                    delivery=result.get('delivery')
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='delivery not possible, distance is too long'
            )
    except Exception as e:
        if not isinstance(e, HTTPException):
            appLogger.error(e)
            raise HTTPException(
                status_code=500,
                detail="A Terrible Failure happened in calculating the fee"
            )
        else:
            appLogger.error(e)
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail
            )


if __name__ == "__main__":
    print("this function is happy to be called directly.")
    config = uvicorn.Config("app:app", port=5000, log_level="info", reload=False, host='0.0.0.0')
    server = uvicorn.Server(config)
    server.run()
