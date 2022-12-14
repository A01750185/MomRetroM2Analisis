# -*- coding: utf-8 -*-
"""MomRetroM2Analisis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DDSsOQmPSIv5WrOiqW87OKUngBuYVwsE

**Amy Murakami Tsutsumi - A01750185**

# **Momento de Retroalimentación: Módulo 2 Análisis y Reporte sobre el Desempeño del Modelo (Portafolio Análisis)**

Para este portafolio de implementación se utilizará el dataset de "Heart Failure Prediction Dataset" que se obtuvo de la siguiente liga: 
https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction

Este dataset contiene información con atributos que se utilizarán para determinar y predecir si una persona es propensa a tener un ataque cardiaco. Estos atributos son: 
1. Age: edad del paciente 
2. Sex: sexo del paciente [M: Hombre, F: Mujer]
3. ChestPainType: tipo de dolor en el pecho [TA: Angina típica, ATA: Angina atípica, NAP: Dolor no anginoso, ASY: Asintomático]
4. RestingBP: presión arterial en reposo [mm Hg]
5. Cholesterol: colesterol sérico [mm/dl]
6. FastingBS: glucemia en ayunas [1: si FastingBS > 120 mg/dl, 0: en caso contrario]
7. RestingECG: resultados del electrocardiograma [Normal: Normal, ST: con anormalidad de la onda ST-T (inversiones de la onda T y/o elevación o depresión del ST de > 0,05 mV), HVI: que muestra hipertrofia ventricular izquierda probable o definitiva según los criterios de Estes].
8. MaxHR: frecuencia cardíaca máxima alcanzada [Valor numérico entre 60 y 202]
9. ExerciseAngina: angina inducida por el ejercicio [Y: Sí, N: No]
10. Oldpeak: oldpeak = ST [Valor numérico medido en depresión]
11. ST_Slope: la pendiente del segmento ST máximo del ejercicio [Up: pendiente ascendente, Flat: plano, Down: pendiente descendente]
12. HeartDisease: clase de salida [1: enfermedad cardiaca, 0: Normal]

Este dataset cuenta con 918 registros de pacientes.

El algoritmo que se utilizará para este análisis es el de redes neuronales utilizando la librería sklearn.neural_network.

### **Lectura de Datos**
"""

# Commented out IPython magic to ensure Python compatibility.
"""
from google.colab import drive
drive.mount("/content/gdrive") 
# %cd "/content/gdrive/MyDrive/Séptimo Semestre/Mod2"
"""

"""Las librerías que se utilizarán son: 
* *pandas* : Para la creación y operaciones de dataframes.
* *numpy* : Para la creación de vectores y matrices.
* *sklearn.neural_network - MLPClassifier* : Para la implementación del algoritmo de redes neuronales. 
* *sklearn.preprocessing - StandardScaler* : Para el escalamiento de datos.
* *sklearn.model_selection - train_test_split* : Para la división de los datos en subconjuntos de entrenamiento y prueba.
* *sklearn.metrics - confusion_matrix & classification_report* : Para la visualización de desempeño del algoritmo y las métricas de clasificación.
* *matplotlib.pyplot* : Para la generación de gráficos.
* *seaborn* : Basada en matplotlib para la graficación de datos estadísticos.
* *mlxtend.plotting - plot_learning_curves*: Para la graficación de las learning curves.

"""

# Librerías
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.plotting import plot_learning_curves
df = pd.read_csv('heart.csv')

"""### **Entendimiento de los datos**"""

df.head()

"""#### Visualización de los datos"""

# Visualizar las personas que son propensas a enfermedades cardiacas. 
sns.countplot(df['HeartDisease'])

"""La gráfica anterior muestra la cantidad de pacientes que tienen y los que no tienen enfermedades cardiacas. """

# HeartDisease por columna
cols = ['Sex', 'ChestPainType', 'RestingECG', 'FastingBS', 'ExerciseAngina', 'ST_Slope']

n_rows = 2
n_cols = 3

# Tamaño de la gráfica
fig, axs = plt.subplots(n_rows, n_cols, figsize=(n_cols*3.2,n_rows*3.2))

