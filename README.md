# Neurito

Mascota virtual con un cerebro artificial hecho a mano con NumPy, sin frameworks de IA.
El proyecto tiene dos partes:

1. **Neurito (clase 07):** una red **3 → 6 → 3** decide si Neurito debe **comer**,
   **dormir** o **jugar** según su hambre, energía y aburrimiento.
2. **Neurito 2.0:** una red **3 → 12 → 1** aprende **cuándo saltar** obstáculos que
   llegan a distintas velocidades. Más detalles en [`GUIA_SALTO.md`](GUIA_SALTO.md).

Clase de referencia: <https://dialvebe.github.io/IA/clases/clase-07/>

## Requisitos

- [uv](https://docs.astral.sh/uv/)
- Python 3.10 o superior (uv lo instala si hace falta)

```bash
uv sync
```

## Parte 1: Neurito, comer, dormir o jugar

- **Datos:** 3000 situaciones aleatorias. La etiqueta es la necesidad más fuerte
  entre hambre, cansancio (`1 - energía`) y aburrimiento.
- **Red:** 3 entradas, 6 neuronas ocultas con ReLU y 3 salidas con Softmax.
- **Entrenamiento:** entropía cruzada, retropropagación y descenso de gradiente
  (1200 épocas, tasa 0.1, lote completo).
- El estado **neutral** es una regla de la interfaz, no una salida de la red.

```bash
uv run red-sencilla.py   # ejemplo de una sola neurona
uv run main.py           # entrena la red y abre a Neurito
```

| Tecla | Acción |
|---|---|
| `H` / `J` | Subir / bajar hambre |
| `E` / `D` | Subir / bajar energía |
| `A` / `S` | Subir / bajar aburrimiento |
| `R` | Necesidades aleatorias |
| `N` | Estado tranquilo |
| `Esc` | Salir |

### Experimentos

`experimentos_clase07.py` reproduce la red de `main.py` y prueba: barridos de una
necesidad, empates en Softmax, 3/6/10/20 neuronas ocultas, épocas, tasa de
aprendizaje y una cuarta acción (Bañarse). No abre ventana, solo imprime resultados.

```bash
uv run experimentos_clase07.py
```

El análisis y las respuestas están en el documento Word de la entrega.

## Parte 2: Neurito 2.0, aprende a saltar

Entradas normalizadas: distancia al obstáculo, velocidad y tiempo estimado hasta
llegar. Salida con sigmoide: si es ≥ 0.5 y Neurito está en el suelo, salta. Es
aprendizaje supervisado: las etiquetas dicen "saltar" cuando faltan entre 7 y 13
fotogramas para el choque.

```bash
uv run saltar.py
```

| Tecla | Acción |
|---|---|
| `1` | Entrenar una época |
| `2` | Entrenar cien épocas |
| `3` | Entrenamiento continuo on/off |
| `A` | Automático / manual |
| `Espacio` | Salto manual |
| `C` | Reiniciar pista y contadores |
| `R` | Reiniciar pesos y contadores |
| `Esc` | Salir |

## Estructura

```text
Neurito/
├── main.py                  # Parte 1: red 3-6-3 + mascota en Pygame
├── red-sencilla.py          # una neurona: suma ponderada + sesgo + ReLU
├── experimentos_clase07.py  # experimentos de la clase 07 (solo consola)
├── salto_modelo.py          # Parte 2: red 3-12-1 y datos de entrenamiento
├── salto_juego.py           # Parte 2: física del salto y colisiones
├── saltar.py                # Parte 2: juego y visualización del entrenamiento
├── GUIA_SALTO.md            # guía de Neurito 2.0
├── pyproject.toml           # dependencias (numpy, pygame-ce)
└── assets/                  # sprites de Neurito
```
