import os
from django.shortcuts import render
from monitoring.utils import check_mongo_connection
from django.http import JsonResponse

if os.environ["MONGO_PORT"]:
    MONGO_PORT = os.environ["MONGO_PORT"]
if os.environ["MONGO_HOST"]:
    MONGO_HOST = os.environ["MONGO_HOST"]


def index(request):
    context = {}
    return render(request, 'monitoring.html', context)


def ajax_monitoring_mongo_db(request):
    status, add_info = check_mongo_connection(host=MONGO_HOST, port=MONGO_PORT)
    response = {"status": status, "add_info": add_info or ""}
    return JsonResponse(response)
