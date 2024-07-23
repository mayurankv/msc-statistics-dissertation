from datetime import datetime
from typing import TypedDict, Literal

PricingModels = Literal["Black-Scholes", "Black-76"]


class OptionParameters(TypedDict):
	type: Literal["C", "P"]
	strike: int
	expiry: datetime
