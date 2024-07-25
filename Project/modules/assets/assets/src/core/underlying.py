from typing import Optional, Literal
from pandas import DataFrame
import numpy as np


class _BaseAsset:
	def __init__(
		self,
		ticker: str,
	) -> None:
		self.ticker = ticker.upper()

	def price(
		self,
		time: np.datetime64,
	) -> float:
		# TODO (@mayurankv): Pull price
		return time

	def prices(
		self,
		start_time: np.datetime64,
		end_time: np.datetime64,
		intraday: bool = False,
	) -> DataFrame:
		# TODO (@mayurankv): Pull prices
		return start_time, end_time, intraday


Future = _BaseAsset


class _Underlying(_BaseAsset):
	def __init__(
		self,
		ticker: str,
	) -> None:
		super(_Underlying, self).__init__(ticker=ticker)
		self.futures: dict[np.datetime64 | Literal["Continuous"], Future] = {}

	def set_future(
		self,
		future_ticker: str,
		future_expiry: Optional[np.datetime64] = None,
	) -> None:
		self.futures[future_expiry if future_expiry is not None else "Continuous"] = Future(
			ticker=future_ticker,
		)

	def get_future(
		self,
		time: Optional[np.datetime64] = None,
	) -> Future:
		expiry = "Continuous" if time is None else min([expiry for expiry in self.futures.keys() if expiry != "Continuous" and expiry > time], key=lambda expiry: expiry - time)
		return self.futures[expiry]


class _WeightedUnderlying(_Underlying):
	def weights(
		self,
		time: np.datetime64,
	) -> dict[str, float]:
		# TODO (@mayurankv): Pull weights
		return time


Stock = _Underlying
Index, ETF = _WeightedUnderlying, _WeightedUnderlying
Underlying = Stock | Index | ETF  # | FX | Commodity
