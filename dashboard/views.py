from django.shortcuts import render
from django.http import JsonResponse
import json
from .utils import update_json_static_data, get_all_states_aggregates, get_geojson_data, mongo_query_aggregates_all, load_static_data
from django.conf import settings
import os
import pandas as pd


def index(request):
    context = {}
    return render(request, 'dashboard.html', context)


def state_view(request):
    context = {}
    return render(request, 'state.html', context)


def map_view(request):
    context = {}
    return render(request, 'map.html', context)


def map_data_ajax(request):
    minute_requested = request.GET.get('minute', '0')

    # GET BASIC GEOJSON DATA
    flat_data = get_geojson_data()

    # ADD NUMBER OF MAIN VOTERS AND NUMBER OF MAX VOTERS
    info_df = load_static_data()
    updated_json = update_json_static_data(flat_data, info_df)

    # GET REAL TIME INFORMATION
    state_results = get_all_states_aggregates(minute=minute_requested)

    # GET GENERAL DONUT RESULT
    aggregates_list = mongo_query_aggregates_all(minute=minute_requested)
    aggregates = pd.DataFrame(aggregates_list)
    idx = aggregates.groupby(['state'])['result'].transform(
        max) == aggregates['result']
    winners = aggregates[idx]
    winners = winners[["state", "vote_result", "vote_timestamp"]].join(info_df[
                                                                       "Votes"], on="state")
    final_result = winners.groupby("vote_result").sum()
    final_result_json = final_result.to_json()
    final_result_dict = json.loads(final_result_json)

    # SEND AS A FEATURES COLLECTION
    features_collection = {
        "type": "FeatureCollection",
        "features": updated_json,
        "state_results": state_results,
        "general": final_result_dict
    }
    # df = pd.read_json(flat_data)

    return JsonResponse(features_collection, safe=False)

"""
[
  {label: "Donald Trump – Parti républicain", value: 150},
  {label: "Hillary Clinton – Parti démocrate", value: 130},
  {label: "Gary Johnson – Parti libertarien", value: 15},
  {label: "Jill Stein – Parti vert", value: 10},
  {label: "No known yet", value: 150}
]
"""
