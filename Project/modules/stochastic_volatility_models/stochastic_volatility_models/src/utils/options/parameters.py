from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.volatility_surface import OptionTypes, OptionParameters


def get_option_symbol(
	ticker: str,
	option_type: OptionTypes,
	expiry: np.datetime64,
	strike: int,
	monthly: bool = True,
) -> str:
	return f"{ticker}{'' if monthly else 'W'} {np.datetime_as_string(expiry, unit="D").replace('-','')[2:]}{option_type}{strike * 1000}"


def get_option_parameters(
	ticker: str,
	symbol: str,
) -> OptionParameters:
	root, suffix = symbol.split(" ")
	option_type = suffix[6:7]
	if option_type not in ["C", "P"]:
		raise ValueError("Invalid symbol")
	option_parameters: OptionParameters = {
		"type": option_type,  # type: ignore
		"strike": int(int(suffix[7:]) / 1000),
		"expiry": np.datetime64(f"20{suffix[:2]}-{suffix[2:4]}-{suffix[4:6]}"),
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
