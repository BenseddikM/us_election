from django.shortcuts import render
from django.http import JsonResponse
import os
import json
import pandas as pd

from django.conf import settings


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
    project_path = settings.BASE_DIR
    data_path = os.path.join(
        project_path, "dashboard/data/states_data.json")
    with open(data_path) as data_file:
        geojson = json.load(data_file)

    flat_data = geojson["features"]
    # Extract state name

    def update_json(record):
        try:
            state_name = record["properties"]["name"]
            info_path = os.path.join(
                project_path, "dashboard/data/state_info.csv")
            info_df = pd.read_csv(
                info_path, index_col="State", sep=";", thousands=",")
            # Add info to record
            record["properties"]["nb_votes"] = str(
                info_df["Votes"][state_name])
            record["properties"]["max_voters"] = str(
                info_df["VEP"][state_name])
        except KeyError:
            record["properties"]["nb_votes"] = "0"
            record["properties"]["max_voters"] = "0"

        return record
    updated_json = list(map(update_json, flat_data))
    features_collection = {
        "type": "FeatureCollection",
        "features": updated_json
    }
    # df = pd.read_json(flat_data)

    return JsonResponse(features_collection, safe=False)
