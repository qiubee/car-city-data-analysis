import geopandas as gp

GEBIED_IND = gp.read_file("datasets/CBS/cbsgebiedsindelingen_2021_v1.gpkg")
print(GEBIED_IND)
