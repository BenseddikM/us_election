from django.shortcuts import render
from django.http import JsonResponse
from .utils import update_json_static_data, update_all_states_aggregates, get_geojson_data, mongo_query_aggregates_all, load_static_data, get_map_with_results, extract_main_electors_donut_data, extract_regular_electors_donut_data
import os


DEFAULT_DB = os.environ["DEFAULT_DB"]


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
    if len(minute_requested) == 1:
        minute_requested = "0" + minute_requested
    if minute_requested == "60":
        update_time = '2016-11-08T21:00'
    else:
        update_time = '2016-11-08T20:%s' % minute_requested

    # UPDATE AGGREGATES FOR GIVEN TIME
    update_all_states_aggregates(update_time=update_time)

    # QUERY AGGREGATES FOR GIVEN TIME
    all_aggregates_at_minute = mongo_query_aggregates_all(
        update_time=update_time)

    # GET MAP (STATIC AND REALTIME)
    map_geojson = get_map_with_results(all_aggregates_at_minute)

    # EXTRACT MAIN VOTERS DONUT DATA
    main_electors_donut_data = extract_main_electors_donut_data(
        all_aggregates_at_minute)

    # EXTRACT REGULAR VOTERS DONUT DATA
    regular_electors_donut_data = extract_regular_electors_donut_data(
        all_aggregates_at_minute)

    # SEND INFORMATION
    data = {
        "map": {"type": "FeatureCollection", "features": map_geojson},
        "main_electors_donut_data": main_electors_donut_data,
        "regular_electors_donut_data": regular_electors_donut_data,
        "minute_requested": minute_requested,
        "all_aggregates_at_minute": all_aggregates_at_minute
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
