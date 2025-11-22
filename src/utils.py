import httpx
from cep_to_coords.convert import cep_to_coords
from passlib.context import CryptContext
import jwt

from config import ALGORITHM, SECRET_KEY

from cep_to_coords.strategies import CEPAbertoConverter

from .models import FreightTypeEnum

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

async def get_coordinates_from_cep(cep: str) -> tuple[float, float]:
   coords = cep_to_coords(cep, factory=CEPAbertoConverter)
   return [coords["latitude"], coords["longitude"]]

OSRM_URL = "http://router.project-osrm.org/route/v1/driving"
async def get_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    url = f"{OSRM_URL}/{lon1},{lat1};{lon2},{lat2}?overview=false"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

        data = response.json()

        if "routes" not in data or len(data["routes"]) == 0:
            raise ValueError("Unable to calculate route using OSRM")

        distance_meters = data["routes"][0]["distance"]
        return distance_meters / 1000


def calculate_freight_price(distance_km: float, weight: float, freight_type: FreightTypeEnum) -> float:
    try:
        FreightTypeEnum(freight_type)
    except ValueError as e:
        raise e
    
    if weight <= 0:
        raise ValueError("Weight cannot be less or equal to zero")
    
    if distance_km <= 0:
        raise ValueError("Distance cannot be less or equal to zero")

    if isinstance(freight_type, FreightTypeEnum):
        freight_type_str = freight_type.value.lower()
    else:
        freight_type_str = str(freight_type).lower()

    base_rate = {
        FreightTypeEnum.normal: 5,
        FreightTypeEnum.sedex: 10,
        FreightTypeEnum.sedex10: 15
    }.get(freight_type_str)

    price = (distance_km * weight) + base_rate
    return round(price, 2)