for r in range(0,n_rows):
    for c in range(0,n_cols):  
        
        i = r*n_cols+ c # indice     
        ax = axs[r][c] # Posición de cada subplot
        sns.countplot(df[cols[i]], hue=df["HeartDisease"], ax=ax, palette="BuPu")
        ax.set_title(cols[i])
        ax.legend(title="HeartDisease", loc='upper right') 
        
plt.tight_layout()

"""Las gráficas anteriores muestran la relación de los datos cualitativos con el valor real (HeartDisease). Podemos notar que a simple vista todos los atributos cualitativos tienen importancia para la predicción que se realizará más adelante. """

sns.set()
sns.pairplot(df, hue='HeartDisease', size=1.5, palette="CMRmap_r");

"""Las gráficas muestran la relación entre los valores cuantitativos con el valor real (HeartDisease). A simple vista podemos notar que todas los atributos cuantitativos son importantes para realizar las predicciones.

#### Análisis de los datos
"""

df.info()

"""Como se puede observar, existen atributos no numéricos como: Sex, ChestPainType, RestingECG, ExerciseAngina y ST_Slope que se deberán converitr en valores numéricos. """

# Obtenemos el total de los valores nulos y los ordenamos de mayor a menor
total = df.isnull().sum().sort_values(ascending=False)
print(total)

"""Ya que no existen valores nulos, no es necesario realizar una limpieza de valores NAN.

Ahora visualizaremos el comportamiento y las correlaciones que existen en los datos. 
"""

# Matriz de Correlación
corr = df.corr()
corr.style.background_gradient(cmap='coolwarm')

"""Al analizar esta matriz de correlación podemos notar que los atributos que tienen mayor correlación con HeartDisease son MaxHR y Oldpeak. Sin embargo, al no contar con un dataset con puros datos numéricos se están omitiendo varios atributos.

### **Preprocesamiento**

Ahora se convertiran las variables cualitativas en cuantitativas para poder utilizarlas en las predicciones.
"""

# Cuantificar las variables no numéricas
dummy_Sex = pd.get_dummies(df['Sex'], prefix='Sex')
dummy_ChestPainType = pd.get_dummies(df['ChestPainType'])
dummy_RestingECG = pd.get_dummies(df['RestingECG'])
dummy_ExerciseAngina = pd.get_dummies(df['ExerciseAngina'], prefix="ExAn")
dummy_STSlope = pd.get_dummies(df['ST_Slope'])

# Concatenar las nuevas columnas
dfHeart = pd.concat([df, dummy_Sex, dummy_ChestPainType, dummy_RestingECG, 
                          dummy_ExerciseAngina, dummy_STSlope], axis=1)
dfHeart = dfHeart.drop(['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope', 'Sex_F', 'ExAn_N'], axis=1)
dfHeart.head()

"""La tabla anterior muestra todos los atributos con valores cuantitativos. Por lo tanto, volveremos a realizar la matriz de correlación para considerar los nuevos datos. """

corr = dfHeart.corr()
corr.style.background_gradient(cmap='coolwarm')

"""La matriz indica que los atributos con mayor correlación con HeartDisease son ASY, Flat y Up.

### **Escalamiento de datos, separación y evaluación del modelo con un conjunto de prueba y uno de validación (Train/Test/Validation)**

Ahora se realizará el escalamiento de datos para que los modelos puedan encontrar facilmente convergencia entre los datos. Esto se realiza con fin de optimizar el método.
"""

# Separar el dataframe 
df_x = dfHeart.drop(['HeartDisease'] ,axis=1)
df_y = dfHeart['HeartDisease']

# Escalamiento 
escalador_fill = StandardScaler()
escalador_fill.fit(df_x)
dt_x = pd.DataFrame(escalador_fill.transform(df_x))

#Modularización del data-set
x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size = 0.20, random_state= 2)
x_train2, x_val, y_train2, y_val = train_test_split(x_train, y_train, test_size = 0.20, random_state= 2)

"""### **Modelos de predicción**

Ahora se realizarán 5 modelos diferentes de redes neuronales para encontrar el más eficiente.
"""

