from django.shortcuts import render
from django.http import JsonResponse
import json
from .utils import update_json_static_data
from django.conf import settings
import os


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

    # GET BASIC GEOJSON DATA
    project_path = settings.BASE_DIR
    data_path = os.path.join(
        project_path, "dashboard/data/states_data.json")
    with open(data_path) as data_file:
        geojson = json.load(data_file)
    flat_data = geojson["features"]

    # ADD NUMBER OF MAIN VOTERS AND NUMBER OF MAX VOTERS
    updated_json = list(map(update_json_static_data, flat_data))

    # GET REAL TIME INFORMATION

    # SEND AS A FEATURES COLLECTION
    features_collection = {
        "type": "FeatureCollection",
        "features": updated_json
    }
    # df = pd.read_json(flat_data)

    return JsonResponse(features_collection, safe=False)
