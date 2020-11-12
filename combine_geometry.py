import pandas as pd
from operator import itemgetter
from itertools import groupby
from collections import defaultdict
from geojson import MultiPolygon


NL_POSTAL = pd.read_csv("data/nl_postal.csv")
NL_PROVINCE_GEO = pd.read_csv("data/cbs_provincie_2020_gegeneraliseerd.csv")
RDW_DATASET = pd.read_csv("data/RDW_dataset.csv")


def drop_df_columns(df, columns):
    return df.drop(df.columns[columns], axis=1)


# drop unused columns
drop_rdw_columns = [0, 2, 3, 4, 6, 9]
rdw = drop_df_columns(RDW_DATASET, drop_rdw_columns)

# match merge column & merge
rename_nl_col = {"placeName": "AreaManagerDesc"}
nl_place_hierarchy = drop_df_columns(NL_POSTAL, [3, 4])
nl_place_hierarchy = nl_place_hierarchy.rename(columns=rename_nl_col)
rdw_geo = pd.merge(rdw, nl_place_hierarchy, how="left", on=["AreaManagerDesc"])

# add sum of usage type in new column
rdw_geo["UsageType_count"] = rdw_geo.groupby("UsageType_Id")["UsageType_Id"].transform(lambda x: x.count())

# count sum of boolean columns
province_cols = [rdw_geo.columns.values[i] for i in [4, 5, 7]]
province_geo = rdw_geo.groupby(province_cols, as_index=False)[["ExitPossibleAllDay", "OpenAllYear"]].sum()

# convert DataFrame to dictionary
province_dict = province_geo.to_dict("records")

# group by province
province_dict = sorted(province_dict, key=itemgetter("province"))
res = defaultdict(list)
for key, group in groupby(province_dict, key=itemgetter("province")):
    res[key] = key
    # res["province"] = key
    for val in group:
        print(val)

print(res)
