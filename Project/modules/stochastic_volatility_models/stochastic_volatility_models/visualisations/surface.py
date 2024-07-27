from typing import TypedDict
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objects import Figure

from stochastic_volatility_models.src.types.types import PriceTypes
from stochastic_volatility_models.src.core.options import QuantityMethod, VolatilitySurface
from stochastic_volatility_models.src.utils.expiry import time_to_expiry
from stochastic_volatility_models.src.utils.moneyness import moneyness


class SurfacePlotParameters(TypedDict):
	mid_price: bool
	time_to_expiry: bool
	moneyness: bool
	log_moneyness: bool


# TODO (@mayurankv): Prettify plot
def plot_volatility_surface(
	time: np.datetime64,
	volatility_surface: VolatilitySurface,
	quantity_method: QuantityMethod,
	plot_parameters: SurfacePlotParameters = {
		"mid_price": True,
		"time_to_expiry": True,
		"moneyness": True,
		"log_moneyness": True,
	},
	*args,
	**kwargs,
) -> Figure:
	x = volatility_surface.expiries if not plot_parameters["time_to_expiry"] else time_to_expiry(time=time, option_expiries=volatility_surface.expiries)
	y = volatility_surface.strikes if not plot_parameters["moneyness"] else moneyness(underlying=volatility_surface.underlying, strikes=volatility_surface.strikes, time=time, log=plot_parameters["log_moneyness"])
	price_types: list[PriceTypes] = ["Bid", "Ask"] if not plot_parameters["mid_price"] else ["Mid"]
	moneyness_title = f"{'log-' if plot_parameters["log_moneyness"] else ''}Moneyness"
	fig = go.Figure(
		data=[
			go.Surface(
				x=x,
				y=y,
				z=surface_quantities.unstack(0).to_numpy().transpose(),  # TODO (@mayurankv): Label
			)
			for surface_quantities in volatility_surface.surface_quantities(time=time, quantity_method=quantity_method, price_types=price_types, *args, **kwargs)
		],
		layout=dict(
			title="Volatility Surface",  # TODO (@mayurankv): Opacity and layout
			scene=dict(
				aspectmode="cube",
				xaxis=dict(title="Expiries" if not plot_parameters["time_to_expiry"] else "Time to Expiry (Yr)"),
				yaxis=dict(title="Strikes" if not plot_parameters["moneyness"] else moneyness_title),
				zaxis=dict(title=quantity_method.split(sep="_")[-1].title()),
			),
		),
	).update_traces(
		contours_z=dict(
			show=True,
			usecolormap=True,
			highlightcolor="limegreen",
			project_z=True,
		),
	)
	return fig