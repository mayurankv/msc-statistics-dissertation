class Coefficients:
	def __init__(
		self,
		noise: list[float] = [],
		observations: list[float] = [1.0],
		squared_residuals: list[float] = [1.0],
		conditional_variances: list[float] = [],
	) -> None:
		self.noise = noise
		self.observations = observations
		self.squared_residuals = squared_residuals
		self.conditional_variances = conditional_variances
		# ma
		# ar
		# ex
		# ex_ma


class MultivariateCrossCoefficients:
	def __init__(
		self,
	) -> None:
		self.observations: list[float] = []


class MultivariateCoefficients:
	def __init__(
		self,
	) -> None:
		pass


class TimeSeries:
	def __init__(
		self,
		coefficients: Coefficients | None = None,
	) -> None:
		if coefficients is not None:
			self.coefficients = coefficients
		else:
			self.coefficients = Coefficients()

	def estimate(
		self,
	):
		pass

	def forecast(
		self,
	):
		pass

	def simulate(
		self,
	):
		pass


class MultivariateTimeSeries:
	def __init__(
		self,
		coefficients: MultivariateCoefficients | None = None,
	) -> None:
		if coefficients is not None:
			self.coefficients = coefficients
		else:
			self.coefficients = MultivariateCoefficients()

	def estimate(
		self,
	):
		pass

	def forecast(
		self,
	):
		pass

	def simulate(
		self,
	):
		pass
