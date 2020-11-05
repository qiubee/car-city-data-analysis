import pandas as pd


# data
ISD = pd.read_csv("datasets/RDW/Index_Statisch_Dynamisch.csv")
GB_BH = pd.read_csv("datasets/RDW/GEBIEDSBEHEERDER.csv")
GB_SPEC = pd.read_csv("datasets/RDW/SPECIFICATIES_PARKEERGEBIED.csv")


def data_head(data):
    return data.head()


isd_hd = data_head(ISD)
gb_bh_hd = data_head(GB_BH)
gb_spec_hd = data_head(GB_SPEC)

print(isd_hd.columns.values)
print(isd_hd)

isd_hd_dp = isd_hd.drop(isd_hd.columns[[3, 4, 6]], axis=1)
print(isd_hd_dp, "\n")
print(isd_hd)

isd_hd_dp.iloc[:, 3] = isd_hd_dp.iloc[:, 3].fillna(False)
print(isd_hd_dp, "\n")

print(gb_bh_hd.columns.values, "\n")
print(gb_bh_hd)

print(gb_spec_hd.columns.values, "\n")
print(gb_spec_hd)
