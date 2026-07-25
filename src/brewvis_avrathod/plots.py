"""Coffee-shop themed chart helpers built on pandas and Matplotlib."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

ESPRESSO = "#3B2417"
MOCHA = "#6F4E37"
CARAMEL = "#C9822B"
CREAM = "#F5EBDD"
FOREST = "#2F5132"
CHARCOAL = "#2B2118"


def _style_axis(ax, title, xlabel, ylabel):
    """Apply the shared cafe look to a single axis."""
    ax.set_facecolor(CREAM)
    ax.figure.set_facecolor(CREAM)
    ax.set_title(title, color=CHARCOAL, fontsize=13, fontweight="bold")
    ax.set_xlabel(xlabel, color=CHARCOAL)
    ax.set_ylabel(ylabel, color=CHARCOAL)
    ax.tick_params(colors=CHARCOAL)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(CHARCOAL)
    ax.spines["bottom"].set_color(CHARCOAL)
    ax.grid(True, axis="y", color=MOCHA, alpha=0.15)


def _require_columns(df, columns):
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")


def plot_drink_sales(df, drink_col="drink", sales_col="units_sold", top_n=5):
    """Bar chart of top-selling drinks by total units sold."""
    _require_columns(df, [drink_col, sales_col])
    totals = df.copy().groupby(drink_col)[sales_col].sum().sort_values(ascending=False)
    totals = totals.head(top_n)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = [CARAMEL if i == 0 else MOCHA for i in range(len(totals))]
    bars = ax.bar(totals.index, totals.values, color=colors, edgecolor=ESPRESSO)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:,.0f}",
                 ha="center", va="bottom", color=CHARCOAL, fontsize=9)

    _style_axis(ax, "Top-Selling Drinks", "Drink", "Units Sold")
    fig.tight_layout()
    return fig, ax


def plot_hourly_sales(df, hour_col="hour", sales_col="sales_usd"):
    """Line chart of sales revenue across hours, with the peak hour annotated."""
    _require_columns(df, [hour_col, sales_col])
    totals = df.copy().groupby(hour_col)[sales_col].sum().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(totals.index, totals.values, color=ESPRESSO, marker="o",
             markerfacecolor=CARAMEL, markeredgecolor=ESPRESSO, linewidth=2)

    peak_hour = totals.idxmax()
    peak_value = totals.max()
    ax.annotate(f"Peak: ${peak_value:,.0f}", xy=(peak_hour, peak_value),
                xytext=(0, 12), textcoords="offset points", ha="center",
                color=FOREST, fontweight="bold")

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    _style_axis(ax, "Sales by Hour of Day", "Hour", "Sales (USD)")
    fig.tight_layout()
    return fig, ax


def plot_price_rating(df, price_col="price", rating_col="rating", label_col="drink"):
    """Scatter plot comparing drink price to customer rating."""
    _require_columns(df, [price_col, rating_col, label_col])
    data = df.copy()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(data[price_col], data[rating_col], s=90, color=MOCHA,
               edgecolor=CARAMEL, linewidth=1.5, zorder=3)

    for _, row in data.iterrows():
        ax.annotate(str(row[label_col]), (row[price_col], row[rating_col]),
                    xytext=(5, 5), textcoords="offset points",
                    color=CHARCOAL, fontsize=8)

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.2f}"))
    _style_axis(ax, "Price vs. Rating", "Price (USD)", "Rating")
    fig.tight_layout()
    return fig, ax
