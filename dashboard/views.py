from django.shortcuts import render
from django.http import JsonResponse
import json
from .utils import update_json_static_data, update_all_states_aggregates, get_geojson_data, mongo_query_aggregates_all, load_static_data, get_static_map, extract_main_electors_donut_data, extract_regular_electors_donut_data
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

    # GET MAP STATIC DATA
    updated_json = get_static_map()

    # UPDATE REAL TIME INFORMATION
    state_results = update_all_states_aggregates(minute=minute_requested)

    # QUERY AGGREGATES FORMERLY CREATED
    all_aggregates_at_minute = mongo_query_aggregates_all(
        minute=minute_requested)

    # EXTRACT MAIN VOTERS DONUT DATA
    main_electors_donut_data = extract_main_electors_donut_data(
        all_aggregates_at_minute)

    # EXTRACT REGULAR VOTERS DONUT DATA
    regular_electors_donut_data = extract_regular_electors_donut_data(
        all_aggregates_at_minute)

    # SEND INFORMATION
    data = {
        "map": {"type": "FeatureCollection", "features": updated_json},
        "state_results": state_results,
        "main_electors_donut_data": main_electors_donut_data,
        "regular_electors_donut_data": regular_electors_donut_data,
        "minute_requested": minute_requested
    }
    # df = pd.read_json(flat_data)

    return JsonResponse(data, safe=False)

"""
[
  {label: "Donald Trump – Parti républicain", value: 150},
  {label: "Hillary Clinton – Parti démocrate", value: 130},
  {label: "Gary Johnson – Parti libertarien", value: 15},
  {label: "Jill Stein – Parti vert", value: 10},
  {label: "No known yet", value: 150}
]
"""