modelo1 = MLPClassifier(random_state = 1,
                                  hidden_layer_sizes = (5),
                                  activation = "relu",
                                  verbose = False,
                                  solver = "adam",
                                  learning_rate = "adaptive", 
                                  max_iter = 10000)

modelo2 = MLPClassifier(random_state = 1,
                                  hidden_layer_sizes = (10, 9),
                                  activation = "relu",
                                  verbose = False,
                                  solver = "adam",
                                  learning_rate = "adaptive", 
                                  max_iter = 10000)

modelo3 = MLPClassifier(random_state = 1,
                                  hidden_layer_sizes = (10, 8, 10),
                                  activation = "relu",
                                  verbose = False,
                                  solver = "adam",
                                  learning_rate = "adaptive", 
                                  max_iter = 10000)

modelo4 = MLPClassifier(random_state = 1,
                                  hidden_layer_sizes = (10, 15, 10, 4),
                                  activation = "relu",
                                  verbose = False,
                                  solver = "adam",
                                  learning_rate = "adaptive", 
                                  max_iter = 10000)

modelo5 = MLPClassifier(random_state = 1,
                                  hidden_layer_sizes = (10, 9, 9, 10),
                                  activation = "relu",
                                  verbose = False,
                                  solver = "adam",
                                  learning_rate = "adaptive", 
                                  max_iter = 10000)

modelo1.fit(x_train, y_train)
modelo2.fit(x_train, y_train)
modelo3.fit(x_train, y_train)
modelo4.fit(x_train, y_train)
modelo5.fit(x_train, y_train)

print("Training score modelo 1: ", modelo1.score(x_train,y_train))
print("Validation score modelo 1: ", modelo1.score(x_val, y_val))
print("Test score modelo 1: ", modelo1.score(x_test, y_test))

print("\nTraining score modelo 2: ", modelo2.score(x_train,y_train))
print("Validation score modelo 2: ", modelo2.score(x_val, y_val))
print("Test score modelo 2: ", modelo2.score(x_test, y_test))

print("\nTraining score modelo 3: ", modelo3.score(x_train,y_train))
print("Validation score modelo 3: ", modelo3.score(x_val, y_val))
print("Test score modelo 3: ", modelo3.score(x_test, y_test))

print("\nTraining score modelo 4: ", modelo4.score(x_train,y_train))
print("Validation score modelo 4: ", modelo4.score(x_val, y_val))
print("Test score modelo 4: ", modelo4.score(x_test, y_test))

print("\nTraining score modelo 5: ", modelo5.score(x_train,y_train))
print("Validation score modelo 5: ", modelo5.score(x_val, y_val))
print("Test score modelo 5: ", modelo5.score(x_test, y_test))

"""Podemos visualizar que los modelos 1, 3 y 5 son los más precisos con los datos de entrenamiento. Sin embargo, los modelos más precisos con los datos de validación son el 1 y 5. Además los modelos más preciso para los datos de 
prueba son el 2, 4 y 5.

### **Predicciones**

Ahora se realizarán las predicciones de los cinco modelos.
"""

pred1 = modelo1.predict(x_test)
pred2 = modelo2.predict(x_test)
pred3 = modelo3.predict(x_test)
pred4 = modelo4.predict(x_test)
pred5 = modelo5.predict(x_test)

"""La siguiente tabla muestra los valores de entrada de las predicciones, el valor real esperado, los resultados de las predicciones y validación del modelo que indica si el valor real esperado es el mismo que el de la predicción. """

