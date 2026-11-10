"""Pregunta 7: ¿Neurito mejora o empeora si el profesor es DFS o A* en vez de BFS?

Uso:
    uv run python experimento_dfs_astar.py

Entrena a Neurito tres veces (una con cada profesor) y lo pone a resolver
retos que nunca vio. No modifica los demás archivos del proyecto.
"""
import heapq

import numpy as np

from laberinto_mundo import MAPAS, libres, vecino, valido, distancias_bfs, accion_experta, Laberinto, elegir_accion
from laberinto_red import RedLaberinto, codificar

EPOCAS = 400
LIMITE_INTENTOS = 45  # igual que en el juego


def profesor_bfs(mapa, origen, meta, memoria):
    """El profesor original: camino más corto."""
    if meta not in memoria:
        memoria[meta] = distancias_bfs(mapa, meta)
    return accion_experta(mapa, origen, memoria[meta])


def profesor_dfs(mapa, origen, meta, memoria):
    """Recorre el laberinto 'a fondo' desde la comida. Siempre llega, pero da vueltas."""
    if meta not in memoria:
        padre, vistas, pila = {}, {meta}, [meta]
        while pila:
            actual = pila.pop()
            for a in range(4):
                siguiente = vecino(actual, a)
                if valido(mapa, siguiente) and siguiente not in vistas:
                    vistas.add(siguiente)
                    padre[siguiente] = actual
                    pila.append(siguiente)
        memoria[meta] = padre
    destino = memoria[meta][origen]
    for a in range(4):
        if vecino(origen, a) == destino:
            return a


def profesor_astar(mapa, origen, meta, memoria):
    """Camino más corto, guiándose por qué tan lejos está la comida."""
    distancia = lambda p: abs(p[0] - meta[0]) + abs(p[1] - meta[1])
    abierta = [(distancia(origen), 0, origen, None)]
    costo = {origen: 0}
    while abierta:
        _, c, actual, primer_paso = heapq.heappop(abierta)
        if actual == meta:
            return primer_paso
        for a in range(4):
            siguiente = vecino(actual, a)
            if valido(mapa, siguiente) and c + 1 < costo.get(siguiente, 10**9):
                costo[siguiente] = c + 1
                heapq.heappush(abierta, (c + 1 + distancia(siguiente), c + 1, siguiente,
                                         a if primer_paso is None else primer_paso))


def generar_datos(profesor, semilla=42):
    """Igual que en laberinto_red.py, pero eligiendo el profesor."""
    muestras = []
    for indice, mapa in enumerate(MAPAS):
        celdas, memoria = libres(mapa), {}
        for meta in celdas:
            for posicion in celdas:
                if posicion != meta:
                    muestras.append((indice, posicion, meta, profesor(mapa, posicion, meta, memoria)))
    np.random.default_rng(semilla).shuffle(muestras)
    corte = int(len(muestras) * 0.8)
    entrenamiento, prueba = muestras[:corte], muestras[corte:]
    X = np.stack([codificar(i, p, m) for i, p, m, _ in entrenamiento])
    y = np.array([a for *_, a in entrenamiento])
    Xp = np.stack([codificar(i, p, m) for i, p, m, _ in prueba])
    yp = np.array([a for *_, a in prueba])
    return X, y, Xp, yp, prueba


def completa(red, indice, inicio, meta):
    """Juega un reto en modo red pura, como en el juego."""
    mundo = Laberinto(indice)
    mundo.posicion, mundo.meta, mundo.visitadas = inicio, meta, {inicio: 1}
    while mundo.intentos < LIMITE_INTENTOS:
        accion, _ = elegir_accion(red, mundo, mundo.visitadas, False)
        if mundo.mover(accion) == 'comida':
            return True
    return False


if __name__ == '__main__':
    print(f'Cada profesor entrena a Neurito {EPOCAS} épocas.\n')
    print(f'{"Profesor":<10}{"Aciertos":>10}{"Laberintos completados":>25}')
    for nombre, profesor in (('BFS', profesor_bfs), ('DFS', profesor_dfs), ('A*', profesor_astar)):
        X, y, Xp, yp, retos = generar_datos(profesor)
        red = RedLaberinto()
        for _ in range(EPOCAS):
            red.entrenar_epoca(X, y)
        logrados = sum(completa(red, i, inicio, meta) for i, inicio, meta, _ in retos)
        print(f'{nombre:<10}{red.exactitud(Xp, yp):>10.1%}{logrados / len(retos):>25.1%}')
