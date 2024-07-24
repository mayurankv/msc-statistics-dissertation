from datetime import datetime
from typing import TypedDict, Literal

PricingModels = Literal["Black-Scholes", "Black-76"]


class OptionParameters(TypedDict):
	type: Literal["C", "P"]
	strike: int
	expiry: datetime


class ObjectiveFunctionParameters(TypedDict):
	prices: float
	model_implied_volatility: float
	pricing_implied_volatility: float
	vol_prices: float
	vol_model_implied_volatility: float
	vol_pricing_implied_volatility: float
	atm_skew: float
