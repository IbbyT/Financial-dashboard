#financial dashboard
import math
import pandas as pd
import datetime as dt
import numpy as np
import yfinance as yf
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import TextInput, Button, DatePicker, MultiChoice

#loading data with error handling
def load_data(ticker1, ticker2, start, end):
    try:
        df1 = yf.download(ticker1, start, end)
        df2 = yf.download(ticker2, start, end)
        return df1, df2
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()  # Return empty DataFrames on error

#plotting data with optional indicators
def plot_data(df, sync_axis=None, indicators=[]):
    gain = df.Close > df.Open
    loss = df.Open > df.Close
    width = 12 * 60 * 60 * 1000  # half day in ms

    if sync_axis is not None:
        p = figure(x_axis_type="datetime", tools="pan, wheel_zoom, box_zoom, reset, save", width=1000,
                   x_range=sync_axis)
    else:
        p = figure(x_axis_type="datetime", tools="pan, wheel_zoom, box_zoom, reset, save", width=1000)

    p.axis.major_label_orientation = math.pi / 4
    p.grid.grid_line_alpha = 0.25

    p.segment(df.index, df.High, df.index, df.Low, color="black")
    p.vbar(df.index[gain], width, df.Open[gain], df.Close[gain], fill_color="#00ff00", line_color="#00ff00")
    p.vbar(df.index[loss], width, df.Open[loss], df.Close[loss], fill_color="#ff0000", line_color="#ff0000")

    #indicators
    if "100 Day SMA" in indicators:
        df['SMA100'] = df['Close'].rolling(window=100).mean()
        p.line(df.index, df['SMA100'], color="blue", legend_label="100 Day SMA")
    
    if "30 Day SMA" in indicators:
        df['SMA30'] = df['Close'].rolling(window=30).mean()
        p.line(df.index, df['SMA30'], color="orange", legend_label="30 Day SMA")
    
    return p

#button click event
def on_button_click():
    ticker1 = stock1_text.value
    ticker2 = stock2_text.value
    start = date_picker_from.value
    end = date_picker_to.value
    indicators = indicator_choice.value

    #validation checks
    if not ticker1 or not ticker2:
        print("Please enter both stock tickers.")
        return
    if start >= end:
        print("Start date must be before end date.")
        return

    df1, df2 = load_data(ticker1, ticker2, start, end)
    
    #checking empty data
    if df1.empty or df2.empty:
        print("Error: Data could not be loaded. Check ticker symbols and date range.")
        return
    
    p1 = plot_data(df1, indicators=indicators)
    p2 = plot_data(df2, sync_axis=p1.x_range, indicators=indicators)

    #clear existing plots and add new ones
    curdoc().clear()
    curdoc().add_root(layout)
    curdoc().add_root(row(p1, p2))

#Bokeh widgets
stock1_text = TextInput(title="Stock 1", value="AAPL")
stock2_text = TextInput(title="Stock 2", value="MSFT")
date_picker_from = DatePicker(title="Start Date", value="2020-01-01", min_date="2000-01-01",
                                max_date=dt.datetime.now().strftime("%Y-%m-%d"))
date_picker_to = DatePicker(title="End Date", value="2020-02-01", min_date="2000-01-01",
                                max_date=dt.datetime.now().strftime("%Y-%m-%d"))
indicator_choice = MultiChoice(options=["100 Day SMA", "30 Day SMA", "Linear Regression Line"], value=[])

load_button = Button(label="Load Data", button_type="success")
load_button.on_click(on_button_click)

layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button)

curdoc().add_root(layout)
