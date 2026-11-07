"""Clase 07 - Experimentos con la red de Neurito (3 -> ocultas -> 3).

Reproduce la red de main.py (misma semilla, mismos datos, mismo entrenamiento)
y ejecuta los cinco experimentos de la guía. Solo usa NumPy.

    uv run experimentos_clase07.py
"""

import numpy as np

ACCIONES = ("Comer", "Dormir", "Jugar")


# ---------------------------------------------------------------- red
def relu(z):
    return np.maximum(0, z)


def softmax(z):
    e = np.exp(z - np.max(z, axis=1, keepdims=True))
    return e / np.sum(e, axis=1, keepdims=True)


def politica(X):
    """Regla que crea las etiquetas: la necesidad más fuerte gana.
    Columna 0 = hambre, 1 = energía (se usa 1 - energía), resto tal cual."""
    necesidades = X.copy()
    necesidades[:, 1] = 1 - X[:, 1]
    return np.argmax(necesidades, axis=1)


def entrenar(ocultas=6, epocas=1200, tasa=0.1, semilla=42, entradas=3, salidas=3):
    np.random.seed(semilla)
    X = np.random.rand(3000, entradas)
    y = politica(X)
    W1 = np.random.randn(entradas, ocultas) * 0.5
    b1 = np.zeros((1, ocultas))
    W2 = np.random.randn(ocultas, salidas) * 0.5
    b2 = np.zeros((1, salidas))
    historial = []
    n = len(X)
    for _ in range(epocas):
        z1 = X @ W1 + b1
        a1 = relu(z1)
        p = softmax(a1 @ W2 + b2)
        historial.append(-np.mean(np.log(p[np.arange(n), y] + 1e-10)))
        d2 = p.copy()
        d2[np.arange(n), y] -= 1
        d2 /= n
        gW2, gb2 = a1.T @ d2, d2.sum(axis=0, keepdims=True)
        d1 = (d2 @ W2.T) * (z1 > 0)
        gW1, gb1 = X.T @ d1, d1.sum(axis=0, keepdims=True)
        W1 -= tasa * gW1
        b1 -= tasa * gb1
        W2 -= tasa * gW2
        b2 -= tasa * gb2
    modelo = (W1, b1, W2, b2)
    return modelo, historial


def predecir(modelo, datos):
    W1, b1, W2, b2 = modelo
    return softmax(relu(np.atleast_2d(datos) @ W1 + b1) @ W2 + b2)


# Conjunto de prueba fijo para que todas las comparaciones sean justas.
_rng = np.random.default_rng(2026)
PRUEBA = _rng.random((1000, 3))
PRUEBA_Y = politica(PRUEBA)


def precision(modelo, X=PRUEBA, y=PRUEBA_Y):
    return np.mean(np.argmax(predecir(modelo, X), axis=1) == y)


def fmt(p):
    return "  ".join(f"{a}: {v:6.1%}" for a, v in zip(ACCIONES, p))


# ---------------------------------------------------------------- experimentos
def exp1_barrido(modelo):
    print("\n=== 1. Dos necesidades fijas, la tercera varía ===")
    casos = [
        ("aburrimiento", 2, [0.6, 0.6, None]),   # hambre 0.6, cansancio 0.4
        ("hambre", 0, [None, 0.4, 0.3]),         # cansancio 0.6, aburrimiento 0.3
        ("energía", 1, [0.7, None, 0.2]),        # hambre 0.7, aburrimiento 0.2
    ]
    for nombre, col, base in casos:
        print(f"\nVariando {nombre} (fijos: {[v for v in base if v is not None]})")
        anterior = None
        for v in np.round(np.arange(0, 1.0001, 0.01), 2):
            x = [v if b is None else b for b in base]
            accion = ACCIONES[int(np.argmax(predecir(modelo, x)))]
            esperada = ACCIONES[int(politica(np.array([x]))[0])]
            if accion != anterior:
                print(f"  {nombre} = {v:.2f} -> red: {accion:6s} | política: {esperada}")
                anterior = accion


def exp2_empates(modelo):
    print("\n=== 2. Prioridades casi iguales (Softmax) ===")
    print("Entrada = [hambre, energía, aburrimiento]; cansancio = 1 - energía")
    for x in ([0.60, 0.40, 0.30],   # hambre = cansancio = 0.6
              [0.61, 0.40, 0.30],
              [0.59, 0.40, 0.30],
              [0.50, 0.50, 0.50],   # triple empate
              [0.90, 0.80, 0.10],   # sin empate: hambre clara
              [0.95, 0.05, 0.95]):  # tres necesidades altas
        print(f"  {x} -> {fmt(predecir(modelo, x)[0])}")


def exp3_ocultas():
    print("\n=== 3. Neuronas ocultas (1200 épocas, tasa 0.1) ===")
    print(f"  {'ocultas':>7} | {'pérdida final':>13} | {'precisión':>9}")
    for h in (3, 6, 10, 20):
        m, hist = entrenar(ocultas=h)
        print(f"  {h:>7} | {hist[-1]:>13.4f} | {precision(m):>9.1%}")
    print("\n  Con 3 ocultas, la semilla importa (neuronas ReLU 'muertas'):")
    for s in (1, 2, 3, 4, 5):
        m, hist = entrenar(ocultas=3, semilla=s)
        print(f"    semilla {s}: pérdida {hist[-1]:.4f}  precisión {precision(m):.1%}")


def exp4_epocas_tasa():
    print("\n=== 4a. Épocas (6 ocultas, tasa 0.1) ===")
    for ep in (50, 200, 1200, 3000, 6000):
        m, hist = entrenar(epocas=ep)
        print(f"  {ep:>5} épocas | pérdida {hist[-1]:.4f} | precisión {precision(m):.1%}")
    print("\n=== 4b. Tasa de aprendizaje (6 ocultas, 1200 épocas) ===")
    for lr in (0.001, 0.01, 0.1, 0.5, 1.0, 3.0, 10.0):
        m, hist = entrenar(tasa=lr)
        h = np.array(hist)
        saltos = int(np.sum(np.diff(h) > 0))  # veces que la pérdida SUBE
        print(f"  tasa {lr:>6} | pérdida {h[-1]:.4f} | precisión {precision(m):6.1%}"
              f" | subidas de pérdida: {saltos}")


def exp5_cuarta_accion():
    print("\n=== 5. Cuarta acción: Bañarse (nueva entrada 'suciedad') ===")
    global ACCIONES
    original = ACCIONES
    ACCIONES = ("Comer", "Dormir", "Jugar", "Bañarse")
    m, hist = entrenar(entradas=4, salidas=4, epocas=3000)
    rng = np.random.default_rng(7)
    Xp = rng.random((1000, 4))
    print(f"  Red 4 -> 6 -> 4 | pérdida {hist[-1]:.4f} | precisión "
          f"{precision(m, Xp, politica(Xp)):.1%}")
    for x in ([0.2, 0.9, 0.1, 0.95], [0.8, 0.9, 0.1, 0.3]):
        print(f"  {x} -> {fmt(predecir(m, x)[0])}")
    ACCIONES = original


if __name__ == "__main__":
    modelo, hist = entrenar()
    print(f"Modelo de referencia 3-6-3: pérdida {hist[-1]:.4f}, "
          f"precisión {precision(modelo):.1%}")
    exp1_barrido(modelo)
    exp2_empates(modelo)
    exp3_ocultas()
    exp4_epocas_tasa()
    exp5_cuarta_accion()
