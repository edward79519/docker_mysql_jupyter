from flask import Flask, render_template

import json
import plotly

import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta
import pymysql
from sqlalchemy import create_engine
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)
app.debug = True

def rpoutrange(df):
    dff = df
    colnm = ["open_price", "high_price", "low_price", "close_price"]
    for col in colnm:
        price_std = dff.describe()[col].loc["std"]
        price_mean = dff.describe()[col].loc["mean"]
        # 尋找離群值超過6個標準差的值
        flt_out = (dff[col] > price_mean + price_std*6) | (dff[col] < price_mean - price_std*6)
        flt_out_idx = dff[flt_out].index.values.astype(int)
        dff[col].iloc[flt_out_idx] = (dff[col].iloc[flt_out_idx+1].values + dff[col].iloc[flt_out_idx-1].values) / 2
    return dff

def rsv(new_df):
    rsv = []
    for i in range(len(new_df)):
        if i < 8:
            rsv.append(0)
            # print(rsv)
        else:
            highp = []
            lowp = []
            for j in range(9):
                highp.append(new_df["high_price"].iloc[i-j])
                lowp.append(new_df["low_price"].iloc[i-j])
            high_max = max(highp)
            low_min = min(lowp)
            # print(new_df["close_price"].iloc[i],high_max,low_min)
            rsv_v = 100*(new_df["close_price"].iloc[i]-low_min)/(high_max-low_min)
            rsv.append(round(rsv_v,3))
            # print(rsv)
    return rsv

def k_lst(new_df):
    k_list = []
    for i in range(len(new_df)):
        if i == 0:
            k_list.append(0)
        else:
            k_value = (2/3) * k_list[i-1] + (1/3) * new_df["rsv"].iloc[i]
            k_list.append(round(k_value,3))
    return k_list

def d_lst(new_df):
    d_list = []
    for i in range(len(new_df)):
        if i == 0:
            d_list.append(0)
        else:
            d_value = (2/3) * d_list[i-1] + (1/3) * new_df["K_value"].iloc[i]
            d_list.append(round(d_value,3))
    return d_list

def kd_cross(new_df):
    new_df["K-D"] = new_df.K_value - new_df.D_value
    new_df["delt_K"] = new_df["K_value"] - new_df["K_value"].shift(1)
    k_boln_M = (new_df["K_value"] > 80) & (new_df["D_value"] > 80)
    k_boln_m = (new_df["K_value"] < 20) & (new_df["D_value"] < 20)
    kd_x = new_df["K-D"] * new_df["K-D"].shift(1) < 0
    selout = k_boln_m & kd_x
    buyin = k_boln_M & kd_x
    tradelen = len(new_df)
    trd = [0]
    for i in range(1,tradelen):
        trd.append(trd[i-1])
        if buyin[i] == True:
            trd[i] = 100
        elif selout[i] == True:
            trd[i] = 0
    new_df["KD_tunnel"] = pd.Series(trd)

@app.route('/')
def index():
    
    engine = create_engine("mysql+pymysql://root:123456@db/iii_project", echo=False)
    readout = pd.read_sql_table('eur_usd_4hr', engine)
    readout.columns = ["trans_time", "open_price", "high_price", "low_price", "close_price"]
    df = readout

    df = rpoutrange(df)

    df["date"] = df["trans_time"].dt.date.astype(str)
    tmpdf = df.groupby(by = "date")
    df_day = pd.DataFrame(index = tmpdf.size().index)
    df_day["open_price"] = tmpdf.head(1).set_index("date")["open_price"]
    df_day["close_price"] = tmpdf.tail(1).set_index("date")["close_price"]
    df_day["high_price"] = tmpdf.max()["high_price"]
    df_day["low_price"] = tmpdf.min()["low_price"]
    df_day = df_day.reset_index()

    df_day["rsv"] = pd.Series(rsv(df_day))

    df_day["K_value"] = pd.Series(k_lst(df_day))
    df_day["D_value"] = pd.Series(d_lst(df_day))

    kd_cross(df_day)



    figdf2 = df_day
    figdf2 = figdf2.set_index("date")
    figdf2 = figdf2.loc["2016-01-01":"2017-02-30"]


    # fig2 = go.Figure()
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    fig2.add_trace(go.Scatter(
                    x=figdf2.index,
                    y=figdf2['K_value'],
                    name="K_line",
                    line_color='blue',
                    opacity=0.3),
                    secondary_y=False)

    fig2.add_trace(go.Scatter(
                    x=figdf2.index,
                    y=figdf2['D_value'],
                    name="D_line",
                    line_color='red',
                    opacity=0.3),
                    secondary_y=False)

    fig2.add_trace(go.Scatter(
                    x = figdf2.index,
                    y = [20]*len(figdf2),
                    name="KD_lowb",
                    line_color="black",
                    opacity=0.5),
                    secondary_y=False)

    fig2.add_trace(go.Scatter(
                    x = figdf2.index,
                    y = [80]*len(figdf2),
                    name="KD_upb",
                    line_color="black",
                    opacity=0.5),
                    secondary_y=False)

    fig2.add_trace(go.Scatter(
                    x = figdf2.index,
                    y=figdf2['KD_tunnel'],
                    name="KD_buysell_tunnel",
                    line_color="orange"),
                    secondary_y=False)

    fig2.add_trace(go.Candlestick(x=figdf2.index,
                    open=figdf2['open_price'],
                    high=figdf2['high_price'],
                    low=figdf2['low_price'],
                    close=figdf2['close_price'],
                    name="K-line"),
                    secondary_y=True)

    # Use date string to set xaxis range
    fig2.update_layout(title_text="Daily OHLC & KD trend chart", 
                       xaxis_rangeslider_visible=True)    
    

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layouts/index.html',
                           graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
