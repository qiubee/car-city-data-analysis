import pandas as pd
import geojson
from collections import defaultdict
from functools import reduce
from shapely import wkt
from pathlib import Path
from os import chdir
from math import isnan


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


def isnone(dict, key):
    none_count = reduce(lambda acc, next: acc + 1 if next[key] is None else acc, dict, 0)
    if none_count == len(dict):
        return True
    else:
        return False


def count_total(dict, key):
    if isnone(dict, key):
        return None
    else:
        return reduce(lambda acc, next: acc + next[key] if not next[key] is None else acc, dict, 0)


def list_keys(dict, key_name="key"):
    # create list of dict keys
    return list({key_name: k, "values": v} for (k, v) in dict.items())


def rename_keys(dict, keys_to_rename):
    for key in sorted(dict.keys()):
        for old_key, new_key in keys_to_rename.items():
            if old_key == key:
                dict[new_key] = dict[old_key]
                del dict[old_key]
    return dict


def nest(dict, key):
    return list_keys(group_by(dict, key))


def process_province_data(dict):
    grouped = nest(dict, "province")
    for province in grouped:
        # loop over dicts in list of key "values" & filter out key "province"
        province["parking"] = [{key: value for (key, value) in d.items() if key != "province"} for d in province["values"]]
        # count totals
        province["parkingTotal"] = count_total(province["parking"], "UsageType_count")
        province["openAllYearTotal"] = count_total(province["parking"], "OpenAllYear")
        province["exitPossibleAllDayTotal"] = count_total(province["parking"], "ExitPossibleAllDay")
        # rename keys
        province["province"] = province["key"]
        keys_to_rename = {
            "ExitPossibleAllDay": "exitOpenAllDay",
            "OpenAllYear": "openAllYear",
            "UsageType_count": "total",
            "UsageType_Id": "type",
        }
        for d in province["parking"]:
            rename_keys(d, keys_to_rename)
        # remove keys
        remove_keys = ("key", "values")
        for k in remove_keys:
            province.pop(k, None)
    return grouped


def process_municipality_data(dict):
    grouped = nest(dict, "municipality")
    for municipality in grouped:
        # convert floats to integer
        for d in municipality["values"]:
            for key, val in d.items():
                if isinstance(val, float):
                    if not isnan(val):
                        d[key] = int(val)
                    else:
                        d[key] = None
        # loop over dicts in list of key "values" & filter out "province" & "municipality"
        municipality["parking"] = [{key: value for (key, value) in d.items() if key != "municipality" and key != "province"} for d in municipality["values"]]
        # count totals
        municipality["parkingTotal"] = count_total(municipality["parking"], "UsageType_count")
        municipality["openAllYearTotal"] = count_total(municipality["parking"], "OpenAllYear")
        municipality["exitPossibleAllDayTotal"] = count_total(municipality["parking"], "ExitPossibleAllDay")
        # rename keys
        municipality["province"] = municipality["values"][0]["province"]
        municipality["municipality"] = municipality["key"]
        keys_to_rename = {
            "ExitPossibleAllDay": "exitOpenAllDay",
            "OpenAllYear": "openAllYear",
            "UsageType_count": "total",
            "UsageType_Id": "type",
        }
        for d in municipality["parking"]:
            rename_keys(d, keys_to_rename)
        # remove keys
        remove_keys = ("key", "values")
        for k in remove_keys:
            municipality.pop(k, None)
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
mp = process_municipality_data(mp_dict)

# create geojson
pv_geo_json = create_featurecollection(pv_geo_dict, pv, "province")
mp_geo_json = create_featurecollection(mp_geo_dict, mp, "municipality")

# export as json
write_json(pv_geo_json, "provinces")
write_json(mp_geo_json, "municipalities")
