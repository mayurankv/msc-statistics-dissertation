from .base_classes import TimeSeries


class MovingAverageProcess(TimeSeries):
	def __init__(
		self,
		ma_order: int,
		**kwargs,
	) -> None:
		super(MovingAverageProcess, self).__init__(**kwargs)
		if ma_order <= 0:
			raise ValueError("Moving Average order must be positive")
		self.ma_order = ma_order
		self.coefficients = {"m"}
