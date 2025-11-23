from typing import Any, Dict
from src import utils
from src.view.schemas.freight import FreightCalcRequest


class FreightUseCases:
    def __init__(self):
        pass

    async def calculate_quote(self, payload: FreightCalcRequest) -> Dict[str, Any]:
        try:
            lat1, lon1 = await utils.get_coordinates_from_cep(payload.origin_zip)
            lat2, lon2 = await utils.get_coordinates_from_cep(payload.destination_zip)
        except Exception as e:
            raise ValueError(f"Failed to get coordinates: {e}")

        try:
            distance_km = await utils.get_distance_km(lat1, lon1, lat2, lon2)
        except Exception as e:
            raise ValueError(f"Distance calculation failed: {e}")

        try:
            price = utils.calculate_freight_price(distance_km=distance_km, weight=payload.weight, freight_type=payload.freight_type)
        except Exception as e:
            raise ValueError(f"Price calculation failed: {e}")

        return { "distance_km": round(distance_km, 2), "price": round(price, 2), "freight_type": payload.freight_type }
