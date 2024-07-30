from __future__ import annotations
from typing import TYPE_CHECKING, cast
import numpy as np
from numpy.typing import NDArray
import pandas as pd
from pandas import DataFrame, Series
from loguru import logger

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying
from stochastic_volatility_models.config import MODULE_DIRECTORY
from stochastic_volatility_models.src.utils.options.expiry import time_to_expiry
from stochastic_volatility_models.src.utils.cache import np_cache
from stochastic_volatility_models.src.data.prices import DEFAULT_CHUNKSIZE
from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate


@np_cache(arg_num=2, arg_name="expiries")
def _get_dividend_yield(
	underlying: Underlying,
	time: np.datetime64,
	expiries: NDArray[np.datetime64],
	monthly: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> NDArray[np.float64]:
	logger.trace("Getting dividend yield")

	spot = underlying.price(time=time)
	reference = spot * 1000

	def get_atm_strikes(
		strike_df: DataFrame,
	) -> DataFrame:
		strike_df.index = strike_df.index.droplevel([0, 1])
		exactmatch = strike_df[strike_df.index == reference]
		if not exactmatch.empty:
			strike = exactmatch.index
		else:
			strike = upperneighbour_ind if (upperneighbour_ind := strike_df[strike_df.index > reference].index.min()) + (lowerneighbour_ind := strike_df[strike_df.index < reference].index.max()) <= 2 * reference else lowerneighbour_ind

		atm_strikes = strike_df.loc[[strike]]

		return atm_strikes

	path: str = f"{MODULE_DIRECTORY}/data/options/{underlying.ticker.lower()}.csv"
	option_prices_iter = pd.read_csv(
		path,
		index_col=[0, 1],
		chunksize=chunksize,
	)

	option_strikes = (
		pd.concat(
			[
				(
					prices := option_prices.xs(
						date_key,
						level=1,
					)
				).loc[(prices["exdate"].isin(np.datetime_as_string(expiries))) & (prices["am_settlement"] == int(monthly)), ["exdate", "cp_flag", "strike_price", "am_settlement", "best_bid", "best_offer"]]
				for option_prices in option_prices_iter
				if (date_key := np.datetime_as_string(time, unit="D")) in option_prices.index.get_level_values(level=1)
			]
		)
		.reset_index()
		.drop(labels=["am_settlement", "symbol"], axis=1)
		.set_index(keys=["exdate", "cp_flag", "strike_price"])
	)

	found_expiries = set(option_strikes.index.get_level_values(level=0).unique())
	if found_expiries != (to_find_expiries := set(np.datetime_as_string(expiries))):
		raise ValueError(f"Options could not be found. Only found {found_expiries} out of {to_find_expiries}.")

	option_strikes["Mid"] = (option_strikes["best_bid"] + option_strikes["best_offer"]) / 2
	option_strikes = option_strikes.drop(["best_bid", "best_offer"], axis=1)

	atm_strikes = option_strikes.groupby(level=[0, 1]).apply(func=get_atm_strikes)["Mid"].unstack(level=1).reset_index().set_index("exdate")
	t2x = time_to_expiry(time=time, option_expiries=expiries)
	dividend_yields = (
		-np.log(
			(
				(atm_strikes["C"] - atm_strikes["P"])
				+ (atm_strikes["strike_price"] / 1000)
				* np.exp(
					-get_risk_free_interest_rate(
						time=time,
						time_to_expiry=t2x,
					)
					* t2x
				)
			)
			/ spot
		)
		/ t2x
	)

	dividend_yields = cast(Series, dividend_yields).reindex(index=np.datetime_as_string(arr=expiries)).to_numpy()

	return dividend_yields


def get_dividend_yield(
	underlying: Underlying,
	time: np.datetime64,
	expiries: NDArray[np.datetime64],
	monthly: bool = True,
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> NDArray[np.float64]:
	_get_dividend_yield(
		underlying=underlying,
		time=time,
		expiries=np.array(list(set(expiries))),
		monthly=monthly,
		chunksize=chunksize,
	)

	return _get_dividend_yield(
		underlying=underlying,
		time=time,
		expiries=expiries,
		monthly=monthly,
		chunksize=chunksize,
	)
