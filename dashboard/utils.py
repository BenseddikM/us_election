from django.conf import settings
import os
import pandas as pd
from monitoring.utils import connect_mongoclient

if os.environ["MONGO_PORT"]:
    MONGO_PORT = os.environ["MONGO_PORT"]
if os.environ["MONGO_HOST"]:
    MONGO_HOST = os.environ["MONGO_HOST"]


def update_json_static_data(record):
    project_path = settings.BASE_DIR

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


def mongo_query_state_count():
    c = connect_mongoclient(host=MONGO_HOST, port=MONGO_PORT)
    db = c["elections"]
    collection = db["votes"]

    pipeline = [
        {"$match": {"state": "Minnesota"}},
        {"$group": {"_id": "$vote_result", "count": {"$sum": 1}}},
    ]
    pipeline = [
        {"$match": {"state": "Minnesota"}},
        {"$group": {"_id": "$vote_result", "result": {"$first": "vote_timestamp"}}},
        {'$limit': 100},
    ]

    collection.aggregate(pipeline, allowDiskUse=True)
