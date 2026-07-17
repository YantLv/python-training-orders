# Evidencias de los laboratorios

Este documento concentra el estado, los archivos y los comandos de validación de los laboratorios realizados durante el curso de Python.

---

## Laboratorio 01 - Entorno y herramientas

### Estado

Completado.

### Objetivo

Configurar un proyecto con Python 3.12 y Poetry, además de integrar herramientas automáticas de calidad de código.

### Herramientas utilizadas

- Poetry
- Black
- isort
- Ruff
- pre-commit

### Archivos principales

- `pyproject.toml`
- `.pre-commit-config.yaml`
- `labs/01_environment/pep8_dem.py`
- `labs/01_environment/README.md`

### Evidencias

- `docs/evidence/lab01_ruff_before.txt`
- `docs/evidence/lab01_ruff_after.txt`

### Comandos de validación

```cmd
poetry run python --version
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetry run pre-commit run --all-files
poetry run python labs\01_environment\pep8_demo.py
```

### Resultado esperado

`60.0`

### Resultado obtenido

Las herramientas de calidad finalizaron sin errores y el scrito se ejecutó correctamente.

---

## Laboratorio 02 - Fundamentos del lenguaje

### Estado

Completado.

### Objetivo

Leer datos desde un archivo JSON, filtrar órdenes, calcular agregaciones y manejar errores de archivo o formato.

### Conceptos aplicados

- Listas y diccionarios.
- Variables y tipos básicos.
- Condicionales y ciclos.
- Funciones.
- `match/case`.
- Expresiones regulares.
- Lectura de JSON.
- Manejo de excepciones.

### Archivos principales
- `labs/02_fundamentals/main.py`
- `labs/02_fundamentals/README.md`
- `labs/02_fundamentals/data/orders.json`
- `labs/02_fundamentals/data/invalid_orders.json`

### Evidencias

- `docs/evidence/lab02_succes.txt`
- `docs/evidence/lab02_invalid_json.txt`
- `docs/evidence/lab02_missing_file.txt`

### Comandos de validación

```cmd
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetry run pre-commit run --all-files
poetry run python labs\02_fundamentals\main.py
```

### Resultado obtenido

El programa leyó correctamente el archivo JSON, filtró las órdenes completadas con monto mínimo de 500, calculó el total y el promedio, y controló correctamente los errores de archivo inexistente y JSON inválido.

---

## Laboratorio 03 — Funciones y programación pythonic

### Estado

Completado.

### Objetivo

Implementar funciones reutilizables mediante características propias de
Python, incluyendo un decorador de reintentos, un generador por lotes y un
context manager de temporización.

### Conceptos aplicados

- Funciones.
- Argumentos posicionales y nombrados.
- Argumentos variables con `*args`.
- Argumentos variables con `**kwargs`.
- Comprensiones de listas.
- Funciones lambda.
- Closures.
- Decoradores.
- Iteradores y generadores.
- Uso de `yield`.
- Context managers.
- Manejo de excepciones.
- Espera progresiva o backoff.

### Ejercicios realizados

#### Decorador de reintentos

Se creó el decorador `retry()`, que vuelve a ejecutar una función cuando se
produce un `ValueError`.

La espera entre intentos aumenta progresivamente.

#### Generador por lotes

Se creó la función `generate_batches()`, que utiliza `yield` para entregar una
colección dividida en lotes.

#### Context manager de temporización

Se creó `execution_timer()`, que mide el tiempo empleado por un bloque
ejecutado mediante `with`.

### Archivos principales

- `labs/03_pythonic_functions/main.py`
- `labs/03_pythonic_functions/README.md`

### Evidencia

- `docs/evidence/lab03_execution.txt`

### Comandos de ejecución

```cmd
poetry run python labs\03_pythonic_functions\main.py
```

### Comandos de validación

```cmd
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetry run pre-commit run --all-files
```

### Resultado obtenido

El programa:

- Calculó un promedio utilizando `*args`.
- Mostró datos recibidos mediante `**kwargs`.
- Generó cuadrados de números pares mediante una comprensión.
- Ordenó órdenes mediante una función lambda.
- Dividió una lista de códigos de orden en tres lotes.
- Midió el tiempo utilizado para procesar los lotes.
- Simuló dos fallos y completó correctamente la operación en el tercer
  intento mediante el decorador de reintentos.

Las verificaciones de Ruff, isort, Black y pre-commit finalizaron
correctamente.

---

## Laboratorio 05 — Tipado estático opcional y calidad

### Estado

Completado.

### Objetivo

Añadir anotaciones de tipos al código del laboratorio de objetos y modelos,
verificar su consistencia mediante mypy e integrar la comprobación estática al
flujo de pre-commit.

### Código modificado

- `labs/04_objects_models/main.py`

### Conceptos aplicados

- Tipado dinámico y tipado estático opcional.
- Anotaciones de parámetros.
- Anotaciones de retorno.
- Tipado de listas y objetos.
- Alias de tipos.
- `Literal`.
- Tipo general `object`.
- Inferencia de tipos.
- Validación estática con mypy.
- Validación de datos mediante Pydantic.
- Integración de herramientas con pre-commit.

### Cambios realizados

- Se añadió el alias `OrderStatus` mediante `Literal`.
- Se anotaron los métodos y propiedades de `OrderItem` y `Order`.
- Se anotaron las funciones de conversión.
- Se añadió el tipo de retorno de `main()`.
- Se anotó la lista de objetos `OrderItem`.
- Se configuró mypy en `pyproject.toml`.
- Se agregó mypy a `.pre-commit-config.yaml`.
- Se sustituyó la creación mediante `OrderIn(**data)` por
  `OrderIn.model_validate(data)`.

### Problema detectado por mypy

Mypy interpretaba los diccionarios utilizados como entrada como:

```text
dict[str, object]
```

Por esa razón no podía garantizar que cada valor correspondiera con los tipos
esperados por `OrderIn`.

El problema se resolvió mediante:

```python
OrderIn.model_validate(data)
```

Pydantic valida el diccionario y produce un modelo con los tipos definidos.

### Archivos principales

- `labs/04_objects_models/main.py`
- `labs/05_static_typing/README.md`
- `pyproject.toml`
- `.pre-commit-config.yaml`

### Evidencias

- `docs/evidence/lab05_mypy_before.txt`
- `docs/evidence/lab05_mypy_after.txt`
- `docs/evidence/lab05_precommit.txt`

### Comandos de validación

```cmd
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetry run mypy
poetry run pre-commit run --all-files
```

### Resultado obtenido

Antes de añadir las anotaciones, mypy detectó funciones sin tipos y
posteriormente identificó incompatibilidades al desempaquetar diccionarios.

Después de anotar el código y utilizar `model_validate()`, la comprobación
final mostró:

```text
Success: no issues found in 1 source file
```

Ruff, isort, Black, mypy y pre-commit finalizaron correctamente.