import pandas as pd
from functools import reduce


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


def merge_dfs(data_frames, col_name):
    return reduce(lambda left, right: pd.merge(left, right, on=[col_name], how="outer"), data_frames)


def wrap_list_index(list, add=1):
    result = []
    for i in range(len(list)):
        result.append(list.index(list[(i + add) % len(list)]))
    return result


def merge_on(data_frames, col_names):
    merged = []
    print(data_frames.index(0))
    # for i, df in enumerate(data_frames):
        # lst = wrap_list_index(data_frames, 1)
        # print(lst[i])
        # df_set = [df, data_frames[i + 1]]
        # for key in col_names:
        #     try:
        #         merged = merge_dfs(df_set, key)
        #         print(f"Match: {key}")
        #     except:
        #         pass
    return merged


# datasets
AREA_MAN = pd.read_csv("../datasets/RDW/GEBIEDSBEHEERDER.csv")
FARE = pd.read_csv("../datasets/RDW/TARIEFDEEL.csv")
AREA = pd.read_csv("../datasets/RDW/GEBIED.csv")
INDEX = pd.read_csv("../datasets/RDW/Index_Statisch_Dynamisch.csv")
P_OPEN = pd.read_csv("../datasets/RDW/PARKING_OPEN.csv")
P_ACCESS = pd.read_csv("../datasets/RDW/PARKING_TOEGANG.csv")
P_SPEC = pd.read_csv("../datasets/RDW/SPECIFICATIES_PARKEERGEBIED.csv")
TIMEPERIOD = pd.read_csv("../datasets/RDW/TIJDVAK.csv")
USEGOAL = pd.read_csv("../datasets/RDW/GEBRUIKSDOEL.csv")

datasets = [AREA_MAN, FARE, AREA, INDEX, P_OPEN, P_ACCESS, P_SPEC, TIMEPERIOD, USEGOAL]
show_datasets(datasets)

dupl = get_duplicates(datasets)
print(dupl)

merge_on(datasets, dupl)
