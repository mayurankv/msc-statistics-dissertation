import pandas as pd
from pandas import DataFrame, IndexSlice
import numpy as np
from numpy.typing import NDArray

from stochastic_volatility_models.config import MODULE_DIRECTORY
from stochastic_volatility_models.src.types.types import OptionParameters, OptionTypes, PriceTypes

PRICE_TYPE_STRINGS = {
	"bid": "best_bid",
	"ask": "best_offer",
}


def get_options_symbols(
	ticker: str,
	option_type: OptionTypes,
	expiry: np.datetime64,
	strike: int,
	monthly: bool = True,
) -> str:
	return f"{ticker}{'W' if monthly else ''} {np.datetime_as_string(expiry, unit="D").replace('-','')}{option_type}{int(strike)}"


def get_option_parameters(
	ticker: str,
	symbol: str,
) -> OptionParameters:
	root, suffix = symbol.split(" ")
	option_type = suffix[8:9]
	if option_type not in ["C", "P"]:
		raise ValueError("Invalid symbol")
	assert isinstance(option_type, OptionTypes)
	option_parameters: OptionParameters = {
		"type": option_type,
		"strike": int(suffix[9:]),
		"expiry": np.datetime64(f"{suffix[:4]}-{suffix[4:6]}-{suffix[6:8]}"),
		"monthly": not (root[len(ticker) :].endswith("W")),
	}

	return option_parameters


def get_options_parameters(
	ticker: str,
	symbols: NDArray[str],  # type: ignore
) -> NDArray[OptionParameters]:  # type: ignore
	options_parameters = np.array([get_option_parameters(ticker=ticker, symbol=symbol) for symbol in symbols])

	return options_parameters


def get_option_prices(
	ticker: str,
	symbols: NDArray[str],  # type: ignore
	time: np.datetime64,
	price_type: PriceTypes,
) -> DataFrame:
	path = f"{MODULE_DIRECTORY}/data/options/{ticker.lower()}.csv"
	option_prices_iter = pd.read_csv(
		path,
		index_col=[0, 1, 2, 3, 4],
		chunksize=20000,
	)
	option_values = DataFrame(None, index=symbols)
	for option_prices in option_prices_iter:
		for symbol in symbols:
			key = IndexSlice[symbol, time]
			if key in option_prices.index:
				try:
					value: float = option_prices.at[key, PRICE_TYPE_STRINGS[price_type]]
				except KeyError:
					raise ValueError("Price type not recognised")
				option_values[symbol] = value
	return option_values
