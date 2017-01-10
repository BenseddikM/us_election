from django.conf import settings
import os
import pandas as pd
from monitoring.utils import connect_mongoclient
from datetime import datetime
import json
from bson import json_util
from multiprocessing import Pool

if os.environ["MONGO_PORT"]:
    MONGO_PORT = os.environ["MONGO_PORT"]
if os.environ["MONGO_HOST"]:
    MONGO_HOST = os.environ["MONGO_HOST"]

project_path = settings.BASE_DIR


def get_geojson_data():
    project_path = settings.BASE_DIR
    data_path = os.path.join(
        project_path, "dashboard/data/states_data.json")
    with open(data_path) as data_file:
        geojson = json.load(data_file)
    flat_data = geojson["features"]
    return flat_data


def load_static_data():
    info_path = os.path.join(
        project_path, "dashboard/data/state_info.csv")
    info_df = pd.read_csv(
        info_path, index_col="State", sep=";", thousands=",")
    return info_df


def update_json_static_data(records, info_df):
    for record in records:
        try:
            state_name = record["properties"]["name"]
            # Add info to record
            record["properties"]["nb_votes"] = str(
                info_df["Votes"][state_name])
            record["properties"]["max_voters"] = str(
                info_df["VEP"][state_name])
        except KeyError:
            record["properties"]["nb_votes"] = "0"
            record["properties"]["max_voters"] = "0"
    return records


def mongo_save_aggregates(agg_list):
    c = connect_mongoclient(host=MONGO_HOST, port=MONGO_PORT)
    db = c["elections"]
    collection = db["aggregates"]
    collection.insert_many(agg_list)


def mongo_query_aggregates_state(state):
    """
    Checks if state aggregates are available
    """
    c = connect_mongoclient(host=MONGO_HOST, port=MONGO_PORT)
    db = c["elections"]
    collection = db["aggregates"]
    find_query = {"state": state}
    result = list(collection.find(find_query))
    if len(result) > 0:
        # first transform into json
        string_json = json_util.dumps(result)
        result = json.loads(string_json)
        return result
    else:
        return False


def mongo_compute_state_count(state="Minnesota", minute=None, limit=10000000):
    c = connect_mongoclient(host=MONGO_HOST, port=MONGO_PORT)
    db = c["elections"]
    collection = db["votes"]
    if not minute:
        update_time = datetime.now().strftime('2016-11-08T20:%M')
    else:
        update_time = '2016-11-08T20:%s' % minute
    # timestamp: "2016-11-08T20:00"
    pipeline = [
        {"$match": {"state": state, "vote_timestamp": {"$lt": update_time}}},
        {'$limit': 10000000},  # in case lots of voters
        {"$group": {"_id": {"state": '$state', "vote_timestamp": '$vote_timestamp', "vote_result": "$vote_result"},
                    "result": {"$sum": 1}}}
    ]

    answer = list(collection.aggregate(pipeline, allowDiskUse=True))
    # Handle BSON object?
    string_json = json_util.dumps(answer)
    answer = json.loads(string_json)

    for item in answer:
        # free _id
        item["state"] = item["_id"]["state"]
        item["vote_timestamp"] = item["_id"]["vote_timestamp"]
        item["vote_result"] = item["_id"]["vote_result"]
        del item["_id"]

    # print("Request answer: ", answer)
    if len(answer) == 0:
        return False
    else:
        return answer


def get_state_aggregates(state, minute):
    # Try to find in aggregate collection
    print("GETTING AGG FOR %s at minute %s " % (state, minute))
    print("Is information in aggregate collection?")
    aggregate = mongo_query_aggregates_state(state)
    if aggregate:
        print("Yes!")
        return (state, aggregate)
    print("No, so we'll compute it it: is data available?")
    aggregate = mongo_compute_state_count(state=state, minute=minute)
    if aggregate:
        print("Yes! Let's save it in Mongo aggregate collection")
        try:
            # save it in aggregate collection
            mongo_save_aggregates(aggregate)
        except:
            print("Saving results didn't work")
        return (state, aggregate)
    print("Information not available at this time")
    return (state, False)


def get_all_states_aggregates(minute):
    data_file_path = os.path.join(
        project_path, "dashboard", "data", "state_info.csv")
    df = pd.read_csv(data_file_path, sep=";")
    states = df["State"].values
    results = {}

    pool = Pool(processes=10)
    n = len(states)
    all_parameters = zip(states, [minute] * n)
    list_tuples = pool.starmap(get_state_aggregates, all_parameters)
    pool.close()
    pool.join()

    for item_tuple in list_tuples:
        if item_tuple[1]:
            results[item_tuple[0]] = item_tuple[1]
        else:
            results[item_tuple[0]] = "Not available"
    return results


def update_json_realtime_data():
    pass


def mongo_query_aggregates_all(minute):
    c = connect_mongoclient(host=MONGO_HOST, port=MONGO_PORT)
    db = c["elections"]
    collection = db["aggregates"]
    if not minute:
        update_time = datetime.now().strftime('2016-11-08T20:%M')
    else:
        update_time = '2016-11-08T20:%s' % minute
    find_query = {"vote_timestamp": {"$lte": update_time}}
    aggregates = list(collection.find(find_query))
    return aggregates


"""
    {"$match": {"state": "Minnesota", "vote_timestamp": {"$lt": "2016-11-08T20:00"}}},
    {'$limit': 10000000},
    {"$group": {"_id": {"state": '$state', "vote_timestamp": '$vote_timestamp', "vote_result": "$vote_result"},
                "result": {"$sum": 1}}}



Result array of:

{ "_id" : { "state" : "Minnesota", "vote_timestamp" : "2016-11-08T20:00", "vote_result" : "Autre" }, "result" : 41657 }
{ "_id" : { "state" : "Minnesota", "vote_timestamp" : "2016-11-08T20:00", "vote_result" : "McMullin" }, "result" : 53076 }
"""
