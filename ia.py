import tensorflow as tf
import numpy as np
import pandas as pd
import time

def lector_excel(absorbancia_material,array_de_absorbancias,absorbancia_muestra):
    '''
    Funcion que lee el excel y procesa los datos
    '''
    #abrimos el archivo y la hoja de calibracion
    xlsx = pd.ExcelFile("Datos-UV-Visible.xlsx")
    df = pd.read_excel(xlsx, "UV - de Calibración")
    i = 1
    #ciclo durante todas las lineas o hasta que consiga 450 (por ser vidrio)
    while i < df.shape[0]:
        x = df.iloc[i,0]
        if x >= absorbancia_material:
            break
        i += 1
    j = 0
    #ciclo para asignar absorbancias de la linea cuando consigue 450
    while j < 7:
        array_de_absorbancias[j] = df.iloc[i,1 + 4*j]
        j+=1
    #ciclo durante las lineas restantes
    while i < df.shape[0]:
        j = 0
        while j < 7:
            if array_de_absorbancias[j] < df.iloc[i,1 + 4*j]:
                array_de_absorbancias[j] = df.iloc[i,1 + 4*j]
            j+=1
        i += 1
    #abrimos la hoja de muestra
    df = pd.read_excel(xlsx, "UV - Muestra")
    i = 1
    while i < df.shape[0]:
        x = df.iloc[i,0]
        if x >= absorbancia_material:
            break
        i += 1
    while i < df.shape[0]:
        if absorbancia_muestra[0] < df.iloc[i,1]:
            absorbancia_muestra[0] = df.iloc[i,1]
        i += 1


def red_neuronal(array_de_absorbancias,absorbancia_muestra):
    '''
    red neuronal
    '''
    #concentraciones
    Concentracion = np.array ([0.2, 0.5, 1, 2, 3, 4, 5], dtype=float)
    #configuraciones de la red neuronal
    capa = tf.keras.layers.Dense(units=1, input_shape=[1])
    modelo = tf.keras.Sequential([capa])
    modelo.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss="mean_squared_error")
    modelo.fit(array_de_absorbancias, Concentracion, epochs=1000, verbose=True)
    print(f"El entrenamiento ha terminado, hacienddo una prediccion con {absorbancia_muestra}")

    #prediccion
    resultado = modelo.predict([absorbancia_muestra])
    #Variables internas
    print("Las variales internas son:")
    print(capa.get_weights())
    print("El resultado es " + str(resultado[0][0]) + "ppm")

#main
array_de_absorbancias = np.zeros(7)
absorbancia_muestra = np.zeros(1)
lector_excel(450,array_de_absorbancias,absorbancia_muestra)
print("Universidad Simón Bolívar \nCreado por Andrea Delgado 18-10374 \nQM-2515 (introducción a la quimiometría)")
time.sleep(3)
print("\nEntrenando red neuronal, por favor espere", end="")
time.sleep(0.5)
print(".", end="")
time.sleep(0.5)
print(".", end="")
time.sleep(0.5)
print(".", end="")
red_neuronal(array_de_absorbancias,absorbancia_muestra)
