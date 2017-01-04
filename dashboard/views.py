from django.shortcuts import render
from django.http import JsonResponse
import os
import json
# import pandas as pd

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

    return JsonResponse(geojson, safe=False)