pd.set_option('max_columns', None)
dfEntPred = x_test.copy()
dfEntPred["Valor Real Esperado"] = y_test
dfEntPred["Predicción Modelo 1"] = pred1
dfEntPred["Validación Pred 1"] = np.where(dfEntPred["Valor Real Esperado"] == dfEntPred["Predicción Modelo 1"], "✅" , "❌")        
dfEntPred["Predicción Modelo 2"] = pred2
dfEntPred["Validación Pred 2"] = np.where(dfEntPred["Valor Real Esperado"] == dfEntPred["Predicción Modelo 2"], "✅" , "❌")     
dfEntPred["Predicción Modelo 3"] = pred3
dfEntPred["Validación Pred 3"] = np.where(dfEntPred["Valor Real Esperado"] == dfEntPred["Predicción Modelo 3"], "✅" , "❌") 
dfEntPred["Predicción Modelo 4"] = pred4
dfEntPred["Validación Pred 4"] = np.where(dfEntPred["Valor Real Esperado"] == dfEntPred["Predicción Modelo 4"], "✅" , "❌")  
dfEntPred["Predicción Modelo 5"] = pred5
dfEntPred["Validación Pred 5"] = np.where(dfEntPred["Valor Real Esperado"] == dfEntPred["Predicción Modelo 5"], "✅" , "❌")               
dfEntPred.head()

#Modelo 1
print('Modelo 1: ')
print(modelo1.predict_proba([df_x.loc[0]]))
print('Heart Disease? Estimated: ', modelo1.predict([df_x.loc[0]]),
      'Real: ', df_y.loc[0])
#Modelo 2
print('\nModelo 2: ')
print(modelo2.predict_proba([df_x.loc[0]]))
print('Heart Disease? Estimated: ', modelo2.predict([df_x.loc[0]]),
      'Real: ', df_y.loc[0])
#Modelo 3
print('\nModelo 3: ')
print(modelo3.predict_proba([df_x.loc[0]]))
print('Heart Disease? Estimated: ', modelo3.predict([df_x.loc[0]]),
      'Real: ', df_y.loc[0])
#Modelo 4
print('\nModelo 4: ')
print(modelo4.predict_proba([df_x.loc[0]]))
print('Heart Disease? Estimated: ', modelo4.predict([df_x.loc[0]]),
      'Real: ', df_y.loc[0])
#Modelo 5
print('\nModelo 5: ')
print(modelo5.predict_proba([df_x.loc[0]]))
print('Heart Disease? Estimated: ', modelo5.predict([df_x.loc[0]]),
      'Real: ', df_y.loc[0])

"""Podemos observar que en todos los modelos se está realizando la predicción de manera correcta. Como primer valor muestra la probabilidad de que el HeartDisease tenga un valor de 0 y 1. Después se muestra el valor estimado con los modelos y el valor real. En todos los modelos coinciden que el valor estimado por cada modelo y el valor real es 0, por lo que se puede confirmar que son modelos efectivos para la predicción de enfermedades cardiacas.

### **Validación**

Para la etapa de validación se utilizarán matrices de confusión y reportes de clasificación.
"""

#Modelo 1
print('Modelo 1: ')
sns.set()
f, ax = plt.subplots()
matriz1 = confusion_matrix(y_test,pred1)
print(classification_report(y_test,pred1))
print('\nMatriz de confusión: ')
sns.heatmap(matriz1, annot=True, ax=ax, cbar=False, fmt='g', cmap='Dark2_r')

"""Para el primer modelo podemos observar que el valor de f1-score es 0.81 lo que indica que es un buen modelo de predicción. Por otro lado, en la matriz de confusión se tienen 67 valores true positive y 82 valores true negative; es decir, valores predecidos que coinciden con el valor real. Además, se tienen 22 valores false positive y 13 false negative es decir valores erróneos."""

#Modelo 2
print('Modelo 2: ')
sns.set()
f, ax = plt.subplots()
matriz2 = confusion_matrix(y_test,pred2)
print(classification_report(y_test,pred2))
print('\nMatriz de confusión: ')
sns.heatmap(matriz2, annot=True, ax=ax, cbar=False, fmt='g', cmap='Paired')

"""Para el segundo modelo podemos observar que el valor de f1-score es 0.84 lo que indica que es un mejor modelo de predicción que el primero. Por otro lado, en la matriz de confusión se tienen 69 valores true positive y 86 valores true negative; es decir, valores predecidos que coinciden con el valor real. Además, se tienen 20 valores false positive y 9 false negative es decir valores erróneos."""

#Modelo 3
print('Modelo 3: ')
sns.set()
f, ax = plt.subplots()
matriz3 = confusion_matrix(y_test,pred3)
print(classification_report(y_test,pred3))
print('\nMatriz de confusión: ')
sns.heatmap(matriz3, annot=True, ax=ax, cbar=False, fmt='g', cmap='Pastel1')

