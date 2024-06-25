from scipy import sparse
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sys import getsizeof
import numpy as np
import os
import pickle
from dash import Dash, html, dcc, callback, Output, State, Input 
from sklearn.ensemble import RandomForestClassifier
import math

variableIndices = [
    0,
    36, # Precipitation
    72, # Temp Max
    108, # Temp Min
    229, # EVI
    350, # NDVI
    471, # Lai
    615, # Hydrography
    759, # Roads
    903 # Lines
]

parameters = [
    "Precipitation (1D)",
    "Temp Max (1D)",
    "Temp Min (1D)",
    "EVI (16D)",
    "NDVI (16D)",
    "LAI (16D)",
    "Hydrography",
    "Roads",
    "Transmission Lines"
]

testX = np.load("data-demo/testX_demo.npy")
testY = np.load("data-demo/testY_demo.npy")
pred_demo = np.load("data-demo/pred_demo.npy")
print(testX.shape)

def create_figure(figIdx):
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=tuple(parameters)
    )

    curCol = 1
    curRow = 1

    for varIdx in range(1, len(variableIndices)):
        newShape = int(math.sqrt(variableIndices[varIdx]-variableIndices[varIdx-1]))
        data = testX[figIdx][variableIndices[varIdx-1]:variableIndices[varIdx]].reshape(newShape, newShape)
        fig.add_trace(
            go.Heatmap(z=data, name=parameters[varIdx-1], showscale=False), 
            row=curRow, col=curCol )

        if curCol == 3:
            curCol = 1
            curRow += 1
        else:
            curCol+=1

    fig.update_layout(autosize=False, height=1000, width=800)
    return fig

app = Dash(__name__) 

app.layout = html.Div([
    html.Div(children=[
        html.H2("Input - test X"),
        dcc.Graph(id="input-data-graph"),
    ], style={'padding':10, 'flex':1}),
    html.Div(children=[
        html.H1("Model Predictions from Testing Dataset on Random Forest Classifier"),
        html.P("Visualize Test Case Number:"),
        dcc.Slider(
            id='slider-testcase', min=0, max=1000,
            value=0, step=1, marks=None, tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.H3("Predicted"),
        html.Div(id='output-predicted'),
        html.H3("Actual"),
        html.Div(id='output-actual')
    ], style={'padding':10, 'flex':1})
], style={'display': 'flex', 'flexDirection': 'row'})

@app.callback(
    Output("input-data-graph", "figure"),
    Output("output-actual", "children"),
    Output("output-predicted", "children"),
    Input("slider-testcase", "value"))
def change_testcase(newTestcase):
    fig = create_figure(newTestcase)

    return fig, testY[newTestcase], pred_demo[newTestcase]

app.run_server(debug=True)