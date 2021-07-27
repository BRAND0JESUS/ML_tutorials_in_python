
# # para hacer preprocesamiento de los datos
# from sklearn import preprocessing
# # para establecer nuestros conjuntos de entrenamiento y evaluacion. 
# from sklearn.model_selection import train_test_split 
# # para usar las metricas necesarias para analizar la ejecución de nuestros modelos 
# from sklearn.preprocessing import metricsZAZSCGC

#%%
# REGRESION LINEAL SIMPLE
a = [3,2]
from matplotlib import colors
import pandas as pd     
import matplotlib.pyplot as plt
from pandas.core.algorithms import value_counts     # para trabajar con conjunto de datos
from sklearn.model_selection import train_test_split            
from sklearn.linear_model import LinearRegression



dataset = pd.read_csv('salarios.csv')
# print(dataset.head(5))
# print(dataset.shape)


x = dataset.iloc[:, :-1].values     # iloc = para localizar datos;[: para hacer intervalos,: obtener la culmna]; .value = para obtener sus valores
y = dataset.iloc[:, 1].values       # pediccion
# X = dataset['Aexperiencia'].values            # metodo cuando se tiene pocas var independientes
# y = dataset['Salario'].values

X_train, X_test, Y_Train, Y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)        # train_test_split = sirve para dividir la informacion
                                                                                                    # (datos, datos, test_size = (1-% datos de entrenamiento), random_state = si debemos modificar los datos, = 0 siempre vamos a tener los mismos datos)

regressor = LinearRegression()      # LinearRegression = modelo o metodo

regressor.fit(X_train,Y_Train)

viz_train = plt
viz_train.scatter(X_train, Y_Train, color = 'blue')        # (datos de entrenamiento)
viz_train.plot(X_train,regressor.predict(X_train), color = 'black') # (que es lo que se va a entrenar, que es lo se entreno; .predict = la prediccion que se muetra en la grafica(datos de enytrada))
viz_train.title('Salario vs Experiencia')
viz_train.xlabel('Experiencia')
viz_train.ylabel('Salario')
viz_train.show()


viz_train = plt
viz_train.scatter(X_test, Y_test, color = 'red')        # (datos de entrenamiento)
viz_train.plot(X_train,regressor.predict(X_train), color = 'black') # (que es lo que se va a entrenar, que es lo se entreno; .predict = la prediccion que se muetra en la grafica(datos de enytrada))
viz_train.title('Salario vs Experiencia')
viz_train.xlabel('Experiencia')
viz_train.ylabel('Salario')
viz_train.show()


print(regressor.score(X_test, Y_test)) # =0.78, el 78% de los nuevos datos que se use para validar el aprendizaje se va a hacer de manera correcta

#%%
# import pandas as pd
# import numpy as np
# import random
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression 
# from sklearn import preprocessing

# # Importacion de dataset
# dataset = pd.read_csv('salarios.csv')

# # defino los paises en list paises
# paises = ['CO','BR','PE','MX']

# # llevo cada elemento de paises a que sea convertido a un numero
# le1 = preprocessing.LabelEncoder()
# paises_encoded = le1.fit_transform(paises)

# # de forma aleatoria creo 30 elementos para dataset
# paises_dataset = [random.choice(paises_encoded) for i in range(len(dataset))]

# # paises codificados y en lista pasados al dataset
# dataset['pais'] = paises_dataset

# # Aplicando la regresión lineal

# # Dividiendo las columnas en x y y
# x = dataset.drop('Salario', axis=1)
# y = dataset.iloc[:,1].values

# # dividimos nuestro dataset
# X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

# # Invocamos el modelo y creamos el modelo con .fit
# regressor = LinearRegression()
# regressor.fit(X_train, Y_train)

# # Evaluamos performance
# print(regressor.score(X_test, Y_test))

# # ploteamos datos de entrenamiento para ver si realmente el 
# # modelo lo hizo bien, se entreno como se debe
# fig = plt.figure()
# viz_train = fig.add_subplot(111, projection='3d')
# viz_train.scatter(X_train['Aexperiencia'],X_train['pais'], Y_train, color = 'blue')
# viz_train.plot_trisurf(X_train['Aexperiencia'],X_train['pais'], regressor.predict(X_train),color = 'black', alpha = 0.5)
# viz_train.set_title('Salario Experiencia y pais')
# viz_train.set_xlabel('Experiencia')
# viz_train.set_ylabel('Pais')
# viz_train.set_zlabel('Salario')
# viz_train.set_yticks(range(len(paises_encoded)))
# viz_train.set_yticklabels(le1.inverse_transform(paises_encoded))
# viz_train.azim=-10
# fig.show()

# # probamos con datos de test
# fig = plt.figure()
# viz_train = fig.add_subplot(111, projection='3d')
# viz_train.scatter(X_test['Aexperiencia'],X_test['pais'], Y_test, color = 'red')
# viz_train.plot_trisurf(X_train['Aexperiencia'], X_train['pais'], regressor.predict(X_train),color = 'black', alpha = 0.5)
# viz_train.set_title('Salario Experiencia y pais')
# viz_train.set_xlabel('Experiencia')
# viz_train.set_ylabel('Pais')
# viz_train.set_zlabel('Salario')
# viz_train.set_yticks(range(len(paises_encoded)))
# viz_train.set_yticklabels(le1.inverse_transform(paises_encoded))
# viz_train.azim=-10
# fig.show()