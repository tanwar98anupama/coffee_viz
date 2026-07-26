# brewvis-avrathod

A small coffee-shop themed visualization package that wraps common pandas and Matplotlib operations so you can create café-styled charts with very little code.

## Features

- Three focused chart functions: drink popularity, hourly sales trend, and price-vs-rating
- Consistent coffee-shop color palette (espresso, mocha, caramel, cream, forest, charcoal)
- Returns plain Matplotlib `(fig, ax)` objects — no hidden state, no `plt.show()` calls
- Never mutates your input DataFrame
- Only two dependencies: `pandas` and `matplotlib`

## Installation

```bash
pip install brewvis-avrathod
```

For local development, from the repository root:

```bash
pip install -e .
```

## Quick Start

```python
import pandas as pd
import matplotlib.pyplot as plt

from brewvis_avrathod import plot_drink_sales

df = pd.read_csv("examples/coffee_sales_sample.csv")
plot_drink_sales(df)
plt.show()
```

## Function Reference

### `plot_drink_sales(df, drink_col="drink", sales_col="units_sold", top_n=5)`
Groups units sold by drink, sorts descending, and shows the top `top_n` drinks as a donut
chart. The top seller is highlighted in caramel. Returns `(fig, ax)`.

### `plot_hourly_sales(df, hour_col="hour", sales_col="sales_usd")`
Groups revenue by hour and plots a line chart with markers. The peak-sales hour is
annotated, and the y-axis is formatted as US dollars. Returns `(fig, ax)`.

### `plot_price_rating(df, price_col="price", rating_col="rating", label_col="drink")`
Scatter plot of price versus rating with each point labeled by drink name. The x-axis is
formatted as US dollars. Returns `(fig, ax)`.

All three functions validate that required columns exist and raise a `ValueError` with a
clear message if a column is missing. None of them modify the input DataFrame or fill/alter
missing values.

## Example Dataset

`examples/coffee_sales_sample.csv` contains synthetic, simulated sample data (not real
business data) for a handful of drinks across a single day, useful for demonstrating all
three chart functions.

Run the demo:

```bash
python examples/demo.py
```

## Development and Build Commands

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install build twine

rm -rf build dist src/*.egg-info
python -m build
python -m twine check dist/*
```

## TestPyPI Instructions

Upload to TestPyPI (requires your own TestPyPI API token, entered at the upload prompt —
never store it in this repository):

```bash
python -m twine upload --repository testpypi dist/*
```

Install from TestPyPI (the extra index is needed so dependencies like pandas and
Matplotlib can still be found on regular PyPI):

```bash
python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  brewvis-avrathod
```

## License

MIT License. See [LICENSE](LICENSE) for details.
