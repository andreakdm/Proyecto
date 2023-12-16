import pandas as pd
import numpy as np

# Carga el archivo de Excel
xlsx = pd.ExcelFile("Datos-UV-Visible.xlsx")
df = pd.read_excel(xlsx, "UV - de Calibración")
print(df.iloc[261,9])
i = 1
while i < 912:
    x = df.iloc[i,0]
    if x == 450:
        break
    i += 1
array_de_absorbancias = np.zeros(7)
j = 0
while j < 7:
    array_de_absorbancias[j] = df.iloc[i,1 + 4*j]
    j+=1
array_auxiliar = np.zeros(7)
x = 1
vacio = df.iloc[0,3]
while i < df.shape[0]:
    j = 0
    while j < 7:
        if array_de_absorbancias[j] < df.iloc[i,1 + 4*j]:
            array_de_absorbancias[j] = df.iloc[i,1 + 4*j]
        j+=1
    i += 1


print(array_de_absorbancias)
