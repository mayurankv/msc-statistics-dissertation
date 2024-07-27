from typing import Callable, Literal
from pandas import DataFrame
import numpy as np


Metrics = Literal["MSE", "RMSE", "MAE"]


def mse(
	quantities_1: DataFrame,
	quantities_2: DataFrame,
) -> float:
	return ((quantities_1 - quantities_2) ** 2).values.mean()


def rmse(
	quantities_1: DataFrame,
	quantities_2: DataFrame,
) -> float:
	return np.sqrt(((quantities_1 - quantities_2) ** 2).values.mean())


def mae(
	quantities_1: DataFrame,
	quantities_2: DataFrame,
) -> float:
	return np.abs((quantities_1 - quantities_2).values).mean()


METRICS: dict[Metrics, Callable[[DataFrame, DataFrame], float]] = {
	"RMSE": rmse,
	"MAE": mae,
}
