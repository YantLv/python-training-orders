# Laboratorio 03 — Funciones y programación pythonic

## Objetivo

Aplicar funciones y características propias de Python para crear código
reutilizable y expresivo.

El laboratorio implementa:

- Un decorador de reintentos con espera progresiva.
- Un generador que divide una colección en lotes.
- Un context manager para medir el tiempo de ejecución de un bloque.

También incluye ejemplos de argumentos variables, funciones lambda,
comprensiones y closures.

## Conceptos utilizados

### Argumentos `*args`

Permiten que una función reciba una cantidad variable de argumentos
posicionales.

En este laboratorio se utilizan en `calculate_average()` para calcular el
promedio de cualquier cantidad de valores.

### Argumentos `**kwargs`

Permiten recibir una cantidad variable de argumentos nombrados.

En este laboratorio se utilizan en `show_details()` para mostrar información
sin definir previamente todos los campos que se recibirán.

### Comprensiones de listas

Permiten construir una lista a partir de otra colección de manera compacta.

El laboratorio genera los cuadrados de los números pares utilizando una
comprensión.

### Funciones lambda

Una función lambda es una función pequeña y anónima formada por una sola
expresión.

Se utiliza como criterio para ordenar las órdenes según su total.

### Closures

Una closure es una función que conserva acceso a variables del entorno donde
fue creada.

La función `process_order()` utiliza la lista `pending_results`, definida
dentro de la función principal, para simular resultados diferentes en cada
intento.

### Decoradores

Un decorador permite agregar comportamiento a una función sin modificar
directamente su lógica.

El decorador `retry()` vuelve a ejecutar una función cuando se produce un
`ValueError`.

El tiempo de espera aumenta después de cada fallo:

```text
0.5 segundos
1.0 segundos
2.0 segundos
```

Este aumento progresivo se conoce como backoff.

### Generadores

Un generador produce valores uno por uno utilizando `yield`.

La función `generate_batches()` divide una colección en lotes sin generar
manualmente una lista con todos los lotes.

Por ejemplo:

```text
Entrada: [1, 2, 3, 4, 5]
Tamaño del lote: 2

Resultado:
[1, 2]
[3, 4]
[5]
```

### Context managers

Un context manager controla las acciones que ocurren antes y después de un
bloque ejecutado con `with`.

La función `execution_timer()` registra el tiempo inicial, permite ejecutar
el bloque y posteriormente calcula el tiempo transcurrido.

## Archivo principal

- `main.py`: contiene todos los ejercicios y demostraciones del laboratorio.

## Funciones implementadas

- `calculate_average()`: calcula el promedio de una cantidad variable de
  valores.
- `show_details()`: muestra argumentos nombrados.
- `generate_batches()`: divide una colección en lotes.
- `execution_timer()`: mide el tiempo de ejecución de un bloque.
- `retry()`: crea un decorador de reintentos.
- `main()`: coordina las demostraciones del laboratorio.

## Ejecución

Desde la raíz del proyecto:

```cmd
poetry run python labs\03_pythonic_functions\main.py
```

## Resultado esperado

El programa muestra:

1. El uso de `*args`.
2. El uso de `**kwargs`.
3. Una comprensión de lista.
4. El ordenamiento mediante una función lambda.
5. La generación de lotes.
6. El tiempo empleado en procesar los lotes.
7. Dos intentos fallidos y un tercer intento exitoso.

La duración exacta mostrada por el temporizador puede variar entre
ejecuciones.

## Validación de calidad

```cmd
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetry run pre-commit run --all-files
```

## Evidencia

La salida de una ejecución correcta se encuentra en:

```text
docs/evidence/lab03_execution.txt
```

## Resultado

Se implementaron correctamente el decorador de reintentos, el generador por
lotes y el context manager de temporización solicitados en el laboratorio.
Además, se demostraron argumentos variables, funciones lambda, comprensiones
y closures.

