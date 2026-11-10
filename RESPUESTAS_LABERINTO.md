# Respuestas a los experimentos de Neurito 3.0

## 1. Neurito sin entrenar. ¿Por qué se atasca?

Al abrir el juego sin entrenar, Neurito no tiene idea de para dónde ir. Muchas veces se pega contra una pared y se queda ahí chocando una y otra vez, y el contador de paredes no para de subir. Otras veces va y vuelve entre dos casillas sin avanzar. Casi nunca llega a la comida y la "Exactitud prueba" queda alrededor del 28 %, que es como adivinar al azar entre las cuatro direcciones.

Se atasca porque, cuando choca, sigue en el mismo lugar. Como nada cambió, vuelve a tomar la misma decisión y choca de nuevo. Además, no recuerda por dónde ya pasó, por eso se queda dando vueltas.

## 2. Entrenar 100, 200 y 400 épocas

| Épocas | Pérdida | Exactitud prueba |
|---|---|---|
| 100 | 0.135 | 85 % |
| 200 | 0.038 | 90 % |
| 400 | 0.011 | 92 % |

A medida que entrena, la línea de la pérdida en la gráfica va bajando y la exactitud sube. Con 100 épocas Neurito ya se mueve mejor, pero todavía se pierde bastante y se atasca seguido. Con 200 se nota el cambio: casi siempre va directo a la comida. Entre 200 y 400 la diferencia ya es poca.

Algo que llama la atención es que con 100 épocas la exactitud ya es del 85 %, pero Neurito sigue fallando muchos laberintos. Para llegar a la comida tiene que hacer bien muchos movimientos seguidos, y con equivocarse en uno solo ya se pierde.

## 3. Red pura vs. modo asistido

En modo red pura, Neurito decide solo con lo que aprendió. Si está bien entrenado llega casi siempre, pero de vez en cuando choca o se queda dando vueltas.

En modo asistido llega prácticamente siempre, y lo curioso es que **llega incluso sin entrenar**. Las reglas del modo asistido no lo dejan chocar contra las paredes y lo empujan a no repetir casillas, así que termina encontrando la comida a punta de explorar, aunque da muchísimas vueltas.

Entonces:

- **Lo que aprendió el modelo** es saber hacia dónde queda la comida. Por eso, ya entrenado, va casi por el camino más corto.
- **Lo que ponen las reglas** es que no choque ni se quede en círculos.

Para ver lo que de verdad aprendió Neurito hay que mirarlo en modo red pura.

## 4. Cambiar las neuronas ocultas

Cambié el 96 por 16, 32 y 128, y entrené cada uno 400 épocas.

| Neuronas | Exactitud prueba |
|---|---|
| 16 | 87 % |
| 32 | 89 % |
| 96 | 92 % |
| 128 | 91 % |

Con 16 neuronas Neurito tiene un "cerebro" más pequeño: aprende, pero se equivoca más y se atasca más seguido. Con 32 mejora un poco y con 96 se ve bastante bien. Con 128 casi no cambia nada respecto a 96; como el laberinto es pequeño, darle más neuronas ya no le ayuda mucho.

## 5. Cambiar la tasa de aprendizaje

La tasa de aprendizaje es qué tanto corrige Neurito cada vez que se equivoca. Probé varios valores con 400 épocas:

| Tasa | Exactitud prueba | ¿Qué se ve? |
|---|---|---|
| 0.01 | 74 % | Aprende lentísimo, sigue perdido |
| 0.1 | 87 % | Aprende, pero más lento |
| 0.45 | 92 % | Aprende bien |
| 1.0 | 93 % | Aprende bien, un poco más rápido |
| 5.0 | 24 % | No aprende nada, se descontrola |

Con una tasa muy pequeña, la pérdida baja tan despacio que a las 400 épocas Neurito todavía se pierde mucho. Con una muy grande (5.0) la gráfica no baja y Neurito se comporta como si nunca hubiera entrenado: corrige tanto que se pasa del punto correcto. Con 0.45 o 1.0 sí converge.

## 6. Cambiar de mapa

Con la tecla N pasé por los tres mapas. Neurito se defiende bien en los tres. El mapa 2 me pareció el más difícil, porque tiene más cruces y pasillos cortos donde es fácil irse por el camino equivocado.

Eso sí, Neurito ya conocía los tres mapas porque entrenó con ellos. Lo nuevo son las posiciones de inicio y de la comida. Si le pusieran un mapa totalmente nuevo no sabría resolverlo, porque no "ve" las paredes: solo recuerda las de los mapas con los que entrenó.

## 7. Cambiar BFS por DFS y A*

BFS es el "profesor" que le enseña a Neurito el movimiento correcto. Con ayuda de IA (vibecoding) hice el archivo `experimento_dfs_astar.py`, que entrena a Neurito con tres profesores distintos y compara los resultados. Se ejecuta con:

    uv run python experimento_dfs_astar.py

- **DFS**: siempre llega a la comida, pero no por el camino más corto; da muchas vueltas.
- **A\***: encuentra el camino más corto, igual que BFS, guiándose por qué tan lejos está la comida.

| Profesor | Aciertos | Laberintos completados |
|---|---|---|
| BFS | 92 % | 83 % |
| DFS | 83 % | 62 % |
| A* | 93 % | 86 % |

- **Con DFS, Neurito empeora.** Aprende a dar vueltas porque eso es lo que le enseñan, y a veces el camino es tan largo que no alcanza a llegar.
- **Con A\*, queda igual o un poquito mejor que con BFS**, porque los dos enseñan el camino más corto. La diferencia es muy pequeña.

Neurito aprende copiando a su profesor: si el profesor es malo, el alumno también.

## Conclusión

Neurito aprende imitando a BFS. Después de entrenar, casi siempre llega a la comida por un buen camino, aunque acertar la mayoría de movimientos no garantiza terminar el laberinto. El modo asistido llega siempre, pero buena parte de ese mérito es de las reglas y no de lo que aprendió. Y lo que Neurito aprende depende de qué tan bueno sea el profesor que le enseña.
