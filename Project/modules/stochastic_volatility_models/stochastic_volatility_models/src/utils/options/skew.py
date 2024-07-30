from __future__ import annotations
from typing import TYPE_CHECKING, cast
import numpy as np
from pandas import DataFrame

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.volatility_surface import VolatilitySurface
from stochastic_volatility_models.src.utils.options.strikes import moneyness, find_closest_strikes


def atm_skew(
	surface: DataFrame,
	volatility_surface: VolatilitySurface,
	time: np.datetime64,
) -> DataFrame:
	indices = find_closest_strikes(
		strikes=volatility_surface.strikes,
		spot=volatility_surface.underlying.price(time=time),
	)
	atm_skews = DataFrame(
		data=[
			np.polyfit(
				x=moneyness(volatility_surface.underlying, indices, time, log=True),
				y=cast(DataFrame, surface.xs(key=expiry, level=1)).loc[indices, "Symbol"].to_numpy(),
				deg=1,
			)[0]
			for expiry in volatility_surface.expiries
		],
		index=[expiry for expiry in volatility_surface.expiries],
		columns=["Skew"],
	)

	return atm_skews
