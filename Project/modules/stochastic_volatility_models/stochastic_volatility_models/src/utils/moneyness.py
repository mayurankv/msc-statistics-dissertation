from datetime import datetime

from stochastic_volatility_models.src.core.options import Option
from assets.src.core.underlying import Underlying
import numpy as np
from numpy.typing import NDArray


def moneyness(
	underlying: Underlying,
	strike: NDArray[np.int32],
	time: datetime,
	future: bool = False,
	log: bool = False,
) -> NDArray[np.float32]:
	moneyness = (underlying.get_future(time=time).price(time=time) if future else underlying.price(time=time)) / strike
	if log:
		moneyness = np.log(moneyness)
	return moneyness


def option_moneyness(
	option: Option,
	time: datetime,
	future: bool = False,
	log: bool = False,
) -> float:
	return moneyness(
		underlying=option.underlying,
		strike=np.array([option.parameters["strike"]]),
		time=time,
		future=future,
		log=log,
	)[0]
