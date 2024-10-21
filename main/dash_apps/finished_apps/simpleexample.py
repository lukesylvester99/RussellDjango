from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from django.core.cache import cache
from django.contrib.auth.models import User

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)


# Layout of the Dash app
app.layout = html.Div([
    html.H1('Titer Workflow Results'),
    
    # Dropdown to select the titer metric
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'wmel_titer', 'value': 'wmel_titer'},
            {'label': 'wwil_titer', 'value': 'wwil_titer'},
            {'label': 'wri_titer', 'value': 'wri_titer'},
            {'label': 'wri_mean_depth', 'value': 'wri_mean_depth'},
            {'label': 'dmel_mean_depth', 'value': 'dmel_mean_depth'},
            {'label': 'total_reads', 'value': 'total_reads'},
            {'label': 'mapped_reads', 'value': 'mapped_reads'},
            {'label': 'duplicate_reads', 'value': 'duplicate_reads'},
            {'label': 'wmel_mean_depth', 'value': 'wmel_mean_depth'},
            {'label': 'wwil_mean_depth', 'value': 'wwil_mean_depth'},
            {'label': 'dsim_mean_depth', 'value': 'dsim_mean_depth'},
            {'label': 'mapped_reads', 'value': 'mapped_reads'},

        ],
        value='wmel_titer',  # Default value
        clearable=False,
    ),

    # Graph that will display the selected metric
    dcc.Graph(id='titer-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),

])

# Callback to update the graph based on the selected metric
@app.callback(
    Output('titer-graph', 'figure'),
    [Input('dropdown', 'value')]  # The selected titer metric from the dropdown
)
def update_graph(selected_titer_metric):
    # Assume that the current user is logged in, and we retrieve their cached data
    user_id = User.objects.first().id  # In a real application, use the logged-in user's ID
    
    # Retrieve cached sample names and titer info for the user
    cache_key_names = f"sample_names_{user_id}"
    cache_key_info = f"titer_info_{user_id}"
    
    sample_names = cache.get(cache_key_names)
    titer_info = cache.get(cache_key_info)

    if not sample_names or not titer_info:
        return {'data': [], 'layout': go.Layout(title="No Samples Found")}

    # Prepare the x and y data for the graph
    x_values = sample_names  # Sample names on the x-axis
    y_values = [titer_info[sample][selected_titer_metric] for sample in sample_names]  # Titer values on the y-axis

    # Create the bar graph
    graph = go.Bar(
        x=x_values,
        y=y_values,
        name=selected_titer_metric
    )

    layout = go.Layout(
        title=f'Titer Results for {selected_titer_metric}',
        xaxis=dict(title='Sample ID'),
        yaxis=dict(title=f'{selected_titer_metric}'),
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    # Return the figure to be displayed
    return {'data': [graph], 'layout': layout}