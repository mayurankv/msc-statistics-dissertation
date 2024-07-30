from __future__ import annotations
from typing import TYPE_CHECKING, cast
import numpy as np
from numpy.typing import NDArray
from pandas import Series

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying
from stochastic_volatility_models.src.utils.options.expiry import time_to_expiry
from stochastic_volatility_models.src.utils.cache import np_cache
from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
from stochastic_volatility_models.src.data.option_implied_prices import get_atm_prices
from stochastic_volatility_models.src.data.prices import DEFAULT_CHUNKSIZE


@np_cache(arg_num=2, arg_name="expiries")
def get_dividend_yield(
	underlying: Underlying,
	time: np.datetime64,
	expiries: NDArray[np.datetime64],
	monthly: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> NDArray[np.float64]:
	atm_prices = get_atm_prices(
		underlying=underlying,
		time=time,
		expiries=expiries,
		monthly=monthly,
		chunksize=chunksize,
	)
	t2x = time_to_expiry(time=time, option_expiries=expiries)
	r = get_risk_free_interest_rate(time=time, time_to_expiry=t2x)
	dividend_yields = -np.log(((atm_prices["C"] - atm_prices["P"]) + (atm_prices["strike_price"] / 1000) * np.exp(-r * t2x)) / underlying.price(time=time)) / t2x
	dividend_yields = cast(Series, dividend_yields).to_numpy()

	return dividend_yields
