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

# rdw_geo = rdw_geo.groupby("province")["UsageIdDesc"].agg(lambda x: x.value_counts().index[0])
print(rdw_geo)
