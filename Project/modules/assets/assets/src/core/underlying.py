from typing import Optional, Literal
from datetime import datetime
from pandas import DataFrame


class _BaseAsset:
	def __init__(
		self,
		ticker: str,
	) -> None:
		self.ticker = ticker

	def price(
		self,
		time: datetime,
	) -> float:
		# Pull price
		return time

	def prices(
		self,
		start_time: datetime,
		end_time: datetime,
		intraday: bool = False,
	) -> DataFrame:
		# Pull prices
		return start_time, end_time, intraday


Future = _BaseAsset


class _Underlying(_BaseAsset):
	def __init__(
		self,
		ticker: str,
	) -> None:
		super(_Underlying, self).__init__(ticker=ticker)
		self.futures: dict[datetime | Literal["Continuous"], Future] = {}

	def set_future(
		self,
		future_ticker: str,
		future_expiry: Optional[datetime] = None,
	) -> None:
		self.futures[future_expiry if future_expiry is not None else "Continuous"] = Future(
			ticker=future_ticker,
		)

	def get_future(
		self,
		time: Optional[datetime] = None,
	) -> Future:
		expiry = "Continuous" if time is None else min([expiry for expiry in self.futures.keys() if expiry != "Continuous" and expiry > time], key=lambda expiry: expiry - time)
		return self.futures[expiry]


class _WeightedUnderlying(_Underlying):
	def weights(
		self,
		time: datetime,
	) -> dict[str, float]:
		# Pull weights
		return time


Stock = _Underlying
Index, ETF = _WeightedUnderlying, _WeightedUnderlying
Underlying = Stock | Index | ETF  # | FX | Commodity
