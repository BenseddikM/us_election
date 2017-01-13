import os
import pandas as pd
import json

BASE_DIR = os.environ["BASE_DIR"]

# #### MAP ####


def get_geojson_data():
    data_path = os.path.join(
        BASE_DIR, "dashboard/data/states_data.json")
    with open(data_path) as data_file:
        geojson = json.load(data_file)
    flat_data = geojson["features"]
    return flat_data


def load_static_data():
    info_path = os.path.join(
        BASE_DIR, "dashboard/data/state_info.csv")
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


def get_static_map():
    # GET BASIC GEOJSON DATA
    geojson_data = get_geojson_data()

    # ADD NUMBER OF MAIN VOTERS AND NUMBER OF MAX VOTERS
    df_voters = load_static_data()
    updated_geojson_map = update_json_static_data(geojson_data, df_voters)
    return updated_geojson_map


def get_map_with_results(aggregates):
    map_records = get_static_map()
    aggregates = pd.DataFrame(aggregates)
    idx = aggregates.groupby(['state'])['result'].transform(
        max) == aggregates['result']
    winners = aggregates[idx]
    winners = winners[["state", "vote_result", "vote_timestamp"]]
    winners = winners.set_index("state")
    for record in map_records:
        try:
            state_name = record["properties"]["name"]
            record["properties"]["vote_result"] = str(
                winners["vote_result"][state_name])
            record["properties"]["vote_timestamp"] = str(
                winners["vote_timestamp"][state_name])
        except KeyError:
            record["properties"]["vote_result"] = "Unknown"
            record["properties"]["vote_timestamp"] = "Not yet"
    return map_records


# #### DONUTS ####


def extract_main_electors_donut_data(all_aggregates_at_minute):
    info_df = load_static_data()
    aggregates = pd.DataFrame(all_aggregates_at_minute)
    idx = aggregates.groupby(['state'])['result'].transform(
        max) == aggregates['result']
    winners = aggregates[idx]
    winners = winners[["state", "vote_result", "vote_timestamp"]]
    winners = winners.join(info_df[
        "Votes"], on="state")
    final_result = winners.groupby("vote_result").sum()
    final_result_json = final_result.to_json()
    final_result_dict = json.loads(final_result_json)
    results = final_result_dict["Votes"]
    candidates = ["Clinton", "Trump", "Johnson", "Stein", "Autre"]

    def check_data(candidate, data):
        try:
            return str(data[candidate])
        except KeyError:
            return "0"

    for candidate in candidates:
        results[candidate] = check_data(candidate, results)

    results["Unknown"] = 538 - int(results["Clinton"]) - int(results["Trump"])

    return results


def extract_regular_electors_donut_data(all_aggregates_at_minute):
    df = pd.DataFrame(all_aggregates_at_minute)
    results = df.groupby("vote_result").result.sum()
    results = results.to_json()
    results = json.loads(results)
    return results
