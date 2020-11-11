import pandas as pd
from geojson import MultiPolygon


NL_POSTAL = pd.read_csv("data/nl_postal.csv")
NL_PROVINCE_GEO = pd.read_csv("data/cbs_provincie_2020_gegeneraliseerd.csv")
RDW_DATASET = pd.read_csv("data/RDW_dataset.csv")


def drop_df_columns(df, columns):
    return df.drop(df.columns[columns], axis=1)


drop_rdw_columns = [0, 2, 3, 4, 6, 9]
rdw = drop_df_columns(RDW_DATASET, drop_rdw_columns)

rename_nl_col = {"placeName": "AreaManagerDesc"}
nl_place_hierarchy = drop_df_columns(NL_POSTAL, [3, 4])
nl_place_hierarchy = nl_place_hierarchy.rename(columns=rename_nl_col)

rdw_geo = pd.merge(rdw, nl_place_hierarchy, how="left", on=["AreaManagerDesc"])

# rdw_group_col = [rdw_geo.columns.values[i] for i in [5]]
rdw_geo["UsageType_count"] = rdw_geo.groupby("UsageType_Id")["UsageType_Id"].transform(lambda x: x.count())

# get sum of "ExitPossibleAllDay" & "OpenAllYear" of each province

# province_geo = rdw_geo.groupby(rdw_group_col)["UsageType_Id"].value_counts()
print(rdw_geo)
