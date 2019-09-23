from flask import Flask, render_template

import json
import plotly

import pandas as pd
import numpy as np

import plotly.graph_objs as go

import json

from sqlalchemy import create_engine

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)

    engine = create_engine("mysql+pymysql://root:123456@db/iii_project", echo=False)
    df_day = pd.read_sql_table('eur_usd_rslt2', engine)
    
    readout = df_day
    readout = readout.set_index("date")
    readout = readout.loc["2016-01-01":"2017-02-30"]
    
    graphs = [
        dict(
            data=[
                go.Candlestick(
                    x=readout.index,
                    open=readout['open_price'],
                    high=readout['high_price'],
                    low=readout['low_price'],
                    close=readout['close_price'],
                    name="K-line"
                ),                
                go.Scatter(
                    x=readout.index,
                    y=readout['ma20'],
                    name="20MA",
                    line_color='blue',
                    opacity=0.3
                )
            ],
            layout=dict(
                width=1000,
                title='Daily OHLC & MA trend chart', 
                xaxis=dict(
                    rangeslider={},
                    rangeselector= 
                    {"buttons": 
                    [    
                    {
                      "step": "month", 
                      "count": 1, 
                      "label": "1m", 
                      "stepmode": "backward"
                    }, 
                    {
                      "step": "month", 
                      "count": 6, 
                      "label": "6m", 
                      "stepmode": "backward"
                    }, 
                    {
                      "step": "year", 
                      "count": 1, 
                      "label": "YTD", 
                      "stepmode": "todate"
                    }, 
                    {
                      "step": "year", 
                      "count": 1, 
                      "label": "1y", 
                      "stepmode": "backward"
                    }, 
                    {"step": "all"}]}
                ),
                yaxis=dict(title="EUR/USD", tick0=0, dtick=0.02,)
            )
        )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layouts/index.html',
                           ids=ids,
                           graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
