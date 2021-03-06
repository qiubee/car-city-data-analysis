# Auto's in Nederland - Data analysis

This repo is intended for data cleaning and data analysis. Making use of Python to import raw data from a file, clean the data and export as a json file so it can be used in d3 and JavaScript. For creating datavisualizations for de Volkskrant the data has to be converted and cleaned to make it accessable and usable for visialization with d3.

## Requirements

* Python >= 3.6
* [`pandas`](https://pandas.pydata.org/)
* [`geopandas`](https://github.com/geopandas/geopandas)
* [`geojson`](https://github.com/jazzband/geojson)

## Datasets

Public datasets used for data analysis.

### RDW

The datasets from [RDW](https://opendata.rdw.nl/):

* [Open Data Parkeren: GEBIED](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-GEBIED/adw6-9hsg)
* [Open Data Parkeren: GEBIEDSBEHEERDER](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-GEBIEDSBEHEERDER/2uc2-nnv3)
* [Open Data Parkeren: GEBRUIKSDOEL](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-GEBRUIKSDOEL/qidm-7mkf)
* [GEO Parkeer Garages](https://opendata.rdw.nl/Parkeren/GEO-Parkeer-Garages/t5pc-eb34)
* [Open Data Parkeren: GEOMETRIE GEBIED](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-GEOMETRIE-GEBIED/nsk3-v9n7)
* [Open Data Parkeren: Index Statisch en Dynamisch](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-Index-Statisch-en-Dynamisch/f6v7-gjpa)
* [Open Data Parkeren: PARKING OPEN](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-PARKING-OPEN/figd-gux7)
* [Open Data Parkeren: PARKING TOEGANG](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-PARKING-TOEGANG/edv8-qiyg)
* [Open Data Parkeren: SPECIFICATIES PARKEERGEBIED](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-SPECIFICATIES-PARKEERGEBIED/b3us-f26s)
* [Open Data Parkeren: TARIEFDEEL](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-TARIEFDEEL/534e-5vdg)
* [Open Data Parkeren: TIJDVAK](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-TIJDVAK/ixf8-gtwq)
* [Open Data Parkeren: PARKEERGEBIED](https://opendata.rdw.nl/Parkeren/Open-Data-Parkeren-PARKEERGEBIED/mz4f-59fw)

### CBS

* [Geografische data](https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data)
* [CBS gebiedsindelingen](https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data/cbs-gebiedsindelingen)

### GeoNames

* [GeoNames Data - countries](https://download.geonames.org/export/zip/)

## Resources

* [Merge Dataframes](https://realpython.com/pandas-merge-join-and-concat/)
* [Merge, join, concatenate and compare - Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html)
* [Matplotlib - sample plots](https://matplotlib.org/tutorials/introductory/sample_plots.html#sphx-glr-tutorials-introductory-sample-plots-py)
* [Python: pandas merge multiple dataframes](https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes)
* [Find duplicates in a list](https://shoutthegeek.com/how-to-find-duplicates-in-a-list-in-python/?PageSpeed=noscript)
* [Wrapping around list index - Stackoverflow](https://stackoverflow.com/questions/22122623/wrapping-around-on-a-list-when-list-index-is-out-of-range)
* [How can I safely create a nested directory - Stackoverflow](https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory)
* [How To Install GDAL/OGR Packages](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html)
* [Installing modules from source code - Harvard University](https://rce-docs.hmdc.harvard.edu/book/installing-modules-source-code)
* [Can geopandas get a geopackage's (or other vector file) all layers? - Stackoverlfow](https://stackoverflow.com/questions/56165069/can-geopandas-get-a-geopackages-or-other-vector-file-all-layers)
* [Understanding Geonames dump](https://www.logilab.org/blogentry/10074668)
* [Transforming a polygon to a linestring](https://gis.stackexchange.com/questions/290756/transforming-a-polygon-to-a-linestring/332157)
* [Python Dictionary Comprehension Tutorial](https://www.datacamp.com/community/tutorials/python-dictionary-comprehension)
* [Group Array of JavaScript Objects by Key or Property Value](https://gist.github.com/JamieMason/0566f8412af9fe6a1d470aa1e089a752)
* [Convert GeoJSON to/from WKT in Python](https://gist.github.com/drmalex07/5a54fc4f1db06a66679e)
* [Geospatial adventures. Step 2: Pandas vs. GeoPandas - Towards Data Science](https://towardsdatascience.com/geospatial-adventures-step-2-pandas-vs-geopandas-16e842d0e3a7?gi=e40afba336b6)
* [EPSG:28992 - Spatial Reference](https://spatialreference.org/ref/epsg/28992/)
