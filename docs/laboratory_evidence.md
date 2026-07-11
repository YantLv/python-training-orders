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

