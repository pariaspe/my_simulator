# Entrega: Desde Cero
Este repositorio contiene la generación de laberinto con un robot en python, moviendo el robot desde el origen hasta la meta. Este desplazamiento se consigue mediante el uso de un plugin de openRAVE desarrollado en python para la resolución de este ejercicio.

Autor: **Pedro Arias Pérez**

Link: [pariaspe/my_simulator](https://github.com/pariaspe/my_simulator)


## Índice
- [1. Descripción](#1-descripción)
- [2. Estructura de Carpetas](#2-estructura-de-carpetas)
- [3. Base](#3-base)
- [4. Extras](#4-extras)
    - [4.1. Extra 1](#extra-1-vídeo-parte-base)

---

## 1. Descripción
Para la práctica se han realizado los siguientes hitos:

- **Base**:
    1. Se presenta un script de python que controla al robot para que alcance la meta sobre un mapa sencillo (map1).

- **Extra**:
    1. Se presenta un **vídeo** que muestra la ejecución de la parte base.

## 2. Estructura de carpetas
El esquema de organización del repositorio es el siguiente:
```
.
+-- README.md
```

## 3. Base
Tras finalizar la instalación se calculan las dimensiones del mapa:

```bash
parias@parias-msi:~/repos/my_simulator$ python3
Python 3.6.9 (default, Oct  8 2020, 12:12:24)
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> x = len("arias")*2
>>> y = len("perez")*2
>>> print(x, y)
10 10
>>>
```

Dadas estas dimensiones `(10x10)` se ha construído el siguiente mapa en formato csv `(map1.csv)`:

```bash
parias@parias-msi:~/repos/my_simulator$ cat assets/map1.csv
1,1,1,1,1,1,1,1,1,1
1,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,1
1,1,1,1,0,0,0,0,0,1
1,1,1,1,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,1
1,1,1,1,1,1,1,1,1,1
```

Se ha elegido un mapa muy sencillo con una resolución de un metro por caracter. El inicio será la posición `[1,1]` (fila 2, columna 2), mientras que la meta será en la posición `[8,8]` (fila 9, columna 9).

El siguiente script (`pygame-display.py`) permite visualizar el mapa. El script se ha modificado minimamente para que las filas y columnas del csv coincidan con el mostrado en la ventana.

```bash
parias@pariaas-msi:~/repos/my_simulator$ ./scripts/pygame-display.py map1.csv 1 1
```

![map](/doc/map1.png)

El código del fichero (`base.py`) se encarga de simular el recorrido del robot  para alcanzar la meta. Destacar que el algorimo seguido por el robot es muy simple, primero trata de alcanzar una posición con una Y superior a la de meta (superior a 8) y después lo mismo para la coordenada X.

Si analizamos el código con más atención podemos observar cuatro clases `Simulator`, `Map`, `Robot` y `RobotView`. La clase `Simulator` se encarga de desplegar la ventana del simulador y mantenerla actualizada. La clase `Map` que representa el mapa. Y las clases `Robot` y `RobotView` los cuales representan al robot con sus parámetros reales y sus parámetros necesarios para su visualización en el simulador. Los detalles de la implementación se pueden ver en el código fuente, el cual se encuentra comentado.

## 4. Extras
### Extra 1: Vídeo parte base

Se muestra en vídeo el resultado de la ejecución de la parte base.

[![OpenRAVE Base](http://img.youtube.com/vi/j-N7YpmrsZ4/0.jpg)](http://www.youtube.com/watch?v=j-N7YpmrsZ4)
