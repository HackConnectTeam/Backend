from typing import List
from fastapi import APIRouter
import pycountry

from src.app.schemas.country import Country

router = APIRouter()


@router.get("/countries/", response_model=List[Country])
def get_countries():
    countries = [
        {"code": country.alpha_2, "name": country.name}
        for country in pycountry.countries
    ]
    countries.sort(key=lambda x: x["name"])
    return countries
