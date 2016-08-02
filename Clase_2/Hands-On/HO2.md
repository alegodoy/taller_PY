# Hands-On Numpy y Matplolib

## Agua o tierra

Escriba un programa que tome coordenadas geográficas como entrada e imprima si esa coordenada es tierra o agua. El programa debe ser usado como un pipe de la linea de comandos.

**Tip:**
* numpy.fromfile

http://www.landcover.org/data/landcover/

### Eventos

Por cada evento que hay en el archivo *data/events.txt*, agregarle una columna al final indicando si ocurrió en agua o tierra.

### Graficando

Por cada evento que el usuario pasa por linea de comando, marcarlo con un cuadrado sobre el mapa.


## Datos faltantes

Muchos archivos de datos poseen el siguiente formato:

```
fecha inicial - fecha final
datos
dato faltante
mas texto
```

Escribir un script en python que reciba una archivo de este tipo, y retorne una matriz remplazado los valores faltantes por NaN.

## Promedio

Calcular los promedio y desviación standar por mes y por año.

### Graficar

Graficar estos datos usando matplotlib (histograma, precipitación vs mes).
