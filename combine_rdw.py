import pandas as pd
from functools import reduce
from pathlib import Path
from os import chdir


def show_datasets(list):
    for dataset in datasets:
        dataset.head()
        print(dataset, "\n")


def get_duplicates(dataset_list):
    lst = []
    duplicates = set()
    for dataset in dataset_list:
        col_names = dataset.columns.values
        for name in col_names:
            lst.append(name)
    for i in lst:
        if lst.count(i) > 1:
            duplicates.add(i)
    return duplicates


def merge_dfs(data_frames, col_name, type="outer"):
    return reduce(lambda left, right: pd.merge(left, right, on=[col_name], how=type), data_frames)


# Wrapping around list https://stackoverflow.com/questions/22122623/wrapping-around-on-a-list-when-list-index-is-out-of-range
def wrap_list_index(list, add=1):
    result = []
    for i in range(len(list)):
        result.append(list.index(list[(i + add) % len(list)]))
    return result


def merge_on(data_frames, col_names):
    merged = []
    for i, df in enumerate(data_frames):
        r = (i + 1) % len(data_frames)
        df_set = [df, data_frames[r]]
        for key in col_names:
            try:
                merged = merge_dfs(df_set, key)
                print(f"Match: {key}")
            except KeyError:
                pass
    return merged


def write_csv(data, filename):
    Path("data").mkdir(parents=True, exist_ok=True)
    chdir("data")
    file = f"{filename}.csv"
    data.to_csv(file)
    print(file, "is created in folder: data")
    chdir("../")


# datasets
AREA_MAN = pd.read_csv("datasets/RDW/GEBIEDSBEHEERDER.csv")
FARE = pd.read_csv("datasets/RDW/TARIEFDEEL.csv")
AREA = pd.read_csv("datasets/RDW/GEBIED.csv")
INDEX = pd.read_csv("datasets/RDW/Index_Statisch_Dynamisch.csv")
P_OPEN = pd.read_csv("datasets/RDW/PARKING_OPEN.csv")
P_ACCESS = pd.read_csv("datasets/RDW/PARKING_TOEGANG.csv")
P_SPEC = pd.read_csv("datasets/RDW/SPECIFICATIES_PARKEERGEBIED.csv")
TIMEPERIOD = pd.read_csv("datasets/RDW/TIJDVAK.csv")
USEGOAL = pd.read_csv("datasets/RDW/GEBRUIKSDOEL.csv")

datasets = [AREA_MAN, FARE, AREA, INDEX, P_OPEN, P_ACCESS, P_SPEC, TIMEPERIOD, USEGOAL]
dupl = get_duplicates(datasets)
print("Duplicate keys:", dupl)

merged_dfs = merge_on(datasets, dupl)
AREA_MAN_ID = merge_dfs([P_OPEN, AREA], "AreaManagerId", "inner")
all_data = merge_dfs([merged_dfs, AREA_MAN_ID], "AreaManagerId", "inner")

rename_col = {"UsageId_y": "UsageType_Id", "AreaId_x": "AreaZone_Id"}
remove_col = ["SpecificationIndicator", "SuperiorAreaManagerId", "StartDateAreaManagerId", "EndDateAreaManagerId", "StartOfPeriod", "EndOfPeriod", "StartDateArea", "EndDateArea", "AreaId_y", "UsageId_x", "PeriodName", "URL"]

all_data = all_data.drop(columns=remove_col, axis=1)
all_data = all_data.rename(columns=rename_col)

all_data["ExitPossibleAllDay"] = all_data["ExitPossibleAllDay"].replace([1, 0], [True, False])
all_data["OpenAllYear"] = all_data["OpenAllYear"].replace([1.0, 0.0], [True, False]).fillna(False)

write_csv(all_data, "RDW_dataset")
