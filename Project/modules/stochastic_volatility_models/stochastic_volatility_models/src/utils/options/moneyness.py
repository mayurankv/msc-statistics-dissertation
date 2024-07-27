from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying


def moneyness(
	underlying: Underlying,
	strikes: NDArray[np.int64],
	time: np.datetime64,
	future: bool = True,
	log: bool = False,
) -> NDArray[np.float64]:
	moneyness = (underlying.future_price(time=time) if future else underlying.price(time=time)) / strikes
	if log:
		moneyness = np.log(moneyness)
	return moneyness
