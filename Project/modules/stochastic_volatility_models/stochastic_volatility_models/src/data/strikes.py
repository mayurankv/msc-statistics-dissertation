import pandas as pd
import numpy as np
from numpy.typing import NDArray
from functools import lru_cache

from stochastic_volatility_models.config import MODULE_DIRECTORY
from stochastic_volatility_models.src.data.prices import DEFAULT_CHUNKSIZE


@lru_cache
def get_strikes_of_expiry(
	ticker: str,
	expiry: np.datetime64,
	monthly: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> tuple[int, ...]:
	path: str = f"{MODULE_DIRECTORY}/data/options/{ticker.lower()}.csv"
	option_prices_iter = pd.read_csv(
		path,
		index_col=[0, 1],
		chunksize=chunksize,
	)

	call_strikes = set()
	put_strikes = set()

	for option_prices in option_prices_iter:
		call_strikes.update(option_prices.loc[(option_prices["exdate"] == np.datetime_as_string(expiry, unit="D")) & (option_prices["cp_flag"] == "C") & (option_prices["am_settlement"] == int(monthly)), "strike_price"].values / 1000)
		put_strikes.update(option_prices.loc[(option_prices["exdate"] == np.datetime_as_string(expiry, unit="D")) & (option_prices["cp_flag"] == "P") & (option_prices["am_settlement"] == int(monthly)), "strike_price"].values / 1000)

	strikes = {
		"C": tuple(sorted(call_strikes)),
		"P": tuple(sorted(put_strikes)),
	}

	if strikes["C"] != strikes["P"]:
		raise ValueError(f"Calls and Puts have different strikes: \nCalls: {strikes["C"]}\nPuts: {strikes["P"]}")

	strikes = strikes["C"]

	return strikes


def get_strikes_of_expiries(
	ticker: str,
	expiries: NDArray[np.datetime64],
	monthly: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> tuple[int, ...]:
	strikes = tuple(
		sorted(
			set.intersection(
				*[
					set(
						get_strikes_of_expiry(
							ticker=ticker,
							expiry=expiry,
							monthly=monthly,
							chunksize=chunksize,
						)
					)
					for expiry in expiries
				]
			)
		)
	)

	return strikes
