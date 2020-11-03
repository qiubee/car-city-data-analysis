import pandas as pd


def show_datasets(list):
    for dataset in datasets:
        dataset.head()
        print(dataset, "\n")


# datasets
M = pd.read_csv("datasets/RDW/GEBIEDSBEHEERDER.csv")
F = pd.read_csv("datasets/RDW/TARIEFDEEL.csv")
AREA = pd.read_csv("datasets/RDW/GEBIED.csv")

datasets = [M, F, AREA]

show_datasets(datasets)
