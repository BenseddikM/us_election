import os
import pandas as pd
from monitoring.utils import connect_mongoclient
from datetime import datetime
import json
from bson import json_util
from multiprocessing import Pool


def get_collection(collection):
    MONGO_PORT = os.environ["MONGO_PORT"]
    MONGO_HOST = os.environ["MONGO_HOST"]
    c = connect_mongoclient(host=MONGO_HOST, port=MONGO_PORT)
    db = c["elections"]
    collection = db[collection]
    return collection


def clean_bson_to_json(bson):
    string_json = json_util.dumps(bson)
    dict_json = json.loads(string_json)
    return dict_json


def mongo_query_states_with_info(update_time):
    collection = get_collection("votes")
    query = {"vote_timestamp": {"$lt": update_time}}
    states = list(collection.distinct("state", query))
    return states


def mongo_query_aggregates_state(state):
    """
    Checks if state aggregates are available
    """
    collection = get_collection("aggregates")
    find_query = {"state": state}
    result = list(collection.find(find_query))
    if len(result) > 0:
        return clean_bson_to_json(result)
    else:
        # If no aggregates
        return False


def mongo_compute_state_count(state, update_time):
    collection = get_collection("votes")
    pipeline = [
        {"$match": {"state": state, "vote_timestamp": {"$lt": update_time}}},
        {"$group": {"_id": {"state": '$state', "vote_timestamp": '$vote_timestamp', "vote_result": "$vote_result"},
                    "result": {"$sum": 1}}}
    ]

    aggregates_list = list(collection.aggregate(pipeline, allowDiskUse=True))
    aggregates_list = clean_bson_to_json(aggregates_list)
    if len(aggregates_list) == 0:
        return False

    # Unnest id properties
    for item in aggregates_list:
        item["state"] = item["_id"]["state"]
        item["vote_timestamp"] = item["_id"]["vote_timestamp"]
        item["vote_result"] = item["_id"]["vote_result"]
        del item["_id"]

    # Save it in aggregates
    collection = get_collection("aggregates")
    collection.insert_many(aggregates_list)
    return aggregates_list


def update_all_states_aggregates(update_time):
    """
    PROCESS:
    for a given update_time:
    1: find states with results (distinct names in votes collection with timestamp lower than update_time)
    2: for each state with information:
        A: check if aggregate info is available in aggregates collection
        B: if not, compute counts from votes, and save it in aggregates
    """
    states = mongo_query_states_with_info(update_time)
    for state in states:
        aggregate = mongo_query_aggregates_state(state)
        if aggregate:
            return True
        try:
            mongo_compute_state_count(
                state=state, update_time=update_time)
        except:
            print("Update aggregates for state %s error" % state)


def mongo_query_aggregates_all(update_time):
    collection = get_collection("aggregates")
    find_query = {"vote_timestamp": {"$lte": update_time}}
    aggregates = list(collection.find(find_query))
    clean_aggregates = clean_bson_to_json(aggregates)
    return clean_aggregates
