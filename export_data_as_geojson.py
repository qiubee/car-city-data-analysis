import pandas as pd
from pprint import pprint
from collections import defaultdict
from functools import reduce

PROVINCE = pd.read_csv("data/province.csv")
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
        dict["province"] = dict["key"]
        # loop over dicts in list of key "values" & filter out key "province"
        dict["parking"] = [{key: value for (key, value) in d.items() if key != "province"} for d in dict["values"]]
        # count total
        dict["parkingTotal"] = count_total(dict["parking"], "UsageType_count")
        dict["openAllYearTotal"] = count_total(dict["parking"], "OpenAllYear")
        dict["exitPossibleAllDayTotal"] = count_total(dict["parking"], "ExitPossibleAllDay")
        remove_keys = ("key", "values")
        for k in remove_keys:
            dict.pop(k, None)
    return grouped


# convert DataFrame to dictionary
pv_dict = PROVINCE.to_dict("records")
mp_dict = MUNICIPALITY.to_dict("records")

pv = process_province_data(pv_dict)
pprint(pv)

# add geometry
# rename_to_pv = {"statnaam": "province"}
# rename_to_mp = {"statnaam": "municipality"}
# pv_geo = NL_PROVINCE_GEO.rename(columns=rename_to_pv)
# mp_geo = NL_MUNICIPALITY_GEO.rename(columns=rename_to_mp)
# pv_complete = pd.merge(pv_geo, rdw_geo, how="left", on=["province"])
# mp_complete = pd.merge(mp_geo, rdw_geo, how="left", on=["municipality"])
