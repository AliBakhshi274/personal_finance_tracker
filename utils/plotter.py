from datetime import datetime
from pprint import pprint

import matplotlib.pyplot as plt

def plot_daily_summary(daily_data):
    dates = [datetime.strptime(str(day), "%Y-%m-%d") for day, _ in daily_data]
    totals = [total for _, total in daily_data]

    plt.figure(figsize = (10, 5))
    plt.plot(dates, totals)
    plt.xlabel("Date")
    plt.ylabel("Amount (EUR)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_monthly_summary(monthly_data):
    print(monthly_data)
    dates = [f"{int(year)}-{int(month)}" for year, month, _ in monthly_data]
    totals = [total for _, _, total in monthly_data]
    print(totals)
    plt.figure(figsize = (10, 5))
    plt.plot(dates, totals)
    plt.xlabel("Date")
    plt.ylabel("Amount (EUR)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

