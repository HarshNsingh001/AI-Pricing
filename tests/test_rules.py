from app.pricing_engine.rules import recommend_price

def test_basic_rules():
    price, factors, why = recommend_price(
        current_price=250,
        competitor_prices=[240, 260, 245],
        weather={"temperature": 32, "condition": "Sunny"},
        events=[{"name": "Fest", "popularity": "High", "distance_km": 2.5}],
    )
    assert price > 240
    assert factors["weather_multiplier"] >= 1.0