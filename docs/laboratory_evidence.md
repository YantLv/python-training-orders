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

## Laboratorio 04 — Objetos y modelos de datos

### Estado

Completado.

### Objetivo

Modelar órdenes mediante dataclasses, aplicar cálculos derivados, comparar
objetos y validar entradas y salidas mediante Pydantic.

### Conceptos aplicados

- Clases y objetos.
- Dataclasses.
- Composición.
- Propiedades calculadas.
- Métodos especiales o dunder.
- Validación con Pydantic.
- Serialización mediante `model_dump()`.
- Conversión entre modelos y entidades.
- Manejo de errores de validación.

### Entidades implementadas

- `OrderItem`
- `Order`

### Modelos Pydantic implementados

- `OrderItemIn`
- `OrderIn`
- `OrderOut`

### Cálculos realizados

- Subtotal por artículo.
- Subtotal de la orden.
- Total después de aplicar el descuento.
- Comparación entre órdenes según su total.

### Validaciones realizadas

- Formato del código de orden.
- Nombre de cliente obligatorio.
- Lista de artículos no vacía.
- Cantidad mayor que cero.
- Precio no negativo.
- Descuento entre 0 y 1.

### Archivos principales

- `labs/04_objects_models/main.py`
- `labs/04_objects_models/README.md`

### Evidencia

- `docs/evidence/lab04_execution.txt`

### Comando de ejecución

```cmd
poetry run python labs\04_objects_models\main.py
```

### Comandos de validación

```cmd
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetry run pre-commit run --all-files
```

### Resultado obtenido

Se crearon dos órdenes válidas, se calcularon sus subtotales y totales, y se
compararon mediante el operador `<`.

Los datos inválidos fueron rechazados correctamente por Pydantic debido al
formato incorrecto del código, una cantidad igual a cero y un descuento fuera
del rango permitido.

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

---

## Laboratorio 06 — Librería estándar y entrada/salida

### Estado

Completado.

### Objetivo

Construir un proceso de entrada y salida utilizando herramientas de la
librería estándar de Python para leer un archivo CSV, calcular métricas y
guardar un reporte en JSON.

También se utilizaron configuración YAML, fechas con zona horaria, logging y
subprocess.

### Flujo implementado

```mermaid
flowchart TB

A[Configuración YAML] -> B[Lectura de órdenes CSV]
B -> C[Conversión de valores]
C -> D[Filtrado de órdenes]
D -> E[Cálculo de métricas]
E -> F[Generación de reporte JSON]
F -> G[Registro del procesamiento]
```

### Conceptos aplicados

- Manejo de rutas mediante `pathlib`.
- Lectura de archivos CSV.
- Lectura de configuración YAML.
- Escritura de archivos JSON.
- Conversión de texto a valores numéricos.
- Fechas y horas mediante `datetime`.
- Zonas horarias mediante `zoneinfo`.
- Formato de fecha ISO 8601.
- Logging en consola y archivo.
- Niveles `INFO`, `WARNING` y `ERROR`.
- Ejecución de procesos mediante `subprocess`.
- Uso de `sys.executable`.
- Manejo de excepciones.
- Creación automática de directorios.

### Archivos de entrada

- `labs/06_standard_library/data/orders.csv`
- `labs/06_standard_library/config.yaml`

### Archivos generados

- `labs/06_standard_library/output/summary.json`
- `labs/06_standard_library/logs/laboratory.log`

### Archivo principal

- `labs/06_standard_library/main.py`

### Funciones implementadas

- `configure_logging()`
- `load_config()`
- `load_orders()`
- `filter_orders()`
- `calculate_metrics()`
- `get_report_datetime()`
- `get_python_version()`
- `save_report()`
- `main()`

### Configuración utilizada

```yaml
minimum_total: 500
selected_status: completed
timezone: America/Mexico_City
output_file: summary.json
```

### Dependencias agregadas

- `PyYAML`
- `tzdata`

PyYAML se agregó para leer archivos YAML.

`tzdata` se agregó porque el entorno de Windows no encontraba la base de datos
necesaria para utilizar `America/Mexico_City` mediante `ZoneInfo`.

### Problema de zona horaria

Durante la primera ejecución se produjo:

```text
No time zone found with key America/Mexico_City
```

La zona horaria configurada era válida. El problema era la ausencia de datos
IANA de zonas horarias en el entorno.

Se solucionó instalando:

```cmd
poetry add tzdata
```

También se agregó manejo específico para:

```python
ZoneInfoNotFoundError
```

Este bloque se colocó antes de `KeyError`, porque `ZoneInfoNotFoundError`
deriva de esa excepción.

### Resultado obtenido

Se cargaron seis órdenes desde el CSV.

Tres órdenes cumplieron los filtros de estado `completed` y monto mínimo de
500:

- `ORD-3001`
- `ORD-3003`
- `ORD-3005`

Las métricas obtenidas fueron:

```text
Cantidad de órdenes: 3
Monto total: 4200.50
Monto promedio: 1400.17
```

El reporte fue guardado correctamente en formato JSON.

### Validación de WARNING

Se modificó temporalmente el monto mínimo a 5000.

Ninguna orden cumplió los filtros y el programa generó correctamente un
mensaje con nivel `WARNING`.

Después de la prueba, el monto mínimo se restauró a 500.

### Evidencias

- `docs/evidence/lab06_execution.txt`
- `docs/evidence/lab06_warning.txt`
- `docs/evidence/lab06_ruff.txt`

### Comando de ejecución

```cmd
poetry run python labs\06_standard_library\main.py
```

### Comandos de validación

```cmd
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetry run mypy
poetry run pre-commit run --all-files
```

### Resultado de calidad

La ejecución del laboratorio terminó correctamente.

Ruff, isort, Black, mypy y los hooks de pre-commit finalizaron sin errores.