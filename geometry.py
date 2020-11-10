import geopandas as gp
import pandas as pd
import fiona

GPKG_FILE = "datasets/CBS/cbsgebiedsindelingen_2021_v1.gpkg"


def get_gpkg_layer_names(geopkg_src):
    layers = []
    for layername in fiona.listlayers(geopkg_src):
        layers.append(layername)
    return layers


layers = get_gpkg_layer_names(GPKG_FILE)
# print(layers)

landsdeel_2021_id = layers.index("cbs_landsdeel_2021_gegeneraliseerd")
gemeente_2021_id = layers.index("cbs_gemeente_2021_labelpoint")
gemeente_2020_id = layers.index("cbs_gemeente_2020_gegeneraliseerd")

GEMEENTE_2021_IND = layers[gemeente_2021_id]
LANDSDEEL_2021 = layers[landsdeel_2021_id]
GEMEENTE_2020_IND = layers[gemeente_2020_id]

data = gp.read_file(GPKG_FILE, layer=GEMEENTE_2021_IND)
print(data)
