# Laboratorio 06 — Librería estándar y entrada/salida

## Objetivo

Utilizar herramientas de la librería estándar de Python para leer, procesar y
guardar información en distintos formatos.

El laboratorio implementa un flujo que:

1. Lee opciones desde un archivo YAML.
2. Carga órdenes desde un archivo CSV.
3. Convierte los valores del CSV a tipos de Python.
4. Filtra las órdenes según una configuración.
5. Calcula métricas generales.
6. Obtiene la fecha actual con una zona horaria.
7. Consulta la versión de Python mediante un subproceso.
8. Guarda el resultado en formato JSON.
9. Registra el proceso mediante logging.

## Flujo del programa

```mermaid
flowchart TB
A[config.yaml] -> B[orders.csv]
B -> C[lectura y conversión]
C -> D[filtrado de órdenes]
D -> E[cálculo de métricas]
E -> F[summary.json]
F -> G[mensajes de logging]
```

## Estructura

```text
labs/06_standard_library/
├── data/
│ └── orders.csv
├── logs/
│ └── laboratory.log
├── output/
│ └── summary.json
├── config.yaml
├── main.py
└── README.md
```

Los archivos `laboratory.log` y `summary.json` se generan o actualizan durante
la ejecución.

## Conceptos utilizados

### pathlib

`pathlib` permite representar rutas mediante objetos `Path`.

La ruta base del laboratorio se obtiene con:

```python
BASE_DIR = Path(__file__).resolve().parent
```

A partir de ella se construyen las rutas de entrada y salida:

```python
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"
```

Este enfoque evita concatenar manualmente cadenas con separadores de rutas.

### CSV

El archivo `orders.csv` contiene las órdenes utilizadas por el laboratorio.

Se utiliza `csv.DictReader` para convertir cada fila en un diccionario cuyas
claves corresponden con los encabezados del archivo.

Como los valores de un CSV se leen inicialmente como texto, el campo `total`
se convierte explícitamente a `float`.

### YAML

El archivo `config.yaml` contiene las opciones del procesamiento:

```yaml
minimum_total: 500
selected_status: completed
timezone: America/Mexico_City
output_file: summary.json
```

Se utiliza `yaml.safe_load()` para convertir el contenido YAML en un
diccionario de Python.

PyYAML es una dependencia externa, ya que el soporte para YAML no forma parte
de la librería estándar.

### JSON

El resultado del procesamiento se guarda en:

```text
labs/06_standard_library/output/summary.json
```

Se utiliza `json.dump()` con indentación para producir un archivo legible.

El reporte contiene:

- Fecha de generación.
- Versión de Python.
- Filtros utilizados.
- Métricas calculadas.
- Órdenes que cumplieron los filtros.

### Fechas y zonas horarias

Se utilizan `datetime` y `ZoneInfo` para obtener la fecha actual en la zona:

```text
America/Mexico_City
```

En Windows fue necesario instalar `tzdata`, ya que el sistema no proporcionaba
directamente la base de datos de zonas horarias utilizada por `zoneinfo`.

La fecha se guarda en formato ISO 8601.

Ejemplo:

```text
2026-07-18T14:35:20.254322-06:00
```

### Logging

El módulo `logging` registra información del proceso en dos destinos:

- Consola.
- Archivo `logs/laboratory.log`.

Los niveles utilizados son:

- `INFO`: ejecución normal.
- `WARNING`: ninguna orden cumplió los filtros.
- `ERROR`: ocurrió un problema que impidió continuar una operación.

El formato configurado incluye:

```text
fecha | nivel | mensaje
```

### Subprocess

Se utiliza `subprocess.run()` para ejecutar el intérprete actual con la opción
`--version`.

```python
result = subprocess.run(
    [sys.executable, "--version"],
    capture_output=True,
    text=True,
    check=True,
)
```

`sys.executable` permite utilizar el mismo intérprete de Python que ejecuta el
laboratorio dentro del entorno de Poetry.

### Manejo de errores

El programa controla:

- `FileNotFoundError`: falta un archivo requerido.
- `KeyError`: falta una opción de configuración o una columna.
- `ValueError`: un dato no puede convertirse correctamente.
- `ZoneInfoNotFoundError`: no existe la zona horaria configurada.
- `subprocess.CalledProcessError`: el subproceso terminó con error.

`ZoneInfoNotFoundError` se maneja antes de `KeyError`, ya que es una excepción
derivada de `KeyError`.

## Funciones implementadas

### `configure_logging()`

Configura el registro de mensajes en consola y archivo.

### `load_config()`

Lee y devuelve las opciones de `config.yaml`.

### `load_orders()`

Lee el archivo CSV, convierte sus filas y devuelve una lista de órdenes.

### `filter_orders()`

Selecciona las órdenes que cumplen el estado y monto mínimo configurados.

### `calculate_metrics()`

Calcula:

- Cantidad de órdenes.
- Monto total.
- Monto promedio.

### `get_report_datetime()`

Obtiene la fecha actual en la zona horaria configurada.

### `get_python_version()`

Obtiene la versión del intérprete mediante `subprocess`.

### `save_report()`

Guarda el reporte generado en formato JSON.

### `main()`

Coordina la ejecución completa y maneja los errores esperados.

## Dependencias agregadas

```cmd
poetry add pyyaml
poetry add tzdata
```

- `PyYAML`: permite leer archivos YAML.
- `tzdata`: proporciona la base de datos de zonas horarias en sistemas que no
  la incluyen, como puede ocurrir en Windows.

## Ejecución

Desde la raíz del proyecto:

```cmd
poetry run python labs\06_standard_library\main.py
```

## Resultado esperado

Con la configuración normal:

```yaml
minimum_total: 500
selected_status: completed
```

se seleccionan tres órdenes:

```text
ORD-3001
ORD-3003
ORD-3005
```

Las métricas esperadas son:

```text
Cantidad de órdenes: 3
Monto total: 4200.50
Monto promedio: 1400.17
```

## Prueba del nivel WARNING

Para comprobar el nivel `WARNING`, se cambió temporalmente:

```yaml
minimum_total: 5000
```

Como ninguna orden alcanzó ese monto, el programa registró:

```text
WARNING | Ninguna orden cumplió los filtros establecidos.
```

Después de la prueba, la configuración se restauró a:

```yaml
minimum_total: 500
```

## Validación de calidad

```cmd
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetry run mypy
poetry run pre-commit run --all-files
```

Mypy continúa revisando únicamente el archivo configurado en el Laboratorio 5.

## Evidencias

- `docs/evidence/lab06_execution.txt`
- `docs/evidence/lab06_warning.txt`
- `docs/evidence/lab06_ruff.txt`

## Resultado

Se implementó correctamente un proceso de entrada y salida que utiliza CSV,
YAML y JSON.

También se utilizaron rutas con `pathlib`, fechas con zona horaria, logging en
consola y archivo, ejecución de un subproceso y manejo de errores relacionados
con archivos, configuración, datos y zonas horarias.