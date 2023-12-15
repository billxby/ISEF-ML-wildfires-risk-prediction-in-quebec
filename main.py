from scipy import sparse
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sys import getsizeof
import numpy as np
import os
from dash import Dash, html, dcc, callback, Output, State, Input

directory = r"D:\Users\xubil\OneDrive\Documents\Wildfires Data NPZ\Training"
data = {}
processed = {}
max_col = 4 # Dashboard 

def change_zoom(x_min, x_max, y_min, y_max):
    ratio_y, ratio_x = (y_max-y_min)/36400, (x_max-x_min)/59700
    
    for item in data:
        data_process = data[item][y_min:y_max, x_min:x_max] # To csc speeds up processing

        N, M = data_process.shape
        s, t = int(400*ratio_y), int(400*ratio_x)          # decimation factors for y and x directions
        T = sparse.csc_matrix((np.ones((M,)), np.arange(M), np.r_[np.arange(0, M, t), M]), (M, (M-1) // t + 1))
        S = sparse.csr_matrix((np.ones((N,)), np.arange(N), np.r_[np.arange(0, N, s), N]), ((N-1) // s + 1, N))
        result = S @ data_process @ T     # downsample by binning into s x t rectangles
        processed[item] = result.todense() 
    
    # return processed

def create_figure():
    total = len(processed)
    n_row = int(total/max_col if total % max_col == 0 else total/max_col+1)
    # print(target)
    # print(n_row)

    fig = make_subplots(
        rows=n_row, cols=4, 
        start_cell="top-left", subplot_titles=list(processed.keys()))

    curr_row, curr_col = 1, 1

    for filename in processed:
        fig.add_trace(go.Heatmap(z=processed[filename], name=filename), row=curr_row, col=curr_col)
        fig['layout']['yaxis']['autorange'] = "reversed"

        if curr_col == max_col:
            curr_row += 1
            curr_col = 1
        else: 
            curr_col += 1
    
    return fig, n_row

for filename in os.listdir(directory):
    print("Reading from ",filename)

    if (filename == 'Ignore'):
        continue

    data[filename] = sparse.load_npz(os.path.join(directory, filename))
    # print(data[filename].shape)

# print(data)



# Crop between 0 - 36400 and 0-59700
y_min, y_max, x_min, x_max = 11000, 30000, 20000, 45000
data_keys = list(data.keys())
change_zoom(x_min, x_max, y_min, y_max)
fig, nrow = create_figure()

# If I only want a particular and figure and not the app, I just return the figure and get it here then go fig.show() 


# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.RangeSlider(0, 75438, marks={0:'0', 75438:'75438'}, value=[x_min, x_max], id='x-slider', allowCross=False),
    dcc.RangeSlider(0, 46080, marks={0:'0', 46080:'46080'}, value=[y_min, y_max], id='y-slider', allowCross=False),
    html.Div(id='output-graphs')
    # dcc.Graph(figure={}, style={'height': str(nrow*30)+"vw"}, id='output-graph')
])

@callback(
    Output('output-graphs', 'children'),
    Input('x-slider', 'value'),
    Input('y-slider', 'value')
)
def update_output(value_x, value_y):
    change_zoom(value_x[0], value_x[1], value_y[0], value_y[1])
    fig, nrow = create_figure()
    return dcc.Graph(
        figure=fig,
        style={'height': str(nrow*30)+"vw"}
    )

# Run the app
if __name__ == '__main__':
    app.run(debug=True)