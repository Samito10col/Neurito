"""Una sola neurona artificial: suma ponderada + sesgo + ReLU."""

hambre, energia, aburrimiento = 0.8, 0.2, 0.5
w1, w2, w3, sesgo = 0.7, -0.5, 0.3, 0.1

z = hambre * w1 + energia * w2 + aburrimiento * w3 + sesgo
activacion = max(0, z)  # ReLU
print(f"z = {z:.2f}")
print(f"ReLU(z) = {activacion:.2f}")  # 0.71: es una activación, no una probabilidad
