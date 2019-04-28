# based on cyto-multiselect-callback.py

# added ability to add nodes and edges
# + experiments with styling
# + logging (but not enough to conveniently store changes between sessions)

#import json
import datetime

print("START")

with open("logfile.txt", "a") as file:
    print(str(datetime.datetime.now()), file=file)

import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

nodes = [
    {
        'data': {'id': short, 'label': label},
        'position': {'x': 20*lon, 'y': -20*lat}
    }
    for short, label, lat, lon in (
        ('la', 'Los Angeles', 34.03, -118.25),
        ('nyc', 'New York', 40.71, -74),
        ('to', 'Toronto', 43.65, -79.38),
        ('mtl', 'Montreal', 45.50, -73.57),
        ('van', 'Vancouver', 49.28, -123.12),
        ('chi', 'Chicago', 41.88, -87.63),
        ('bos', 'Boston', 42.36, -71.06),
        ('hou', 'Houston', 29.76, -95.37)
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('van', 'la'),
        ('la', 'chi'),
        ('hou', 'chi'),
        ('to', 'mtl'),
        ('mtl', 'bos'),
        ('nyc', 'bos'),
        ('to', 'hou'),
        ('to', 'nyc'),
        ('la', 'nyc'),
        ('nyc', 'bos')
    )
]

selected_source = ""
selected_target = ""

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'vee',
        }
    },
    {
        'selector': ':selected',
        'style': {
            'background-color': 'purple',
            'shape': 'octagon',
            #'width': '35px' # have not figured out a way to do it only for nodes, but not for edges
            #'height': '25px'
            #'line-color': 'blue' # commented out: let's keep the default, some different shade of blue
        }
    }
]


app.layout = html.Div([
    html.Div([
        html.Div(style={'width': '20%', 'display': 'inline'}, children=[
            'Label:',
            dcc.Input(id='input-label', type='text')
        ]),
        html.Div(style={'width': '20%', 'display': 'inline'}, children=[
            'Id:',
            dcc.Input(id='input-node-id', type='text')
        ]),
        html.Div(style={'width': '20%', 'display': 'inline'}, children=[
            'Lat:',
            dcc.Input(id='input-lat', type='text')
        ]),
        html.Div(style={'width': '20%', 'display': 'inline'}, children=[
            'Lon:',
            dcc.Input(id='input-lon', type='text')
        ]),
        html.Button('Add Node', id='btn-add-node', n_clicks_timestamp=0),
    ]),
    html.Div([
        html.Div(style={'width': '20%', 'display': 'inline'}, children=[
            'Source Id:',
            dcc.Input(id='source-id', type='text')
        ]),
        html.Div(style={'width': '20%', 'display': 'inline'}, children=[
            'Target Id:',
            dcc.Input(id='target-id', type='text')
        ]),
        html.Button('Add Edge', id='btn-add-edge', n_clicks_timestamp=0),
    ]),
    cyto.Cytoscape(
        id='cytoscape-graph',
        layout={'name': 'preset'},
        elements=edges+nodes,
        stylesheet=default_stylesheet,
		boxSelectionEnabled=True,
        style={'width': '100%', 'height': '450px'}
    ),
    dcc.Markdown(id='cytoscape-selectedNodeData-markdown')
])


@app.callback([Output('cytoscape-selectedNodeData-markdown', 'children'),
               Output('source-id', 'value'),
               Output('target-id', 'value')],
              [Input('cytoscape-graph', 'selectedNodeData'),
               Input('cytoscape-graph', 'selectedEdgeData')])
def displaySelectedNodeData(node_data_list, edge_data_list):

    global selected_source
    global selected_target

    if node_data_list:
        cities_list = [data['label']+' ('+data['id']+')' for data in node_data_list]
        cities_string = "\nYou selected the following cities:\n* " + "\n* ".join(cities_list)
        if len(node_data_list) > 0: selected_source = node_data_list[0]['id']
        if len(node_data_list) > 1: selected_target = node_data_list[1]['id']
    else:
        cities_string = ""
	
    if edge_data_list:
        routes_list = [data['source']+"->"+data['target'] for data in edge_data_list]
        routes_string = "\n\nYou selected the following routes:\n* " + "\n* ".join(routes_list)
    else:
        routes_string = ""	
	
    return cities_string + routes_string, selected_source, selected_target

@app.callback(Output('cytoscape-graph', 'elements'),
              [Input('btn-add-node','n_clicks_timestamp'),
               Input('btn-add-edge','n_clicks_timestamp')],
              [State('input-label', 'value'),
               State('input-node-id', 'value'),
               State('input-lat', 'value'),
               State('input-lon', 'value'),
               State('source-id', 'value'),
               State('target-id', 'value')])
def addNodeOrEdge(timestamp_add_node, timestamp_add_edge, input_label, input_id, input_lat, input_lon, source_id, target_id):
    print("timestamp_add_node = ", timestamp_add_node)
    print("timestamp_add_edge = ", timestamp_add_edge)
    # good only for single user
    global nodes
    global edges
    if timestamp_add_node > timestamp_add_edge:
        if not input_lat: input_lat = '38.5'
        if not input_lon: input_lon = '-100.0'
        new_node = {
                      'data': {'id': input_id, 'label': input_label},
                      'position': {'x': 20*float(input_lon), 'y': -20*float(input_lat)}
                   }        
        with open("logfile.txt", "a") as file:
           print(new_node, file=file)
        nodes = nodes + [new_node] 

    if timestamp_add_edge > timestamp_add_node:
        new_edge = {
                      'data': {'source': source_id, 'target': target_id},
                   }        
        with open("logfile.txt", "a") as file:
           print(new_edge, file=file)
        edges = edges + [new_edge] 

    return edges+nodes
 
    
if __name__ == '__main__':
    print("ABOUT TO RUN SERVER")
    app.run_server(debug=True)
	