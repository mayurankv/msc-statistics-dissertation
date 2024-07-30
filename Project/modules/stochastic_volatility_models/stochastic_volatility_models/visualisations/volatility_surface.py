from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objects import Figure

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.volatility_surface import QuantityMethod, PriceTypes, VolatilitySurface
from stochastic_volatility_models.src.utils.options.expiry import time_to_expiry
from stochastic_volatility_models.src.utils.options.strikes import moneyness


class SurfacePlotParameters(TypedDict):
	mid_price: bool
	time_to_expiry: bool
	moneyness: bool
	log_moneyness: bool


DEFAULT_PLOT_PARAMETERS: SurfacePlotParameters = {
	"mid_price": True,
	"time_to_expiry": True,
	"moneyness": True,
	"log_moneyness": True,
}


# TODO (@mayurankv): Prettify plot
def plot_volatility_surface(
	time: np.datetime64,
	volatility_surface: VolatilitySurface,
	quantity_method: QuantityMethod,
	plot_parameters: SurfacePlotParameters = DEFAULT_PLOT_PARAMETERS,
	*args,
	**kwargs,
) -> Figure:
	plot_parameters = DEFAULT_PLOT_PARAMETERS | plot_parameters
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
