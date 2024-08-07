from __future__ import annotations
from typing import TYPE_CHECKING, Optional, cast
import numpy as np
from numpy.typing import NDArray
from pandas import Series
from scipy.interpolate import CubicSpline

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying
from stochastic_volatility_models.src.utils.options.expiry import time_to_expiry, annualise
from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
from stochastic_volatility_models.src.data.option_implied_prices import get_atm_prices
from stochastic_volatility_models.src.data.prices import DEFAULT_CHUNKSIZE


def _get_dividend_yield(
	ticker: str,
	spot: float,
	time: np.datetime64,
	expiries: Optional[NDArray[np.datetime64]] = None,
	monthly: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> Series:
	atm_prices = get_atm_prices(
		ticker=ticker,
		spot=spot,
		time=time,
		monthly=monthly,
		chunksize=chunksize,
	)

	if expiries is not None:
		atm_prices = atm_prices.loc[np.datetime_as_string(expiries)].reindex(index=np.datetime_as_string(expiries))  # type: ignore
	else:
		expiries = np.array(atm_prices.index, dtype=np.datetime64)

	time_to_expiries = time_to_expiry(
		time=time,
		option_expiries=expiries,
	)
	risk_free_rates = get_risk_free_interest_rate(
		time=time,
		time_to_expiry=time_to_expiries,
	)
	dividend_yields = cast(
		Series,
		-np.log(((atm_prices["C"] - atm_prices["P"]) + (atm_prices["strike_price"] / 1000) * np.exp(-risk_free_rates * time_to_expiries)) / spot) / time_to_expiries,
	)

	return dividend_yields


def get_dividend_yield(
	underlying: Underlying,
	time: np.datetime64,
	expiries: Optional[NDArray[np.datetime64]] = None,
	monthly: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> NDArray[np.float64]:
	dividend_yields = _get_dividend_yield(
		ticker=underlying.ticker,
		spot=underlying.price(time=time),
		time=time,
		expiries=expiries,
		monthly=monthly,
		chunksize=chunksize,
	).to_numpy()

	return dividend_yields


def interpolate_dividend_yield(
	ticker: str,
	spot: float,
	time: np.datetime64,
	time_to_expiries: NDArray[np.float64],
	monthly: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> NDArray[np.float64]:
	implied_dividend_yields = _get_dividend_yield(
		ticker=ticker,
		spot=spot,
		time=time,
		expiries=None,
		monthly=monthly,
		chunksize=chunksize,
	)

	implied_dividend_yields.index = annualise(np.array(implied_dividend_yields.index, dtype=np.datetime64) - time)  # type: ignore

	cs = CubicSpline(implied_dividend_yields.index, implied_dividend_yields.values)
	dividend_yields = cast(NDArray[np.float64], cs(time_to_expiries))

	return dividend_yields
