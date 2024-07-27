import pandas as pd
import numpy as np
from numpy.typing import NDArray
from functools import lru_cache

from stochastic_volatility_models.config import MODULE_DIRECTORY
from stochastic_volatility_models.src.data.prices import DEFAULT_CHUNKSIZE


@lru_cache
def get_expiries_of_strike(
	ticker: str,
	strike: int,
	monthly: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> tuple[np.datetime64, ...]:
	path: str = f"{MODULE_DIRECTORY}/data/options/{ticker.lower()}.csv"
	option_prices_iter = pd.read_csv(
		path,
		index_col=[0, 1],
		chunksize=chunksize,
	)

	call_expiries = set()
	put_expiries = set()

	for option_prices in option_prices_iter:
		call_expiries.update(option_prices.loc[(option_prices["strike_price"] == strike * 1000) & (option_prices["cp_flag"] == "C") & (option_prices["am_settlement"] == int(monthly)), "exdate"].values)
		put_expiries.update(option_prices.loc[(option_prices["strike_price"] == strike * 1000) & (option_prices["cp_flag"] == "P") & (option_prices["am_settlement"] == int(monthly)), "exdate"].values)

	expiries = {
		"C": tuple(sorted(call_expiries)),
		"P": tuple(sorted(put_expiries)),
	}

	if expiries["C"] != expiries["P"]:
		raise ValueError(f"Calls and Puts have different expiries: \nCalls: {expiries["C"]}\nPuts: {expiries["P"]}")

	expiries = expiries["C"]

	return expiries


def get_expiries_of_strikes(
	ticker: str,
	strikes: NDArray[np.int64],
	monthly: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> tuple[np.datetime64, ...]:
	expiries = tuple(
		sorted(
			set.intersection(
				*[
					set(
						get_expiries_of_strike(
							ticker=ticker,
							strikes=strike,
							monthly=monthly,
							chunksize=chunksize,
						)
					)
					for strike in strikes
				]
			)
		)
	)

	return expiries
