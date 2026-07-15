# Laboratorio 02 - Fundamentos del lenguaje

## Objetivo

Crear un script que lea información desde un archivo JSON, filtre órdenes, calcule agraciones y maneje errores relacionados con archivos y formato.

## Conceptos utilizados

- Variables y tipos básicos.
- Listas y diccionarios.
- Condicionales.
- Ciclos `for`.
- Funciones.
- `match/case`.
- Expresiones regulares.
- Lectura de archivos JSON.
- Manejo de excepciones mediante `try/except`.

## Archivos

- `main.py`: contiene la lógica principal del laboratorio.
- `data/orders.json`: contiene órdenes válidas.
- `data/invalid_orders.json`: contiene un JSON incorrecto para probar el manejo de errores.

## Funcionaiento

El programa solicita el nombre de un archivo JSON. Si no se introduce ningún nombre, utiliza `orders.json`.

Posteriormente:

1. Lee las órdenes.
2. Filtra las órdenes con estado `completed`.
3. Conserva únicamente las órdenes con un total mayor o igual a 500.
4. Calcula el número de órdenes, el monto total y el promedio.
5. Muestra los resultados en la consola.

También verifica el formato de los códigos de orden mediante una expresión regular y utiliza `match/case` para traducir los estados.

## Ejecución

Desde la raíz del proyecto:

```cmd
poetry run python labs\02_fundamentals\main.py
```

Para utilizar el archivo predeterminado, se debe presionar Enter cuando el programa solicite el nombre del archivo.

## Casos de prueba manuales

### Archivo correcto
```
orders.json
```

### JSON inválido
```
invalid_orders.json
```

### Archivo inexistente
```
missing.json
```

## Validación de calidad

```cmd
poetry run ruff check .
poetry run isort --check-only .
poetry run black --check .
poetru run pre-commit run --all-files
```

## Resultado

El laboratorio proceso correctamente una lista de órdenes, aplica filtros, calcula agregaciones y controla errores de archivo inexistente y JSON incorrecto.