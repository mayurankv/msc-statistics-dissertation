import numpy as np
from numpy.typing import NDArray

from stochastic_volatility_models.src.types.types import OptionParameters, OptionTypes


def get_option_symbol(
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


def get_options_parameters_transpose(
	ticker: str,
	symbols: NDArray[str],  # type: ignore
) -> dict[str, NDArray]:  # type: ignore
	options_parameters_transpose = {
		"type": np.array([get_option_parameters(ticker=ticker, symbol=symbol)["type"] for symbol in symbols]),
		"strike": np.array([get_option_parameters(ticker=ticker, symbol=symbol)["strike"] for symbol in symbols]),
		"expiry": np.array([get_option_parameters(ticker=ticker, symbol=symbol)["expiry"] for symbol in symbols]),
		"monthly": np.array([get_option_parameters(ticker=ticker, symbol=symbol)["monthly"] for symbol in symbols]),
	}

	return options_parameters_transpose
