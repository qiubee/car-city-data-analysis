from pathlib import Path
from os import chdir
import pandas as pd


def write_csv(data, filename):
    Path("data").mkdir(parents=True, exist_ok=True)
    chdir("data")
    file = f"{filename}.csv"
    data.to_csv(file)
    print(file, "is created in folder: data")


nl_postal_columns = ["CountryCode", "PostalCode", "Place", "Province", "ProvinceId", "f", "g", "h", "i", "Lat", "Long", "l"]
nl_postal = pd.read_table("datasets/geonames/NL_full/NL_full.txt", header=None)
nl_postal.columns = nl_postal_columns
nl_postal = nl_postal.drop(nl_postal.columns[[0, 4, 5, 6, 7, 8, 11]], axis=1)
nl_postal.index.name = "Id"
write_csv(nl_postal, "nl_postal")