"""Para el tercer modelo podemos observar que el valor de f1-score es 0.82 lo que indica que es un buen modelo, pero no tiene la misma precisión que el segundo. Por otro lado, en la matriz de confusión se tienen 68 valores true positive y 83 valores true negative; es decir, valores predecidos que coinciden con el valor real. Además, se tienen 21 valores false positive y 12 false negative es decir valores erróneos."""

#Modelo 4
print('Modelo 4: ')
sns.set()
f, ax = plt.subplots()
matriz4 = confusion_matrix(y_test,pred4)
print(classification_report(y_test,pred4))
print('\nMatriz de confusión: ')
sns.heatmap(matriz4, annot=True, ax=ax, cbar=False, fmt='g', cmap='Pastel2')

"""Para el cuarto modelo podemos observar que el valor de f1-score es 0.84 lo que indica que es de los mejores modelos hasta ahora. Por otro lado, en la matriz de confusión se tienen 67 valores true positive y 88 valores true negative; es decir, valores predecidos que coinciden con el valor real. Además, se tienen 22 valores false positive y 7 false negative es decir valores erróneos."""

#Modelo 5
print('Modelo 5: ')
sns.set()
f, ax = plt.subplots()
matriz5 = confusion_matrix(y_test,pred5)
print(classification_report(y_test,pred5))
print('\nMatriz de confusión: ')
sns.heatmap(matriz5, annot=True, ax=ax, cbar=False, fmt='g', cmap='PuRd')

"""Por último, para el quinto modelo podemos observar que el valor de f1-score es 0.84 lo que indica que es de los mejores modelos junto con el modelo 2 y 4. Por otro lado, en la matriz de confusión se tienen 71 valores true positive y 84 valores true negative; es decir, valores predecidos que coinciden con el valor real. Además, se tienen 18 valores false positive y 11 false negative es decir valores erróneos."""

fig, ax =plt.subplots(1,2)
sns.countplot(pred4, ax=ax[0], palette="Accent")
sns.countplot(y_test, ax=ax[1], palette="RdBu_r")
fig.show()

"""En la gráfica anterior se muestra del lado izquierdo los número de valores predecidos con el modelo cuatro y del lado derecho los valores reales. Se puede observar que los datos predecidos con valor 1 se acercan bastante a los valores reales. Sin embargo, hay una diferencia significativa en los valores igual a cero.

### **Análisis**

#### Diagnóstico sobre el nivel de ajuste del modelo

Ahora se graficaran las learning curves para determinar si es underfitting u overfitting.
Primero graficaremos las learning curves utilizando los datos de entrenamiento y pruebas para el modelo 4 que fue el más preciso.
"""

plot_learning_curves(x_train, y_train, x_test, y_test, modelo4)
plt.title("Modelo 4 Learning Curves (train y test)")
plt.show()

"""Podemos observar que tanto los valores de training como los del test son muy similares, esto significa que el error es mínimo. """

plot_learning_curves(x_train, y_train, x_val, y_val, modelo4)
plt.title("Modelo 4 Learning Curves (train y validation)")
plt.show()

from sklearn import metrics
print("Error absoluto medio:", metrics.mean_absolute_error(y_test, pred4))
print("Error cuadrático medio: ", metrics.mean_squared_error(y_test, pred4))

