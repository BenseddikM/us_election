import os
from django.shortcuts import render
from monitoring.utils import check_mongo_connection
from django.http import JsonResponse
import logging


logger = logging.getLogger(__name__)


def index(request):
    context = {}
    return render(request, 'monitoring.html', context)


def ajax_monitoring_mongo_db(request):
    # print(MONGO_HOST, MONGO_PORT)
    logger.info("Trying to get Mongo status")
    status, add_info = check_mongo_connection()
    response = {"status": status, "add_info": add_info or ""}
    return JsonResponse(response)
