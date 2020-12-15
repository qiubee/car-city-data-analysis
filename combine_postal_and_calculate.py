from pathlib import Path
from os import chdir
import pandas as pd

NL_POSTAL = pd.read_csv("data/nl_postal.csv")
RDW_DATASET = pd.read_csv("data/RDW_dataset.csv")


def drop_df_columns(df, columns):
    return df.drop(df.columns[columns], axis=1)


def write_csv(data, filename):
    Path("data").mkdir(parents=True, exist_ok=True)
    chdir("data")
    file = f"{filename}.csv"
    data.to_csv(file, index=False)
    print(file, "is created in folder: data")
    chdir("../")


def group_and_sum(df, group_columns, to_sum_columns):
    return df.groupby(group_columns, as_index=False)[to_sum_columns].sum()


# drop unused columns
drop_rdw_columns = [0, 2, 3, 4, 6, 9]
rdw = drop_df_columns(RDW_DATASET, drop_rdw_columns)

# match column & merge
rename_nl_col = {"placeName": "AreaManagerDesc"}
nl_place_hierarchy = drop_df_columns(NL_POSTAL, [3, 4])
nl_place_hierarchy = nl_place_hierarchy.rename(columns=rename_nl_col)
rdw_geo = pd.merge(rdw, nl_place_hierarchy, how="left", on=["AreaManagerDesc"])

# add sum of usage type in new column
rdw_geo["UsageType_count"] = rdw_geo.groupby(["AreaManagerDesc", "UsageType_Id"])["UsageType_Id"].transform(lambda x: x.count())

# count sum of boolean columns for municipalities
mp_sum_cols = ["ExitPossibleAllDay", "OpenAllYear"]
mp_group_cols = [rdw_geo.columns.values[i] for i in [4, 5, 6, 7]]
mp_summed = group_and_sum(rdw_geo, mp_group_cols, mp_sum_cols)

# count sum of municipalities
mp_all_summed = mp_summed.groupby(["municipality", "UsageType_Id", "province"], as_index=False).sum()

# add missing municipalities
nl_municipalities = drop_df_columns(nl_place_hierarchy, [0])
mp_data = pd.merge(mp_all_summed, nl_municipalities, how="outer", on=["municipality"])
mp_data = mp_data.drop_duplicates()
mp_data = mp_data.reset_index(drop=True)

# count sum of province
pv_sum_col = ["ExitPossibleAllDay", "OpenAllYear", "UsageType_count"]
pv_group_cols = [rdw_geo.columns.values[i] for i in [4, 5]]
pv_data = group_and_sum(mp_all_summed, pv_group_cols, pv_sum_col)

write_csv(pv_data, "province")
write_csv(mp_data, "municipality")
