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
    - [4.2. Extra 2](#extra-2-algoritmo-a)
    - [4.3. Extra 3](#extra-3-control-interactivo-del-robot)
    - [4.4. Extra 4](#extra-4-paredes)
    - [4.5. Extra 5](#extra-5-vídeo-parte-extra)

---

## 1. Descripción
Para la práctica se han realizado los siguientes hitos:

- **Base**:
    1. Se presenta un script de python que controla al robot para que alcance la meta sobre un mapa sencillo (map1).

- **Extra**:
    1. Se presenta un **vídeo** que muestra la ejecución de la parte base.
    2. Se añade un **algortimo de planificación** A* para alcanzar la meta.
    3. **Control interactivo** del robot.
    4. Las **paredes** son objetos sólidos que el robot no puede atravesar.
    5. Se adjunta un **vídeo** con la ejecución de la parte extra.

## 2. Estructura de carpetas
El esquema de organización del repositorio es el siguiente:
```
.
+-- docs (imgs..)
+-- scripts
    +-- pygame-display.py
+-- tools
    +-- astar.py
    +-- utils.py
+-- base.py
+-- extra.py
+-- map1.csv
+-- map1_inflated.csv
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

![map](/docs/map1.png)

El código del fichero (`base.py`) se encarga de simular el recorrido del robot  para alcanzar la meta. Destacar que el algorimo seguido por el robot es muy simple, primero trata de alcanzar una posición con una Y superior a la de meta (superior a 8) y después lo mismo para la coordenada X.

Si analizamos el código con más atención podemos observar cuatro clases `Simulator`, `Map`, `Robot` y `RobotView`. La clase `Simulator` se encarga de desplegar la ventana del simulador y mantenerla actualizada. La clase `Map` que representa el mapa. Y las clases `Robot` y `RobotView` los cuales representan al robot con sus parámetros reales y sus parámetros necesarios para su visualización en el simulador. Los detalles de la implementación se pueden ver en el código fuente, el cual se encuentra comentado.

## 4. Extras
### Extra 1: Vídeo parte base

Se muestra en vídeo el resultado de la ejecución de la parte base.

[![Desde Cero Base](http://img.youtube.com/vi/JjPXXs3ZV10/0.jpg)](http://www.youtube.com/watch?v=JjPXXs3ZV10)

### Extra 2: Algoritmo A*

La ruta que debe seguir el robot la calcula el algoritmo desarrollado en la asignatura de planificación y un nuevo bucle de control se encarga de el robot vaya siguiendo los pasos hasta alcanzar la meta. La ruta se obtiene mediante el método `get_route` y se optimiza mediante el método `optimize_route`. Para evitar obstaculos debido al volumen del robot, el mapa se infla mediante el método `inflate_map` que simula el mismo escenario para un robot puntual. El bucle de control se muestra a continuación:

```python
route = get_route(inFileStr.split(".")[0], [int(initX), int(initY)], [GOAL[0]-1, GOAL[1]-1])
route.append(GOAL)

ref = route.pop(0)
print("Going to", ref)
while True:
    velx = robot.pos[0] - ref[1]
    if velx > EPSILON:
        velx = -VEL
    elif velx < -EPSILON:
        velx = VEL
    else:
        velx = 0.0

    vely = robot.pos[1] - ref[0]
    if vely > EPSILON:
        vely = -VEL
    elif vely < -EPSILON:
        vely = VEL
    else:
        vely = 0.0

    robot.set_vel([velx, vely])
    if velx == 0 and vely == 0:
        if len(route) == 0:
            break
        ref = route.pop(0)
        print("Going to", ref)

    # handle events, avoiding gui freeze
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    sim.update()

    print("Robot at", robot.pos)
    time.sleep(RATE)
```

Para cada paso de la ruta se calcula la diferencia entre la posición del robot y la posición de referencia. Se fija una velocidad acorde para alcanzar la siguiente posición y se itera hasta llegar a la meta.

### Extra 3: Control Interactivo del Robot
Se ha añadido un procesador de argumentos en el incio de la ejecución del programa. La instrucción `python extra.py -h` muestra la ayuda:

```bash
parias@parias-msi:~/repos/my_simulator$ python extra.py -h
pygame 2.0.0 (SDL 2.0.12, python 3.6.9)
Hello from the pygame community. https://www.pygame.org/contribute.html
usage: extra.py [-h] [-m MAP] [-s N N] [-e N N] [-i]

My Simulator.

optional arguments:
  -h, --help           show this help message and exit
  -m MAP, --map MAP    change map folder
  -s N N, --start N N  change start point
  -e N N, --end N N    change end point
  -i                   interactive mode
```

Entre las opciones disponibles se encuentran cambiar el mapa (por defecto, `map1.csv`), cambiar el punto de partida (por defecto `[2 2]`), cambiar el punto de meta (por defecto, `[8 8]`) y entrar en el modo interactivo.
Así pues, ejecutando `python extra.py -i` se accede en un modo interactivo donde el usuario puede controlar al robot:

```bash
parias@parias-msi:~/repos/my_simulator$ python extra.py -i
pygame 2.0.0 (SDL 2.0.12, python 3.6.9)
Hello from the pygame community. https://www.pygame.org/contribute.html
Interactive Mode
Control de robot with the arrows (space to stop the robot).

```

Como indica el mensaje al ejecutar, el robot se puede controlar utilizando las teclas de flechas y del espacio para detenerse.

### Extra 4: Paredes
Se comprueba si el robot colisionará con algún obstáculo y en caso de que vaya a colisionar se detiene el robot (velocidad nula). El chequeo de colisiones se realiza comprobando si la siguiente posición del robot se solapa con la posición de los obstáculos sobre el mapa.

```python
def update_pos(self):
    """Moves Rect and updates robot pose."""
    rect = self.move(*self.robot.vel)  # movimiento potencial
    if rect.collidelist(self.sim.map.walls) == -1:  # chequeo de colision
        self.move_ip(*self.robot.vel)
        x = (self.center[0] - self.sim.cell_width/4.0) / self.sim.cell_width
        y = (self.center[1] - self.sim.cell_height/4.0) / self.sim.cell_height
        self.robot.pos = [x, y]
    else:
        print("[Info] Potencial collision detected. Robot stopped.")
        self.robot.set_vel([0, 0])  # detenemos robot
```

Se adjunta un gif con la ejecución del simulador en modo interactivo y donde se muestran varias colisiones.

![collision](/docs/simulador-extra.gif)

### Extra 5: Vídeo Parte Extra
Se muestra en vídeo el resultado de la ejecución de la parte extra.

[![Desde Cero Extra](http://img.youtube.com/vi/fDPL8TaYknk/0.jpg)](http://www.youtube.com/watch?v=fDPL8TaYknk)
