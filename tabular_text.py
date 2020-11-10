from pathlib import Path
from os import chdir
import pandas as pd


def write_csv(data, filename):
    Path("data").mkdir(parents=True, exist_ok=True)
    chdir("data")
    file = f"{filename}.csv"
    data.to_csv(file)
    print(file, "is created in folder: data")


columns = ["ItemNumber", "PlaceName", "AreaName", "Namings", "Lat", "Long", "g", "h", "CountryCode", "j", "k", "l", "m", "n", "o", "p", "q", "Capital", "DateOfInput"]
geo_names = pd.read_table("datasets/geonames/NL/NL.txt", header=None)
geo_names.columns = columns
print(geo_names)
write_csv(geo_names, "nl")
