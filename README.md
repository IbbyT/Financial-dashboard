# Financial Dashboard

This Python script creates an interactive financial dashboard for visualizing stock data using Bokeh. It allows users to compare the price movements of two stocks and overlay technical indicators on the charts.

## Features

- **Compare Stocks:** Visualize price data for two different stocks side by side.
- **Interactive Plots:** Use Bokeh's interactive plots to zoom, pan, and save charts.
- **Technical Indicators:** Optionally overlay 30-day and 100-day Simple Moving Averages (SMA) on the charts.
- **Custom Date Range:** Select a custom date range for the data visualization.

## Requirements

- Python 3.x
- `pandas`
- `numpy`
- `yfinance`
- `bokeh`

You can install the required packages using pip:

```bash
pip install pandas numpy yfinance bokeh
```

## Usage
1. Run the Application:
   ```bash
   bokeh serve --show financial_dashboard.py
2. Interactive Widgets:
- Stock 1 and Stock 2: Enter the ticker symbols for the stocks you want to compare (e.g., AAPL and MSFT).
- Start Date and End Date: Select the date range for the data.
- Indicators: Choose technical indicators to display on the charts (e.g., 100-day SMA, 30-day SMA).

3. View Data:
- Click the "Load Data" button to update the plots with the selected stocks, date range, and indicators.

## Code Overview
- Data Loading: Retrieves historical stock data using yfinance and handles errors during data loading.
- Plotting Data: Creates candlestick charts with optional technical indicators using Bokeh.
- Button Click Event: Handles user interactions, validates inputs, and updates plots based on user selections.
- Bokeh Widgets: Provides interactive widgets for user input and chart customization.
