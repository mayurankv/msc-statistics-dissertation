from typing import Optional
import pandas as pd
from pandas import DataFrame, IndexSlice
import numpy as np
from numpy.typing import NDArray
from functools import lru_cache

from stochastic_volatility_models.config import MODULE_DIRECTORY
from stochastic_volatility_models.src.utils.cache import df_cache


DEFAULT_CHUNKSIZE = 20000


@lru_cache
def get_price(
	ticker: str,
	time: np.datetime64,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> float:
	path: str = f"{MODULE_DIRECTORY}/data/securities/{ticker.lower()}.csv"
	prices_iter = pd.read_csv(
		path,
		index_col=[0],
		chunksize=chunksize,
	)

	key = np.datetime_as_string(time, unit="D")

	for prices in prices_iter:
		if key in prices.index:
			return prices.loc[key, "close"]

	raise ValueError("Date not found")


@lru_cache
def get_future_price(
	ticker: str,
	time: np.datetime64,
	expiry: Optional[np.datetime64] = None,
	am_settlement: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> float:
	path: str = f"{MODULE_DIRECTORY}/data/futures/{ticker.lower()}.csv"
	future_prices_iter = pd.read_csv(
		path,
		index_col=[0, 1, 2],
		chunksize=chunksize,
	)

	if expiry is not None:
		key = IndexSlice[
			np.datetime_as_string(time, unit="D"),
			np.datetime_as_string(expiry, unit="D"),
			int(am_settlement),
		]

		for future_prices in future_prices_iter:
			if key in future_prices.index:
				return future_prices.loc[key, "forwardprice"]

		raise ValueError("Future not found")
	else:
		key = IndexSlice[np.datetime_as_string(time, unit="D"), int(am_settlement)]
		future_prices = pd.concat(
			objs=[
				future_prices.xs(
					key=key,
					level=(1, 2),
				)
				for future_prices in future_prices_iter
				if key in future_prices.index.droplevel(0).unique()
			]
		).sort_index()
		future_prices.index = pd.to_datetime(future_prices.index)

		relevant_expiries = future_prices.index[future_prices.index > time]
		if not relevant_expiries.empty:
			price = future_prices.at[relevant_expiries.min(), "forwardprice"]
		else:
			raise ValueError("No Future could be found")

	return price


@df_cache(arg_num=1, arg_name="symbols")
def get_option_prices(
	ticker: str,
	symbols: NDArray[str],  # type: ignore
	time: np.datetime64,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> DataFrame:
	path: str = f"{MODULE_DIRECTORY}/data/options/{ticker.lower()}.csv"
	option_prices_iter = pd.read_csv(
		path,
		index_col=[0, 1],
		chunksize=chunksize,
	)

	option_values = DataFrame(
		data=None,
		index=symbols,
		columns=["Bid", "Ask", "Mid"],
	)

	count = 0
	for option_prices in option_prices_iter:
		key = np.datetime_as_string(time, unit="D")
		if key in option_prices.index.get_level_values(level=1):
			priceable_symbols = option_prices.xs(key=key, level=1).index
			priced_symbols = np.array([symbol for symbol in symbols if symbol in priceable_symbols])

			option_values.loc[priced_symbols, ["Bid", "Ask"]] = option_prices.loc[IndexSlice[priced_symbols, key], ["best_bid", "best_offer"]].values
			option_values.loc[priced_symbols, "Mid"] = (option_values.loc[priced_symbols, "Bid"] + option_values.loc[priced_symbols, "Ask"]) / 2

			count += len(priced_symbols)

			if count >= len(symbols):
				break

	return option_values
