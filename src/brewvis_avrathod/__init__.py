"""Coffee-shop themed visualization helpers for pandas DataFrames."""

from .plots import (
    plot_drink_sales,
    plot_hourly_sales,
    plot_price_rating,
)

__version__ = "0.1.0"

__all__ = [
    "plot_drink_sales",
    "plot_hourly_sales",
    "plot_price_rating",
]
