import pandas as pd
from pathlib import Path
from os import chdir

NL_POSTAL = pd.read_csv("data/nl_postal.csv")
RDW_DATASET = pd.read_csv("data/RDW_dataset.csv")


def write_csv(data, filename):
    Path("data").mkdir(parents=True, exist_ok=True)
    chdir("data")
    file = f"{filename}.csv"
    data.to_csv(file)
    print(file, "is created in folder: data")
    chdir("../")


nl_postal_codes = NL_POSTAL.rename(columns={"Place": "AreaManagerDesc"})
nl_postal_codes = nl_postal_codes.drop(nl_postal_codes.columns[[0, 4, 5]], axis=1)

# combined = pd.DataFrame()
# for i, chunk in enumerate(pd.read_csv("data/RDW_dataset.csv", chunksize=10**4)):
# 	combined = pd.merge(chunk, nl_postal_codes, how="left", on="AreaManagerDesc")
# 	print(f"Merging on chunk: {i}")
# 	print(combined)

combined = pd.merge(RDW_DATASET, nl_postal_codes, how="left", on="AreaManagerDesc")
print(combined)
