from scipy import sparse
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sys import getsizeof
import numpy as np
import os
from dash import Dash, html, dcc, callback, Output, State, Input

directory = r"D:\Users\xubil\OneDrive\Documents\Wildfires Data NPZ"
data = {}
processed = {}
max_col = 4 # Dashboard 

def change_zoom(x_min, x_max, y_min, y_max):
    ratio_y, ratio_x = (y_max-y_min)/36400, (x_max-x_min)/59700
    

    for subdir in data:
        processed[subdir] = {}

        for filename in data[subdir]:

            data_process = data[subdir][filename][y_min:y_max, x_min:x_max] # To csc speeds up processing

            N, M = data_process.shape
            s, t = int(400*ratio_y), int(400*ratio_x)          # decimation factors for y and x directions
            T = sparse.csc_matrix((np.ones((M,)), np.arange(M), np.r_[np.arange(0, M, t), M]), (M, (M-1) // t + 1))
            S = sparse.csr_matrix((np.ones((N,)), np.arange(N), np.r_[np.arange(0, N, s), N]), ((N-1) // s + 1, N))
            result = S @ data_process @ T     # downsample by binning into s x t rectangles
            processed[subdir][filename] = result.todense() 
    
    return processed

def create_figure(target):
    total = len(processed[target])
    n_row = int(total/max_col if total % max_col == 0 else total/max_col+1)
    # print(target)
    # print(n_row)

    fig = make_subplots(
        rows=n_row, cols=4, 
        start_cell="top-left", subplot_titles=list(processed[target].keys()))

    curr_row, curr_col = 1, 1

    for filename in processed[target]:
        fig.add_trace(go.Heatmap(z=processed[target][filename], name=filename), row=curr_row, col=curr_col)

        if curr_col == max_col:
            curr_row += 1
            curr_col = 1
        else: 
            curr_col += 1
    
    return fig, n_row

for filename in os.listdir(directory):
    print("Reading from ",filename)
    filedir = os.path.join(directory, filename)
    if (filename == "fires" or filename == "Ignore"):
        continue

    data[filename] = {}

    for npzname in os.listdir(filedir):
        # print(npzname)
        finaldir = os.path.join(filedir, npzname)
        data[filename][npzname] = sparse.load_npz(finaldir).tocsc()



# Crop between 0 - 36400 and 0-59700
# y_min, y_max, x_min, x_max = 11000, 30000, 20000, 45000
data_keys = list(data.keys())
# processed = change_zoom(x_min, x_max, y_min, y_max)

# If I only want a particular and figure and not the app, I just return the figure and get it here then go fig.show() 



#PLOTLY APP

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

tab_children = []

for subdir in data: 
    tab_children.append(dcc.Tab(label=subdir, value=subdir))

app.layout = html.Div([
    # html.H1('Cropped Regions'),
    # dcc.Tabs(id="tabs-graph", value=data_keys[0], children=tab_children),
    # html.Div(id='tabs-content-graph')
    html.Div(
        [
            html.Div(
                [
                    html.H1("Select Coordinates"),
                    html.P("Crop between x: 0-59700 and y: 0 - 36400"),
                    html.Form(
                        [
                            dcc.Input(
                                id="n_x_min", placeholder="x_min", name="n_x_min", type="number", value=20000
                            ),
                            dcc.Input(
                                id="n_x_max", placeholder="x_max", name="n_x_min", type="number", value=45000
                            ),
                            dcc.Input(
                                id="n_y_min", placeholder="y_min", name="n_x_min", type="number", value=11000
                            ),
                            dcc.Input(
                                id="n_y_max", placeholder="y_max", name="n_x_min", type="number", value=30000
                            ),
                            html.Button('Submit', id='submit-val', n_clicks=0, type="button"),
                            html.Div(id="output"),
                        ]
                    )
                ],
                style={"height":"1000px"},
                className="column left"
            ),
            html.Div(
                [
                    html.H1('Regions'),
                    dcc.Tabs(id="tabs-graph", value=data_keys[0], children=tab_children),
                    html.Div(id='tabs-content-graph')
                ],
                className="column right",
            )
        ],
        className="row"
    )
    
])

@callback(
    Output('tabs-content-graph', 'children'), 
    Input('tabs-graph', 'value'),
)

def render_content(tab):
 
    fig, n_row = create_figure(tab)

    return html.Div([
        html.Div(
            style={'height': (str(n_row*44) + "vh")},
            children=[dcc.Graph(
                figure = fig,
                style={"height":"100%"}
            )],
        ),
    ],
    style={'height':'4000px'},)


@callback(Output("output", "children"),
          Input('submit-val', "n_clicks"),
          State("n_x_min", "value"),
          State("n_x_max", "value"),
          State("n_y_min", "value"),
          State("n_y_max", "value"),
          prevent_initial_call=True,
          )

def update_output(n_clicks, n_x_min, n_x_max, n_y_min, n_y_max):
    # processed = change_zoom(x_min, x_max, y_min, y_max)

    if (n_x_min >= n_x_max and n_x_max < 59700 and n_x_min >=0):
        return 'x axis problem'
    if (n_y_min >= n_y_max and n_y_max < 36400 and n_y_min >=0):
        return 'y axis problem'

    processed = change_zoom(n_x_min, n_x_max, n_y_min, n_y_max)

    return f'{n_x_min} to {n_x_max} & {n_y_min} to {n_y_max}'

if __name__ == '__main__':
    y_min, y_max, x_min, x_max = 11000, 30000, 20000, 45000
    processed = change_zoom(x_min, x_max, y_min, y_max)


    app.run(debug=True)