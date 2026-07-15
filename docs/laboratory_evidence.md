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