import pandas as pd
import matplotlib.pyplot as plt

# data
M = pd.read_csv("datasets/RDW/GEBIEDSBEHEERDER.csv")
F = pd.read_csv("datasets/RDW/TARIEFDEEL.csv")

managers = M.head(25)
fare = F.head(25)

managers = managers.drop(managers.columns[[2, 3, 4]], axis=1)
key = fare.columns[0]
combined = pd.merge(fare, managers, on=[key])
print(combined)
