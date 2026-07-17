# Laboratorio 05 — Tipado estático opcional y calidad

## Objetivo

Agregar anotaciones de tipos al código del laboratorio anterior y utilizar
mypy para verificar su consistencia de forma estática.

También se integró mypy al flujo de pre-commit junto con Ruff, isort y Black.

## Código analizado

El tipado se aplicó al archivo:

```text
labs/04_objects_models/main.py
```

Se eligió este laboratorio porque contiene:

- Dataclasses.
- Modelos Pydantic.
- Propiedades calculadas.
- Funciones de conversión.
- Listas de objetos.
- Valores opcionales y estados limitados.

## Conceptos utilizados

### Tipado dinámico

Python permite crear funciones y variables sin declarar explícitamente sus
tipos.

Por ejemplo:

```python
def calculate_total(price, quantity):
    return price * quantity
```

El tipo de cada valor se determina durante la ejecución.

### Anotaciones de tipos

Las anotaciones permiten indicar qué tipos espera y devuelve una función:

```python
def calculate_total(price: float, quantity: int) -> float:
    return price * quantity
```

Estas anotaciones sirven como documentación y pueden ser analizadas mediante
herramientas como mypy.

No impiden por sí mismas que Python reciba un valor de otro tipo durante la
ejecución.

### Mypy

Mypy es un verificador estático de tipos.

Analiza el código sin ejecutarlo y detecta inconsistencias como:

```python
quantity: int = "cinco"
```

En el laboratorio se ejecutó mypy antes y después de añadir las anotaciones
para conservar evidencia de la corrección del código.

### Literal

Se utilizó `Literal` para restringir los estados permitidos de una orden:

```python
OrderStatus = Literal[
    "pending",
    "completed",
    "cancelled",
]
```

Esto permite que mypy compruebe que el estado pertenezca al conjunto definido.

### Tipos de retorno

Se añadieron tipos de retorno a funciones, métodos y propiedades.

Ejemplos:

```python
def main() -> None:
```

```python
@property
def total(self) -> float:
```

```python
def convert_to_entity(order_input: OrderIn) -> Order:
```

### object

El método especial `__lt__()` acepta inicialmente un valor de tipo `object`:

```python
def __lt__(self, other: object) -> bool:
```

Después se comprueba que el objeto recibido sea una instancia de `Order`.

Esto permite manejar correctamente una posible comparación con otro tipo.

### Validación con Pydantic

Los diccionarios de entrada se validan mediante:

```python
OrderIn.model_validate(data)
```

Este método permite que Pydantic reciba datos externos, compruebe su
estructura y produzca un modelo validado.

Se utilizó `model_validate()` en lugar de desempaquetar directamente los
diccionarios porque mypy no podía garantizar el tipo específico de cada valor
contenido en un `dict[str, object]`.

## Herramientas de calidad

### Ruff

Detecta problemas de estilo, importaciones innecesarias y posibles errores.

### Black

Da formato automático al código.

### isort

Organiza las importaciones.

### Mypy

Comprueba la coherencia de las anotaciones de tipos.

### pre-commit

Ejecuta automáticamente las herramientas de calidad antes de aceptar un
commit.

## Configuración de mypy

La configuración se encuentra en `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.12"
files = ["labs/04_objects_models/main.py"]
disallow_untyped_defs = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true
```

Por ahora, mypy analiza únicamente el Laboratorio 4, ya que es el código
seleccionado para aplicar el ejercicio de tipado estático.

## Ejecución

### Verificación de tipos

```cmd
poetry run mypy
```

Resultado esperado:

```text
Success: no issues found in 1 source file
```

### Verificación completa de calidad

```cmd
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetry run mypy
poetry run pre-commit run --all-files
```

### Ejecución del código tipado

```cmd
poetry run python labs\04_objects_models\main.py
```

Las anotaciones no cambian el comportamiento del programa. La ejecución debe
producir los mismos resultados que antes de agregar los tipos.

## Evidencias

- `docs/evidence/lab05_mypy_before.txt`
- `docs/evidence/lab05_mypy_after.txt`
- `docs/evidence/lab05_precommit.txt`

## Resultado

Se añadieron anotaciones a funciones, métodos, propiedades, listas y estados.

Mypy inicialmente detectó funciones sin tipos y problemas al desempaquetar
diccionarios. Los errores fueron corregidos mediante anotaciones explícitas y
el uso de `model_validate()` de Pydantic.

La comprobación final de mypy y las herramientas integradas en pre-commit
terminaron correctamente.