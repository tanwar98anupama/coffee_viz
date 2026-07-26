"""Coffee-shop themed chart helpers built on pandas and Matplotlib."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.markers import MarkerStyle
from matplotlib.patches import Arc, Rectangle
from matplotlib.transforms import Affine2D

ESPRESSO = "#3B2417"
MOCHA = "#6F4E37"
CARAMEL = "#C9822B"
CREAM = "#F5EBDD"
FOREST = "#2F5132"
CHARCOAL = "#2B2118"

BEAN_MARKER = MarkerStyle("o", transform=Affine2D().scale(1.6, 1.0).rotate_deg(25))
CREASE_MARKER = MarkerStyle("|", transform=Affine2D().scale(1.0, 1.4).rotate_deg(25))


def _draw_mug(ax):
    """Stamp a small steaming coffee-mug watermark above the plot area, clear of any data."""
    ax.add_patch(Rectangle((0.93, 1.04), 0.05, 0.09, transform=ax.transAxes,
                            facecolor=MOCHA, edgecolor=CHARCOAL, linewidth=1.3,
                            clip_on=False, zorder=5))
    ax.add_patch(Arc((0.985, 1.085), 0.04, 0.055, theta1=-100, theta2=100,
                      transform=ax.transAxes, edgecolor=CHARCOAL, linewidth=1.5,
                      clip_on=False, zorder=5))
    for dx in (0.0, 0.02):
        ax.plot([0.943 + dx, 0.953 + dx, 0.943 + dx, 0.953 + dx], [1.14, 1.18, 1.22, 1.26],
                transform=ax.transAxes, color=CHARCOAL, linewidth=1.2, alpha=0.5,
                clip_on=False, zorder=5, solid_capstyle="round")


def _style_axis(ax, title, xlabel, ylabel):
    """Apply the shared cafe look to a single axis, plus a mug watermark."""
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
    _draw_mug(ax)


def _require_columns(df, columns):
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")


def plot_drink_sales(df, drink_col="drink", sales_col="units_sold", top_n=5):
    """Donut chart of top-selling drinks by total units sold."""
    _require_columns(df, [drink_col, sales_col])
    totals = df.copy().groupby(drink_col)[sales_col].sum().sort_values(ascending=False)
    totals = totals.head(top_n)

    fig, ax = plt.subplots(figsize=(7, 7))
    fig.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    colors = [CARAMEL if i == 0 else MOCHA for i in range(len(totals))]

    _, _, autotexts = ax.pie(
        totals.values, labels=totals.index, colors=colors, startangle=90,
        wedgeprops=dict(width=0.4, edgecolor=CREAM, linewidth=2),
        textprops=dict(color=CHARCOAL),
        autopct=lambda pct: f"{round(pct / 100 * totals.sum()):,.0f}",
        pctdistance=0.82,
    )
    for text in autotexts:
        text.set_color(CHARCOAL)
        text.set_fontsize(9)

    ax.text(0, 0, f"{totals.sum():,.0f}\nunits sold", ha="center", va="center",
             color=CHARCOAL, fontsize=16, fontweight="bold")
    ax.set_title("Top-Selling Drinks", color=CHARCOAL, fontsize=13, fontweight="bold")
    _draw_mug(ax)
    fig.tight_layout()
    return fig, ax


def plot_hourly_sales(df, hour_col="hour", sales_col="sales_usd"):
    """Line chart of sales revenue across hours, with the peak hour annotated."""
    _require_columns(df, [hour_col, sales_col])
    totals = df.copy().groupby(hour_col)[sales_col].sum().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.fill_between(totals.index, totals.values, color=MOCHA, alpha=0.15)
    ax.plot(totals.index, totals.values, color=ESPRESSO, marker=BEAN_MARKER,
             markersize=11, markerfacecolor=CARAMEL, markeredgecolor=ESPRESSO, linewidth=2)

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
    ax.scatter(data[price_col], data[rating_col], s=140, marker=BEAN_MARKER,
               color=MOCHA, edgecolor=CARAMEL, linewidth=1.5, zorder=3)
    ax.scatter(data[price_col], data[rating_col], s=70, marker=CREASE_MARKER,
               color=ESPRESSO, linewidth=1.4, zorder=4)

    for _, row in data.iterrows():
        ax.annotate(str(row[label_col]), (row[price_col], row[rating_col]),
                    xytext=(5, 5), textcoords="offset points",
                    color=CHARCOAL, fontsize=8)

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.2f}"))
    _style_axis(ax, "Price vs. Rating", "Price (USD)", "Rating")
    fig.tight_layout()
    return fig, ax
