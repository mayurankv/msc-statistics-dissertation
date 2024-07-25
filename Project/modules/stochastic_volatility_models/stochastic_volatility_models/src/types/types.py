import numpy as np
from typing import TypedDict, Literal


PriceTypes = Literal["Bid", "Ask", "Mid"]
OptionTypes = Literal["C", "P"]
PricingModels = Literal["Black-Scholes", "Black-76"]


class OptionParameters(TypedDict):
	type: OptionTypes
	strike: int
	expiry: np.datetime64
	monthly: bool


class ObjectiveFunctionParameters(TypedDict):
	prices: float
	model_implied_volatility: float
	pricing_implied_volatility: float
	vol_prices: float
	vol_model_implied_volatility: float
	vol_pricing_implied_volatility: float
	atm_skew: float