"""Podemos observar que tanto los valores de training como los de validation son muy similares. Por lo tanto, se podría decir que el modelo está bien ajustado ya que el error tanto del training y del test es bajo. En este caso, el error absoluto es de 0.1576. De hecho, debido a que el error del test es más bajo que el del training se podría decir que el modelo está generalizando bien, porque lo que aprende en la etapa de entrenamiento lo utiliza en el test.

#### Diagnóstico del grado de bias o sesgo: bajo medio alto

Debido a que en el diagnóstico sobre el nivel de ajuste del modelo se obtuvo que el modelo estaba bien ajustado y el error absoluto medio fue de 0.1576, entonces se puede concluir que el modelo tiene un sesgo o bias bajo porque tiene un mínimo de error.

#### Diagnóstico del grado de varianza: bajo medio alto

Debido a que en el diagnóstico sobre el nivel de ajuste del modelo se obtuvo que el modelo estaba bien ajustado y el error medio absoluto fue de 0.1576, entonces se puede concluir que el modelo tiene una varianza baja. Por lo tanto, existe un pequeño desajuste lo que hace que el modelo tenga un rendimiento predictivo un poco deficiente.

#### Técnicas de regularización o el ajuste de parámetros para mejorar el desempeño del modelo

Debido a que ambas gráficas de learning curves mostraron que el modelo 4 está bien ajustado, pero tiene un grado de sesgo y varianza bajo entonces se implementará un modelo más con mayor complejidad.
"""

modelo6 = MLPClassifier(random_state = 1,
                                  hidden_layer_sizes = (10, 16, 10, 10, 10, 9, 15, 10, 10),
                                  activation = "relu",
                                  verbose = False,
                                  solver = "adam",
                                  learning_rate = "adaptive", 
                                  max_iter = 10000)

modelo6.fit(x_train, y_train)

print("Training score modelo 6: ", modelo6.score(x_train,y_train))
print("Validation score modelo 6: ", modelo6.score(x_val, y_val))
print("Test score modelo 6: ", modelo6.score(x_test, y_test))

"""Como muestran los datos anteriores, el modelo 6 es preciso, pero los valores obtenidos son muy parecidos a los primeros cinco modelos. Por lo tanto, se realizarán las learning curves para analizar el nuevo modelo. """

plot_learning_curves(x_train, y_train, x_test, y_test, modelo6)
plt.title("Modelo 6 Learning Curves (train y test)")
plt.show()

plot_learning_curves(x_train, y_train, x_val, y_val, modelo6)
plt.title("Modelo 6 Learning Curves (train y validation)")
plt.show()

pred6 = modelo6.predict(x_test)
print("Error absoluto medio:", metrics.mean_absolute_error(y_test, pred6))
print("Error cuadrático medio: ", metrics.mean_squared_error(y_test, pred6))

"""Las gráficas anteriores muestran una mejora significativa de los datos. Sobre todo en la gráfica con los datos de entrenamiento y prueba. Ya que el modelo tiene un buen balance, tiene un error aceptable en el entrenamiento y un error aceptable de generalización en el subset de validación que son menores al error del modelo 4. Incluso, el error absoluto de este modelo (0.15217391304347827) es menor que el error absoluto del modelo 4 (0.15760869565217392). Por lo tanto, muestra un diagnóstico deseado.

#### Comparación del desempeño del modelo antes y después de incluir las mejoras

Para comparar el desempeño del modelo antes y después se utilizarán el modelo 1 y modelo 4 implementados antes de las modificaciones y el modelo 6 en el que se ajustaron los parámetros para mejorar su desempeño.
"""

print("Modelo 1")
print("Training score modelo 1: ", modelo1.score(x_train,y_train))
print("Validation score modelo 1: ", modelo1.score(x_val, y_val))
print("Test score modelo 1: ", modelo1.score(x_test, y_test))

print("\nModelo 4")
print("Training score modelo 4: ", modelo4.score(x_train,y_train))
print("Validation score modelo 4: ", modelo4.score(x_val, y_val))
print("Test score modelo 4: ", modelo4.score(x_test, y_test))

print("\nModelo 6")
print("Training score modelo 6: ", modelo6.score(x_train,y_train))
print("Validation score modelo 6: ", modelo6.score(x_val, y_val))
print("Test score modelo 6: ", modelo6.score(x_test, y_test))

"""Como se puede observar tanto los valores de training score y validation score del modelo 1 es más preciso que los otros modelos. Sin embargo, la precisión del test score del modelo 1 es el menos preciso. Por lo tanto, a pesar de que el primer modelo sea el que tiene mejor desempeño en las primeras etapas, tiene el peor desempeño con el subset de test.  """

#Modelo 1
print('\nModelo 1: ')
print(modelo1.predict_proba([df_x.loc[0]]))
print('Heart Disease? Estimated: ', modelo1.predict([df_x.loc[0]]),
      'Real: ', df_y.loc[0])

