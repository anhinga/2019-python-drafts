# a slightly cleaned up and extended the last example from Dash Cytoscape docs 
# Documentation chapter https://dash.plot.ly/cytoscape/events

# Changes:
#   boxSelectionEnabled=True (added)
#   lat/long semantics (fixed)
#   markdown output formatting (fixed)
#   output list of selected edges (added)

#import json

import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

nodes = [
    {
        'data': {'id': short, 'label': label},
        'position': {'x': 20*long, 'y': -20*lat}
    }
    for short, label, lat, long in (
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


default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    }
]


app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-event-callbacks',
        layout={'name': 'preset'},
        elements=edges+nodes,
        stylesheet=default_stylesheet,
		boxSelectionEnabled=True,
        style={'width': '100%', 'height': '450px'}
    ),
    dcc.Markdown(id='cytoscape-selectedNodeData-markdown')
])


@app.callback(Output('cytoscape-selectedNodeData-markdown', 'children'),
              [Input('cytoscape-event-callbacks', 'selectedNodeData'),
			   Input('cytoscape-event-callbacks', 'selectedEdgeData')])
def displaySelectedNodeData(node_data_list, edge_data_list):

    if node_data_list:
        cities_list = [data['label'] for data in node_data_list]
        cities_string = "\nYou selected the following cities:\n* " + "\n* ".join(cities_list)
    else:
        cities_string = ""
	
    if edge_data_list:
        routes_list = [data['source']+"->"+data['target'] for data in edge_data_list]
        routes_string = "\n\nYou selected the following routes:\n* " + "\n* ".join(routes_list)
    else:
        routes_string = ""	
	
    return cities_string + routes_string


if __name__ == '__main__':
    app.run_server(debug=True)
	