"""Demo script showing the three brewvis_avrathod chart functions."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from brewvis_avrathod import plot_drink_sales, plot_hourly_sales, plot_price_rating

CSV_PATH = Path(__file__).resolve().parent / "coffee_sales_sample.csv"


def main():
    df = pd.read_csv(CSV_PATH)

    fig1, _ = plot_drink_sales(df)
    fig1.suptitle("Demo: Top Drinks by Units Sold")

    fig2, _ = plot_hourly_sales(df)
    fig2.suptitle("Demo: Hourly Sales Trend")

    fig3, _ = plot_price_rating(df)
    fig3.suptitle("Demo: Price vs. Rating")

    plt.show()


if __name__ == "__main__":
    main()
