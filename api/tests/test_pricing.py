from api.models.schemas import PropertyInput
from api.services.pricing import estimate_price


def test_estimate_price_positive() -> None:
    payload = PropertyInput(
        city="Lisbon",
        district="Alvalade",
        area_m2=100,
        rooms=3,
        year_built=2000,
        energy_rating="C",
        listing_price_eur=300000,
    )

    assert estimate_price(payload) > 0
