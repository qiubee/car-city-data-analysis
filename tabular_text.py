from pathlib import Path
from os import chdir
import pandas as pd


def write_csv(data, filename):
    Path("data").mkdir(parents=True, exist_ok=True)
    chdir("data")
    file = f"{filename}.csv"
    data.to_csv(file)
    print(file, "is created in folder: data")


geo_postal_columns = ["countryCode", "postalCode", "placeName", "province", "adminCode1", "municipality", "adminCode2", "community", "adminCode3", "latitude", "longitude", "accuracy"]
nl_postal = pd.read_table("datasets/geonames/NL_full/NL_full.txt", header=None)
nl_postal.columns = geo_postal_columns
nl_postal = nl_postal.drop(nl_postal.columns[[4, 6, 7, 8, 11]], axis=1)
nl_postal = nl_postal.drop(nl_postal.iloc[:, :2], axis=1)

# nl_postal = nl_postal.drop_duplicates()
print(nl_postal)

# write_csv(nl_postal, "nl_postal")
