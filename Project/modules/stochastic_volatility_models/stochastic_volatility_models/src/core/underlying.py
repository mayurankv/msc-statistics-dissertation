from typing import Optional
import numpy as np

from stochastic_volatility_models.src.data.prices import get_future_price, get_price


class Underlying:
	def __init__(
		self,
		ticker: str,
	) -> None:
		self.ticker = ticker.upper()

	def price(
		self,
		time: np.datetime64,
	) -> float:
		return get_price(
			ticker=self.ticker,
			time=time,
		)

	def future_price(
		self,
		time: np.datetime64,
		expiry: Optional[np.datetime64] = None,
		am_settlement: bool = True,
	) -> float:
		return get_future_price(
			ticker=self.ticker,
			time=time,
			expiry=expiry,
			am_settlement=am_settlement,
		)
