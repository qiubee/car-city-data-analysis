import pandas as pd
import geojson
from pprint import pprint
from collections import defaultdict
from functools import reduce
from shapely import wkt
from pathlib import Path
from os import chdir


PROVINCE = pd.read_csv("data/province.csv")
NL_PROVINCE_GEO = pd.read_csv("data/cbs_provincie_2020_gegeneraliseerd.csv")
NL_MUNICIPALITY_GEO = pd.read_csv("data/cbs_gemeente_2020_gegeneraliseerd.csv")
MUNICIPALITY = pd.read_csv("data/municipality.csv")


def group(acc, next, key):
    # value of key in next dict
    value = next[key]
    # create empty list for new value
    if not acc[value]:
        acc[value] = []
    # add dict to list of value
    acc[value].append(next)
    return acc


def group_by(list_of_dicts, key):
    # create empty dict with default value of list for any key
    d = defaultdict(list)
    # reduce on list, group on key value and place in empty dict
    return reduce(lambda acc, next: group(acc, next, key), list_of_dicts, d)


def count_total(dict, key):
    return reduce(lambda acc, next: acc + next[key], dict, 0)


def list_keys(dict, key_name="key"):
    # create list of dict keys
    return list({key_name: k, "values": v} for (k, v) in dict.items())


def nest(dict, key):
    return list_keys(group_by(dict, key))


def process_province_data(dict):
    grouped = nest(pv_dict, "province")
    for dict in grouped:
        # loop over dicts in list of key "values" & filter out key "province"
        dict["parking"] = [{key: value for (key, value) in d.items() if key != "province"} for d in dict["values"]]
        # count total
        dict["parkingTotal"] = count_total(dict["parking"], "UsageType_count")
        dict["openAllYearTotal"] = count_total(dict["parking"], "OpenAllYear")
        dict["exitPossibleAllDayTotal"] = count_total(dict["parking"], "ExitPossibleAllDay")
        # rename keys
        dict["province"] = dict["key"]
        rename_keys = {
            "ExitPossibleAllDay": "exitOpenAllDay",
            "OpenAllYear": "openAllYear",
            "UsageType_count": "total",
            "UsageType_Id": "type",
        }
        for d in dict["parking"]:
            for key in sorted(d.keys()):
                for old_key, new_key in rename_keys.items():
                    if old_key == key:
                        d[new_key] = d[old_key]
                        del d[old_key]
        # remove keys
        remove_keys = ("key", "values")
        for k in remove_keys:
            dict.pop(k, None)
    return grouped


def create_feature(shape, data):
    return geojson.Feature(geometry=shape, properties=data)


def create_featurecollection(geo_dict, data_dict, key):
    features = [create_feature(gdict["geometry"], ddict) for gdict in geo_dict for ddict in data_dict if gdict[key] == ddict[key]]
    return geojson.FeatureCollection(features)


def write_json(dict, file_name):
    Path("data").mkdir(parents=True, exist_ok=True)
    chdir("data")
    file = f"{file_name}.json"
    with open(file, "w") as json_file:
        geojson.dump(dict, json_file)
    print(file, "is created in folder: data")
    chdir("../")


# convert to shape geometry
rename_to_pv = {"statnaam": "province"}
rename_to_mp = {"statnaam": "municipality"}
pv_geo = NL_PROVINCE_GEO.rename(columns=rename_to_pv)
mp_geo = NL_MUNICIPALITY_GEO.rename(columns=rename_to_mp)
pv_geo["geometry"] = pv_geo["geometry"].apply(wkt.loads)
mp_geo["geometry"] = mp_geo["geometry"].apply(wkt.loads)


# convert DataFrame to dictionary
pv_dict = PROVINCE.to_dict("records")
mp_dict = MUNICIPALITY.to_dict("records")
pv_geo_dict = pv_geo.to_dict("records")
mp_geo_dict = mp_geo.to_dict("records")

# transform dictionaries
pv = process_province_data(pv_dict)

# create geojson
pv_geo_json = create_featurecollection(pv_geo_dict, pv, "province")

# export as json
write_json(pv_geo_json, "provinces")
