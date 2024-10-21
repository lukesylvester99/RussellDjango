from django.shortcuts import render
import pandas as pd 
import plotly.graph_objects as go 
from plotly.io import to_html
from django.core.cache import cache
from django.contrib.auth.models import User
from main.models import Titer

#options for user to select between graphs
titer_values = [
    'wri_mean_depth',
    'dmel_mean_depth',
    'wri_titer',
    'total_reads',
    'mapped_reads',
    'duplicate_reads',
    'wmel_mean_depth',
    'wwil_mean_depth',
    'wmel_titer',
    'wwil_titer',
    'dsim_mean_depth'
]

#retrieves/filters/sorts data associated with cache
def cache_titer_data(user_id):
    cache_key = f"filtered_samples_{user_id}"
    sample_ids = cache.get(cache_key) #sample IDs from custom filter

    titer_data = Titer.objects.filter(sample_id__in=sample_ids)
    titer_dict = {} # coalesce titer data into dict format
    for obj in titer_data:
        titer_dict[obj.sample_id.sample_id] = {
            "wri_mean_depth": obj.wri_mean_depth,
            "dmel_mean_depth": obj.dmel_mean_depth,
            "wri_titer": obj.wri_titer,
            "total_reads": obj.total_reads,
            "mapped_reads": obj.mapped_reads,
            "duplicate_reads": obj.duplicate_reads,
            "wmel_mean_depth": obj.wmel_mean_depth,
            "wwil_mean_depth": obj.wwil_mean_depth,
            "wmel_titer": obj.wmel_titer,
            "wwil_titer": obj.wwil_titer,
            "dsim_mean_depth": obj.dsim_mean_depth,
        }

    # Save the titer info and sample names to cache
    cache.set(f"sample_names_{user_id}", list(titer_dict.keys()), timeout=3600)
    cache.set(f"titer_info_{user_id}", titer_dict, timeout=3600)

    return titer_dict

def create_bar_chart(selected_titer_metric, sample_names, titer_info):
    x_values = sample_names
    y_values = [titer_info[sample][selected_titer_metric] for sample in sample_names]  

    graph = go.Figure(data=[
        go.Bar(
            x=x_values,
            y=y_values,
            name=selected_titer_metric,
            marker=dict(color='#6200EE')
        )])

    graph.update_layout(
        title={
            'text': f'Titer Results for {selected_titer_metric}',
            'x': 0.5, 
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}, 
        },
        xaxis=dict(
            title='Sample ID',
            titlefont={'size': 18}, 
            tickmode='linear',
            tick0=0,
        ),
        yaxis=dict(
            title=f'{selected_titer_metric}',
            titlefont={'size': 18},  
            automargin=True, 
        ),
        font=dict(color='white'),
        bargap=0.75, 
        paper_bgcolor='#27293d',
    )


    return graph

def display_graph(request, titer: str):
    user_id = request.user.id

    cache_key_names = f"sample_names_{user_id}"
    cache_key_info = f"titer_info_{user_id}"

    sample_names = cache.get(cache_key_names)
    titer_info = cache.get(cache_key_info)

    # Populate cache if it doesn't have values yet
    if not sample_names or not titer_info:
        titer_info = cache_titer_data(user_id)
        sample_names = list(titer_info.keys())

    # Create the bar chart
    bar_chart = create_bar_chart(titer, sample_names, titer_info)
    chart_div = to_html(bar_chart, full_html=False, include_plotlyjs="cdn", div_id='titer_chart')

    context = {
        "titer_values": titer_values,
        "chart_div": chart_div
    }

    return render(request, 'titer.html', context)