#Modelo 4
print('\nModelo 4: ')
print(modelo4.predict_proba([df_x.loc[0]]))
print('Heart Disease? Estimated: ', modelo4.predict([df_x.loc[0]]),
      'Real: ', df_y.loc[0])

#Modelo 6
print('\nModelo 6: ')
print(modelo6.predict_proba([df_x.loc[0]]))
print('Heart Disease? Estimated: ', modelo6.predict([df_x.loc[0]]),
      'Real: ', df_y.loc[0])

"""Ahora, al realizar las predicciones se puede observar que ambos modelos están realizando la predicción de manera correcta. Como primer valor muestra la probabilidad de que el HeartDisease tenga un valor de 0 y 1. Después se muestra el valor estimado con los modelos y el valor real. En todos los modelos coinciden que el valor estimado por cada modelo y el valor real es 0, por lo que se puede confirmar que son modelos efectivos para la predicción de enfermedades cardiacas. """

#Modelo 1
print('Modelo 1: ')
sns.set()
f, ax = plt.subplots()
matriz1 = confusion_matrix(y_test,pred1)
print(classification_report(y_test,pred1))
print('\nMatriz de confusión: ')
sns.heatmap(matriz1, annot=True, ax=ax, cbar=False, fmt='g', cmap='Pastel2')

#Modelo 4
print('Modelo 4: ')
sns.set()
f, ax = plt.subplots()
matriz4 = confusion_matrix(y_test,pred4)
print(classification_report(y_test,pred4))
print('\nMatriz de confusión: ')
sns.heatmap(matriz4, annot=True, ax=ax, cbar=False, fmt='g', cmap='Pastel2')

#Modelo 6
pred6 = modelo6.predict(x_test)
print('Modelo 6: ')
sns.set()
f, ax = plt.subplots()
matriz6 = confusion_matrix(y_test,pred6)
print(classification_report(y_test,pred6))
print('\nMatriz de confusión: ')
sns.heatmap(matriz6, annot=True, ax=ax, cbar=False, fmt='g', cmap='Pastel2')

"""Para el primer modelo podemos observar que el valor de f1-score es 0.81. En la matriz de confusión se tienen 67 valores true positive y 82 valores true negative; es decir, valores predecidos que coinciden con el valor real. Además, se tienen 22 valores false positive y 13 false negative es decir valores erróneos.

Para el cuarto modelo podemos observar que el valor de f1-score es 0.84. En la matriz de confusión se tienen 67 valores true positive y 88 valores true negative; es decir, valores predecidos que coinciden con el valor real. Además, se tienen 22 valores false positive y 7 false negative es decir valores erróneos.

Por otro lado, en el sexto modelo se muestra un valor de f1-score de 0.85 lo que indica una mejora en el desempeño de este modelo. En la matriz de confusión se tienen 68 valores true positive y 88 valores true negative; es decir, valores predecidos que coinciden con el valor real. Además, se tienen 21 valores false positive y 7 false negative es decir valores erróneos.

En conclusión, podemos observar una pequeña mejora en el modelo 6 ya que únicamente se tienen 28 valores erróneos mientras que en los modelos 1 y 4 se tienen 35 y 29 respectivamente. 
"""

fig, ax =plt.subplots(1,4)
sns.countplot(pred1, ax=ax[0], palette="Paired")
sns.countplot(pred4, ax=ax[1], palette="Accent")
sns.countplot(pred6, ax=ax[2], palette="Accent_r")
sns.countplot(y_test, ax=ax[3], palette="RdBu_r")
fig.show()

"""En la gráfica anterior se muestra del lado izquierdo el número de valores predecidos con el primer modelo, después con el cuatro, en medio el número de valores predecidos con el modelo seis y del lado derecho los valores reales. Se puede observar que los datos predecidos con valor 1 en todas las gráficas (modelo 1, 4 y 6) se acercan bastante a los valores reales. A pesar de que hay una diferencia significativa en los valores igual a cero de los modelos y los valores reales, los que más se acercan son el modelo 1 y 6. """

