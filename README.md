# Neurito

Mascota virtual con un cerebro artificial hecho a mano con NumPy. Neurito tiene tres
necesidades (hambre, energía y aburrimiento, entre 0 y 1) y una red neuronal
**3 → 6 → 3** decide si debe **comer**, **dormir** o **jugar**. Pygame muestra la
decisión con animaciones.

Proyecto de la clase 07 de Inteligencia Artificial: <https://dialvebe.github.io/IA/clases/clase-07/>

## Cómo funciona

- **Datos:** 3000 situaciones aleatorias. La etiqueta es la necesidad más fuerte
  entre hambre, cansancio (`1 - energía`) y aburrimiento.
- **Red:** 3 entradas, 6 neuronas ocultas con ReLU y 3 salidas con Softmax.
- **Entrenamiento:** entropía cruzada, retropropagación y descenso de gradiente
  (1200 épocas, tasa 0.1, lote completo).
- **Prueba:** 1000 situaciones nuevas; la precisión mide qué tanto imita la red
  la política que creó las etiquetas.
- El estado **neutral** es una regla de la interfaz, no una salida de la red.

## Requisitos

- [uv](https://docs.astral.sh/uv/)
- Python 3.10 o superior (uv lo instala si hace falta)

## Ejecutar

```bash
uv sync
uv run red-sencilla.py   # ejemplo de una sola neurona
uv run main.py           # entrena la red y abre a Neurito
```

## Controles

| Tecla | Acción |
|---|---|
| `H` / `J` | Subir / bajar hambre |
| `E` / `D` | Subir / bajar energía |
| `A` / `S` | Subir / bajar aburrimiento |
| `R` | Necesidades aleatorias |
| `N` | Estado tranquilo |
| `Esc` | Salir |

## Estructura

```text
Neurito/
├── main.py           # red 3-6-3 + mascota en Pygame
├── red-sencilla.py   # una neurona: suma ponderada + sesgo + ReLU
├── pyproject.toml    # dependencias (numpy, pygame-ce)
└── assets/           # sprites de Neurito (comer, dormir, jugar, neutral)
```
