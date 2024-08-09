from pandas import DataFrame
import numpy as np
from typing import cast
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import plotly.graph_objects as go

from stochastic_volatility_models.src.core.pricing_models import PricingModel
from stochastic_volatility_models.src.core.underlying import Underlying
from stochastic_volatility_models.src.core.volatility_surface import VolatilitySurface
from stochastic_volatility_models.visualisations.volatility_surface import plot_volatility_surface
from stochastic_volatility_models.src.utils.options.expiry import time_to_expiry
from stochastic_volatility_models.src.utils.options.strikes import find_closest_strikes


def get_slider(
	traces,
	volatility_surface,
	t2x,
):
	steps = []
	for idx in range(len(volatility_surface.expiries)):
		step = dict(
			method="update",
			args=[
				{"visible": [j // traces == idx for j in range(len(volatility_surface.expiries) * traces)]},  # Group visibility by expiry
				{"title": f"T: {volatility_surface.expiries[idx]} - t2x: {t2x[idx]}"},
			],
			label=str(volatility_surface.expiries[idx]),
		)
		steps.append(step)

	sliders = [dict(active=0, currentvalue={"prefix": "Expiry: "}, pad={"t": 50}, steps=steps)]
	return sliders


class Notebook:
	def __init__(
		self,
		model=None,
		to_fit=False,
	) -> None:
		self.model = model
		self.to_fit = to_fit and model is not None
		self.ticker = "SPX"
		self.vol_ticker = "VIX"
		self.spx = Underlying(self.ticker)
		self.vix = Underlying(self.vol_ticker)
		self.pricing_model = PricingModel("Black-76 EMM" if self.model is not None else "Black-Scholes-Merton")
		self.empirical_pricing_model = PricingModel()
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
		if self.model is not None:
			return self.spx_vs.model_price(time=self.time, model=self.model)
		else:
			return self.spx_vs.empirical_price(time=self.time)

	def plot_surfaces(
		self,
		out_the_money=True,
		call=None,
	) -> None:
		if self.model is not None:
			fig = plot_volatility_surface(
				time=self.time,
				volatility_surface=self.spx_vs,
				quantity_method="model_price",
				model=self.model,
				plot_parameters={"moneyness": False, "time_to_expiry": False, "log_moneyness": False, "mid_price": True},
				out_the_money=out_the_money,
				call=call,
			)
		else:
			fig = plot_volatility_surface(
				time=self.time,
				volatility_surface=self.spx_vs,
				quantity_method="empirical_price",
				plot_parameters={"moneyness": False, "time_to_expiry": False, "log_moneyness": False, "mid_price": True},
				out_the_money=out_the_money,
				call=call,
			)
		fig.show()

		if self.model is not None:
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
		else:
			fig = plot_volatility_surface(
				time=self.time,
				volatility_surface=self.spx_vs,
				quantity_method="empirical_pricing_implied_volatility",
				pricing_model=self.pricing_model,
				plot_parameters={"moneyness": False, "time_to_expiry": False, "log_moneyness": False, "mid_price": True},
				out_the_money=out_the_money,
				call=call,
			)
		fig.show()

	def plot_put_call_iv(
		self,
		plot_closeup=False,
	) -> None:
		volatility_surface = self.spx_vs

		if self.model is not None:
			surface_c = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="model_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=True,
				call=True,
				pricing_model=self.pricing_model,
				model=self.model,
			)[0]
			surface_p = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="model_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=True,
				call=False,
				pricing_model=self.pricing_model,
				model=self.model,
			)[0]
		else:
			surface_c = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="empirical_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=True,
				call=True,
				pricing_model=self.pricing_model,
			)[0]
			surface_p = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="empirical_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=True,
				call=False,
				pricing_model=self.pricing_model,
			)[0]

		spot = volatility_surface.underlying.price(time=self.time)
		t2x = time_to_expiry(self.time, volatility_surface.expiries)
		indices = find_closest_strikes(
			strikes=volatility_surface.strikes,
			spot=volatility_surface.underlying.price(time=self.time),
		)

		fig = go.Figure()

		for idx, expiry in enumerate(volatility_surface.expiries):
			if not plot_closeup:
				fig.add_trace(
					trace=go.Scatter(
						visible=idx == 0,  # Only the first trace is visible initially
						x=volatility_surface.strikes,
						y=cast(DataFrame, surface_c.xs(key=expiry, level=1)).loc[volatility_surface.strikes, "Symbol"].values,
						name=f"T: {expiry}",
						mode="lines+markers",
						line=dict(color="blue"),
						marker=dict(color="blue"),
					)
				)
				fig.add_trace(
					trace=go.Scatter(
						visible=idx == 0,  # Only the first trace is visible initially
						x=volatility_surface.strikes,
						y=cast(DataFrame, surface_p.xs(key=expiry, level=1)).loc[volatility_surface.strikes, "Symbol"].values,
						name=f"T: {expiry}",
						mode="lines+markers",
						line=dict(color="red"),
						marker=dict(color="red"),
					)
				)
			fig.add_trace(
				trace=go.Scatter(
					visible=idx == 0,  # Only the first trace is visible initially
					x=indices,
					y=cast(DataFrame, surface_c.xs(key=expiry, level=1)).loc[indices, "Symbol"].values,
					name=f"T: {expiry}",
					mode="markers" if not plot_closeup else "lines+markers",
					marker=dict(color="purple"),
					line=dict(color="purple"),
				)
			)
			fig.add_trace(
				trace=go.Scatter(
					visible=idx == 0,  # Only the first trace is visible initially
					x=indices,
					y=cast(DataFrame, surface_p.xs(key=expiry, level=1)).loc[indices, "Symbol"].values,
					name=f"T: {expiry}",
					mode="markers" if not plot_closeup else "lines+markers",
					marker=dict(color="orange"),
					line=dict(color="orange"),
				)
			)
			fig.add_vline(
				x=spot,
				line_dash="dash",
				line_color="green",
			)

		fig.update_layout(
			sliders=get_slider(
				traces=4 - 2 * plot_closeup,
				volatility_surface=volatility_surface,
				t2x=t2x,
			),
			showlegend=False,
			title_text=f"T: {volatility_surface.expiries[0]} - t2x: {t2x[0]}",
		)

		fig.show()

	def plot_put_call_iv_old(
		self,
	) -> None:
		volatility_surface = self.spx_vs

		if self.model is not None:
			surface_c = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="model_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=True,
				call=True,
				pricing_model=self.pricing_model,
				model=self.model,
			)[0]
			surface_p = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="model_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=True,
				call=False,
				pricing_model=self.pricing_model,
				model=self.model,
			)[0]
		else:
			surface_c = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="empirical_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=True,
				call=True,
				pricing_model=self.pricing_model,
			)[0]
			surface_p = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="empirical_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=True,
				call=False,
				pricing_model=self.pricing_model,
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
		out_the_money=True,
		call=None,
	) -> None:
		volatility_surface = self.spx_vs

		if self.model is not None:
			surface = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="model_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=out_the_money,
				call=call,
				pricing_model=self.pricing_model,
				model=self.model,
			)[0]
		else:
			surface = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="empirical_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=out_the_money,
				call=call,
				pricing_model=self.pricing_model,
			)[0]

		spot = volatility_surface.underlying.price(time=self.time)
		t2x = time_to_expiry(self.time, volatility_surface.expiries)
		indices = find_closest_strikes(
			strikes=volatility_surface.strikes,
			spot=volatility_surface.underlying.price(time=self.time),
		)

		fig = go.Figure()

		for idx, expiry in enumerate(volatility_surface.expiries):
			cs = CubicSpline(
				x=indices,
				y=cast(DataFrame, surface.xs(key=expiry, level=1)).loc[indices, "Symbol"].values,
				bc_type="natural",
			)

			x = np.linspace(indices.min(), indices.max(), 100)
			slope, intercept = np.polyfit(indices, cast(DataFrame, surface.xs(key=expiry, level=1)).loc[indices, "Symbol"].to_numpy(), 1)

			if not plot_closeup:
				fig.add_trace(
					trace=go.Scatter(
						visible=idx == 0,  # Only the first trace is visible initially
						x=volatility_surface.strikes,
						y=cast(DataFrame, surface.xs(key=expiry, level=1)).loc[volatility_surface.strikes, "Symbol"].values,
						name=f"T: {expiry}",
						mode="lines+markers",
						line=dict(color="blue"),
						marker=dict(color="blue"),
					)
				)
			fig.add_trace(
				trace=go.Scatter(
					visible=idx == 0,  # Only the first trace is visible initially
					x=indices,
					y=cast(DataFrame, surface.xs(key=expiry, level=1)).loc[indices, "Symbol"].values,
					name=f"T: {expiry}",
					mode="lines+markers",
					line=dict(color="red"),
					marker=dict(color="red"),
				)
			)
			fig.add_trace(
				trace=go.Scatter(
					visible=idx == 0,  # Only the first trace is visible initially
					x=[spot],
					y=[cs(spot)],
					name=f"T: {expiry}",
					mode="markers",
					marker=dict(color="darkgreen"),
				)
			)
			fig.add_trace(
				trace=go.Scatter(
					visible=idx == 0,  # Only the first trace is visible initially
					x=x,
					y=slope * x + intercept,
					name=f"T: {expiry}",
					mode="lines",
					line=dict(color="orange"),
				)
			)
			fig.add_trace(
				trace=go.Scatter(
					visible=idx == 0,  # Only the first trace is visible initially
					x=x,
					y=cs(x),
					name=f"T: {expiry}",
					mode="lines",
					line=dict(color="purple"),
				)
			)
			fig.add_vline(
				x=spot,
				line_dash="dash",
				line_color="green",
			)

		fig.update_layout(
			sliders=get_slider(
				traces=5 - plot_closeup,
				volatility_surface=volatility_surface,
				t2x=t2x,
			),
			showlegend=False,
			title_text=f"T: {volatility_surface.expiries[0]} - t2x: {t2x[0]}",
		)

		fig.show()

	def plot_iv_old(
		self,
		plot_closeup=False,
		out_the_money=True,
		call=None,
	) -> None:
		volatility_surface = self.spx_vs

		if self.model is not None:
			surface = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="model_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=out_the_money,
				call=call,
				pricing_model=self.pricing_model,
				model=self.model,
			)[0]
		else:
			surface = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="empirical_pricing_implied_volatility",
				price_types=["Mid"],
				out_the_money=out_the_money,
				call=call,
				pricing_model=self.pricing_model,
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
		out_the_money=True,
		call=None,
	) -> None:
		volatility_surface = self.spx_vs

		if self.model is not None:
			surface = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="model_price",
				price_types=["Mid"],
				out_the_money=out_the_money,
				call=call,
				model=self.model,
			)[0]
		else:
			surface = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="empirical_price",
				price_types=["Mid"],
				out_the_money=out_the_money,
				call=call,
			)[0]

		spot = volatility_surface.underlying.price(time=self.time)
		t2x = time_to_expiry(self.time, volatility_surface.expiries)
		indices = find_closest_strikes(
			strikes=volatility_surface.strikes,
			spot=volatility_surface.underlying.price(time=self.time),
			n=8,
		)

		fig = go.Figure()

		for idx, expiry in enumerate(volatility_surface.expiries):
			if not plot_closeup:
				fig.add_trace(
					trace=go.Scatter(
						visible=idx == 0,  # Only the first trace is visible initially
						x=volatility_surface.strikes,
						y=cast(DataFrame, surface.xs(key=expiry, level=1)).loc[volatility_surface.strikes, "Symbol"].values,
						name=f"T: {expiry}",
						mode="lines+markers",
						line=dict(color="blue"),
						marker=dict(color="blue"),
					)
				)
			else:
				fig.add_trace(
					trace=go.Scatter(
						visible=idx == 0,  # Only the first trace is visible initially
						x=indices,
						y=cast(DataFrame, surface.xs(key=expiry, level=1)).loc[indices, "Symbol"].values,
						name=f"T: {expiry}",
						mode="lines+markers",
						line=dict(color="blue"),
						marker=dict(color="blue"),
					)
				)
			fig.add_vline(
				x=spot,
				line_dash="dash",
				line_color="green",
			)

		fig.update_layout(
			sliders=get_slider(
				traces=1,
				volatility_surface=volatility_surface,
				t2x=t2x,
			),
			showlegend=False,
			title_text=f"T: {volatility_surface.expiries[0]} - t2x: {t2x[0]}",
		)

		fig.show()

	def plot_price_old(
		self,
		plot_closeup=False,
		out_the_money=True,
		call=None,
	) -> None:
		volatility_surface = self.spx_vs

		if self.model is not None:
			surface = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="model_price",
				price_types=["Mid"],
				out_the_money=out_the_money,
				call=call,
				model=self.model,
			)[0]
		else:
			surface = volatility_surface.surface_quantities(
				time=self.time,
				quantity_method="empirical_price",
				price_types=["Mid"],
				out_the_money=out_the_money,
				call=call,
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
		skew_weight=0.0,
		vol_weight=0.0,
	) -> dict:
		if self.to_fit and self.model is not None:
			parameters: dict = self.model.fit(
				index_volatility_surface=self.spx_vs,
				volatility_index_volatility_surface=self.vix_vs,
				time=self.time,
				empirical_pricing_model=self.empirical_pricing_model,
				model_pricing_model=self.pricing_model,
				weights={
					"volatility_index": vol_weight,
					"skew": skew_weight,
				},
			)

			return parameters
		else:
			return {}

	def plot_paths(
		self,
		simulation_length=1,
		num_paths=2**14,
		seed=None,
	) -> None:
		if self.model is not None:
			price_process, variance_process = self.model.simulate_path(
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
