from pandas import DataFrame
import numpy as np
from typing import cast
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

from stochastic_volatility_models.src.core.pricing_models import PricingModel
from stochastic_volatility_models.src.core.underlying import Underlying
from stochastic_volatility_models.src.core.volatility_surface import VolatilitySurface
from stochastic_volatility_models.visualisations.volatility_surface import plot_volatility_surface
from stochastic_volatility_models.src.utils.options.expiry import time_to_expiry
from stochastic_volatility_models.src.utils.options.strikes import find_closest_strikes


class Notebook:
	def __init__(
		self,
		model,
	) -> None:
		self.model = model
		self.ticker = "SPX"
		self.spx = Underlying(self.ticker)
		self.vix = Underlying("VIX")
		self.pricing_model = PricingModel("Black-76 EMM")  # "Black-76 EMM"
		self.time = np.datetime64("2022-03-03")
		expiries = np.array(
			# ["2022-03-04", "2022-03-09", "2022-03-11", "2022-03-18", "2022-03-23", "2022-03-25", "2022-03-30", "2022-03-31", "2022-04-01", "2022-04-08", "2022-04-14", "2022-04-22", "2022-04-29", "2022-05-20", "2022-05-31", "2022-06-17", "2022-06-30", "2022-07-15", "2022-07-29", "2022-08-31"], dtype=np.datetime64
			["2022-03-09", "2022-03-11", "2022-03-18", "2022-03-23", "2022-03-25", "2022-03-30", "2022-03-31", "2022-04-01", "2022-04-08", "2022-04-14", "2022-04-22", "2022-04-29", "2022-05-20", "2022-05-31", "2022-06-17", "2022-06-30", "2022-07-15", "2022-07-29", "2022-08-31"],
			dtype=np.datetime64,
		)

		strikes = np.array(
			[
				2200,
				2400,
				2600,
				2800,
				3000,
				3200,
				3400,
				3500,
				3600,
				3700,
				3800,
				3850,
				3900,
				3950,
				3975,
				4000,
				4025,
				4040,
				4050,
				4060,
				4070,
				4075,
				4080,
				4090,
				4100,
				4110,
				4120,
				4125,
				4130,
				4140,
				4150,
				4160,
				4170,
				4175,
				4180,
				4190,
				4200,
				4210,
				4220,
				4225,
				4230,
				4240,
				4250,
				4260,
				4270,
				4275,
				4280,
				4290,
				4300,
				4310,
				4320,
				4325,
				4330,
				4340,
				4350,
				4360,
				4370,
				4375,
				4380,
				4390,
				4400,
				4410,
				4420,
				4425,
				4430,
				4440,
				4450,
				4460,
				4470,
				4475,
				4480,
				4490,
				4500,
				4510,
				4525,
				4550,
				4600,
				4650,
				4700,
				4800,
				5000,
				5200,
				5400,
			]
		)
		self.spx_vs = VolatilitySurface(
			underlying=self.spx,
			expiries=expiries,
			strikes=strikes,
			monthly=False,
		)

		expiries = np.array(["2022-03-09", "2022-03-23", "2022-03-30", "2022-04-06"], dtype=np.datetime64)

		strikes = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32.5, 35, 37.5, 40, 42.5, 45, 47.5, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])
		self.vix_vs = VolatilitySurface(
			underlying=self.vix,
			expiries=expiries,
			strikes=strikes,
			monthly=False,
		)

	def spx_price(
		self,
	) -> DataFrame:
		return self.spx_vs.model_price(time=self.time, model=self.model)

	def plot_surfaces(
		self,
		out_the_money=True,
		call=None,
	) -> None:
		fig = plot_volatility_surface(
			time=self.time,
			volatility_surface=self.spx_vs,
			quantity_method="model_price",
			model=self.model,
			plot_parameters={"moneyness": False, "time_to_expiry": False, "log_moneyness": False, "mid_price": True},
			out_the_money=out_the_money,
			call=call,
		)
		fig.show()

		fig = plot_volatility_surface(
			time=self.time,
			volatility_surface=self.spx_vs,
			quantity_method="model_pricing_implied_volatility",
			pricing_model=self.pricing_model,
			model=self.model,
			plot_parameters={"moneyness": False, "time_to_expiry": False, "log_moneyness": False, "mid_price": True},
			out_the_money=out_the_money,
			call=call,
		)
		fig.show()

	def plot_put_call_iv(
		self,
	) -> None:
		volatility_surface = self.spx_vs

		surface_c = volatility_surface.surface_quantities(
			time=self.time,
			quantity_method="model_pricing_implied_volatility",
			price_types=["Mid"],
			out_the_money=True,
			call=True,
			pricing_model=self.pricing_model,
			model=self.model,
			num_paths=2**16,
		)[0]
		surface_p = volatility_surface.surface_quantities(
			time=self.time,
			quantity_method="model_pricing_implied_volatility",
			price_types=["Mid"],
			out_the_money=True,
			call=False,
			pricing_model=self.pricing_model,
			model=self.model,
			num_paths=2**16,
		)[0]
		for expiry in volatility_surface.expiries:
			print(f"T: {expiry}")
			indices = find_closest_strikes(
				strikes=volatility_surface.strikes,
				spot=volatility_surface.underlying.price(time=self.time),
			)
			plt.plot(volatility_surface.strikes, cast(DataFrame, surface_c.xs(key=expiry, level=1)).loc[volatility_surface.strikes, "Symbol"].values, linestyle=None, marker="x")
			plt.plot(indices, cast(DataFrame, surface_c.xs(key=expiry, level=1)).loc[indices, "Symbol"].values, linestyle=None, marker="x", color="red")
			plt.plot(volatility_surface.strikes, cast(DataFrame, surface_p.xs(key=expiry, level=1)).loc[volatility_surface.strikes, "Symbol"].values, linestyle=None, marker="x", color="blue")
			plt.plot(indices, cast(DataFrame, surface_p.xs(key=expiry, level=1)).loc[indices, "Symbol"].values, linestyle=None, marker="x", color="orange")
			plt.show()

	def plot_iv(
		self,
		plot_closeup=False,
	) -> None:
		volatility_surface = self.spx_vs

		surface = volatility_surface.surface_quantities(
			time=self.time,
			quantity_method="model_pricing_implied_volatility",
			price_types=["Mid"],
			out_the_money=True,
			call=None,
			pricing_model=self.pricing_model,
			model=self.model,
			num_paths=2**16,
		)[0]
		t2x = time_to_expiry(self.time, volatility_surface.expiries)

		for i, expiry in enumerate(volatility_surface.expiries):
			print(f"T: {expiry}\nt2x: {t2x[i]}")
			indices = find_closest_strikes(
				strikes=volatility_surface.strikes,
				spot=volatility_surface.underlying.price(time=self.time),
			)
			# print(indices)
			cs = CubicSpline(
				x=indices,
				y=cast(DataFrame, surface.xs(key=expiry, level=1)).loc[indices, "Symbol"].values,
				bc_type="natural",
			)
			x = np.linspace(indices.min(), indices.max(), 100)
			s, i = np.polyfit(indices, cast(DataFrame, surface.xs(key=expiry, level=1)).loc[indices, "Symbol"].to_numpy(), 1)

			spot = volatility_surface.underlying.price(time=self.time)
			if plot_closeup:
				plt.plot(volatility_surface.strikes, cast(DataFrame, surface.xs(key=expiry, level=1)).loc[volatility_surface.strikes, "Symbol"].values, linestyle=None, marker="x")
				plt.plot(indices, cast(DataFrame, surface.xs(key=expiry, level=1)).loc[indices, "Symbol"].values, linestyle=None, marker="x", color="red")
				plt.plot(x, s * x + i)
				plt.plot(x, cs(x))
				plt.plot(spot, cs(spot), color="orange", marker="o")
				plt.gca().set_xlim(4300, 4400)
				lims = np.array([s * 4300 + i, s * 4400 + i])
				plt.gca().set_ylim(lims.min(), lims.max())
				plt.show()

			plt.plot(volatility_surface.strikes, cast(DataFrame, surface.xs(key=expiry, level=1)).loc[volatility_surface.strikes, "Symbol"].values, linestyle=None, marker="x")
			plt.plot(indices, cast(DataFrame, surface.xs(key=expiry, level=1)).loc[indices, "Symbol"].values, linestyle=None, marker="x", color="red")
			plt.plot(x, s * x + i)
			plt.plot(x, cs(x))
			plt.plot(spot, cs(spot), color="orange", marker="o")
			plt.show()

	def plot_price(
		self,
		plot_closeup=False,
	) -> None:
		volatility_surface = self.spx_vs

		surface = volatility_surface.surface_quantities(
			time=self.time,
			quantity_method="model_price",
			price_types=["Mid"],
			out_the_money=True,
			call=None,
			model=self.model,
		)[0]
		spot = volatility_surface.underlying.price(time=self.time)
		for expiry in volatility_surface.expiries:
			print(f"T: {expiry}")

			if plot_closeup:
				plt.plot(volatility_surface.strikes, cast(DataFrame, surface.xs(key=expiry, level=1)).loc[volatility_surface.strikes, "Symbol"].values, linestyle=None, marker="x")
				plt.axvline(spot, color="orange", linestyle="dashed")
				plt.gca().set_xlim(4300, 4400)
				plt.show()

			plt.plot(volatility_surface.strikes, cast(DataFrame, surface.xs(key=expiry, level=1)).loc[volatility_surface.strikes, "Symbol"].values, linestyle=None, marker="x")
			plt.axvline(spot, color="orange", linestyle="dashed")
			plt.show()

	def fit(
		self,
		skew_weight=0,
		vol_weight=0,
	) -> dict:
		parameters: dict = self.model.fit(
			index_volatility_surface=self.spx_vs,
			volatility_index_volatility_surface=self.vix_vs,
			time=self.time,
			pricing_model=self.pricing_model,
			weights={
				"volatility_index": vol_weight,
				"skew": skew_weight,
			},
		)

		return parameters

	def plot_paths(
		self,
		simulation_length=1,
		num_paths=2**14,
		seed=None,
	) -> None:
		price_process, variance_process = self.model.simulate(
			underlying=self.spx,
			time=self.time,
			simulation_length=simulation_length,
			num_paths=num_paths,
			monthly=False,
			seed=seed,
		)

		DataFrame(price_process.T).plot(legend=False)
		plt.show()

		plt.plot(price_process[0])
		plt.show()

		DataFrame(variance_process.T).plot(legend=False)
		plt.show()

		plt.plot(variance_process[0])
		plt.show()
