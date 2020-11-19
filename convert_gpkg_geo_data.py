from pathlib import Path
from os import chdir
import geopandas as gpd
import pandas as pd
import fiona

# geometry projection is already set to EPSG:28992
GPKG_FILE = "datasets/CBS/cbsgebiedsindelingen_2021_v1.gpkg"


def get_gpkg_layer_names(geopkg_src):
    layers = []
    for layername in fiona.listlayers(geopkg_src):
        layers.append(layername)
    return layers


def drop_df_columns(df, columns):
    return df.drop(df.columns[columns], axis=1)


def write_csv(data, filename):
    Path("data").mkdir(parents=True, exist_ok=True)
    chdir("data")
    file = f"{filename}.csv"
    data.to_csv(file, index=False)
    print(file, "is created in folder: data")
    chdir("../")


def process_gpkg_layer(gpkg_file, all_layers, layer_name, column_drop_list):
    layer_id = all_layers.index(layer_name)
    df = gpd.read_file(gpkg_file, layer=layer_id)
    df = drop_df_columns(df, column_drop_list)
    # set crs to WSG 84 (lat/long)
    df = df.to_crs(crs=4326)
    write_csv(df, layer_name)


def process_gpkg_multi(gpkg_file, layers, col_drop_lst):
    all_layers = get_gpkg_layer_names(gpkg_file)
    for layer in layers:
        process_gpkg_layer(gpkg_file, all_layers, layer, col_drop_lst)


pv = "cbs_provincie_2020_gegeneraliseerd"
gm = "cbs_gemeente_2020_gegeneraliseerd"

col_drop_lst = [0, 1, 3]
layers = [pv, gm]
process_gpkg_multi(GPKG_FILE, layers, col_drop_lst)
