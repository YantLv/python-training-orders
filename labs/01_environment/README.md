# Laboratorio 01 - Entorno y herramientas

## Objetivo

Preparar un entorno de desarrollo reproducible para los laboratorios y el proyecto final.

## Conceptos utilizados

### Entorno virtual

Un entorno virtual permite aislar las dependencias del proyecto y evitar conflictos con otros proyectos de Python.

### Poetry

Poetry administra las dependencias, el entorno virtual y la configuración del proyecto mediante `pyproject.toml`.

### PEP 8

PEP 8 es la guía de estilo de Python. Define convenciones para mantener el código legible y consistente.

### Black

Black da formato automático al código.

### isort

isort organiza y agrupa las importaciones.

### Ruff

Ruff analiza el código y detecta errores de estilo, importaciones no utilizadas y otros posibles problemas.

### pre-commit

pre-commit ejecuta automáticamente las herramientas de calidad antes de aceptar un commit de Git.

## Ejercicio

Se creó un archivo con errores intencionales de estilo. Después se ejecutaron Ruff, isort y Black automáticamente mediante pre-commit para identificar y corregir los problemas.

## Ejecución
```cmd
poetry run python labs\01_environment\pep8_demo.py
```

## Validación

```cmd
poetry run python --version
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetry run pre-commit run --all-files
```
