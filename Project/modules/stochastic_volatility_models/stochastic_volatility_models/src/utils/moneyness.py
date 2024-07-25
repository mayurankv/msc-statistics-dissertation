from datetime import datetime
import numpy as np
from numpy.typing import NDArray

from assets.src.core.underlying import Underlying


def moneyness(
	underlying: Underlying,
	strikes: NDArray[np.int32],
	time: datetime,
	future: bool = False,
	log: bool = False,
) -> NDArray[np.float32]:
	moneyness = (underlying.get_future(time=time).price(time=time) if future else underlying.price(time=time)) / strikes
	if log:
		moneyness = np.log(moneyness)
	return moneyness
