import json
import logging
import time
from pathlib import Path

import httpx

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

API_OUTPUT_FILE = OUTPUT_DIR / "api_response.json"
DOWNLOAD_OUTPUT_FILE = OUTPUT_DIR / "httpbin_image.png"
LOG_FILE = LOG_DIR / "http_client.log"

JSON_URL = "https://httpbin.org/json"
DOWNLOAD_URL = "https://httpbin.org/image/png"
RETRY_TEST_URL = "https://httpbin.org/status/503"

RETRYABLE_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}


def configure_logging() -> None:
    """Configura el registro de mensajes en consola y archivo."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)


def is_retryable_status(status_code: int) -> bool:
    """Indica si un código HTTP permite realizar otro intento."""

    return status_code in RETRYABLE_STATUS_CODES


def wait_before_retry(
    attempt: int,
    delay: float,
    reason: str,
) -> None:
    """Registra el fallo y espera antes del siguiente intento."""

    logging.warning(
        "Intento %s fallido: %s. Nuevo intento en %.1f segundos.",
        attempt,
        reason,
        delay,
    )

    time.sleep(delay)


def get_with_retries(
    client: httpx.Client,
    url: str,
    max_attempts: int = 3,
    initial_delay: float = 0.5,
) -> httpx.Response:
    """Realiza una petición GET con reintentos y backoff."""

    delay = initial_delay

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.get(url)
            response.raise_for_status()

            return response

        except httpx.HTTPStatusError as error:
            status_code = error.response.status_code

            if not is_retryable_status(status_code) or attempt == max_attempts:
                raise

            wait_before_retry(
                attempt,
                delay,
                f"código HTTP {status_code}",
            )

        except httpx.RequestError as error:
            if attempt == max_attempts:
                raise

            wait_before_retry(
                attempt,
                delay,
                str(error),
            )

        delay *= 2

    raise RuntimeError("La petición terminó sin producir una respuesta.")


def fetch_json(
    client: httpx.Client,
    url: str,
) -> dict[str, object]:
    """Consulta una API y devuelve una respuesta JSON."""

    logging.info("Consultando la API: %s", url)

    response = get_with_retries(
        client,
        url,
        max_attempts=3,
        initial_delay=0.5,
    )

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError(
            "La respuesta JSON no contiene un objeto en su nivel principal."
        )

    logging.info(
        "La API respondió correctamente con código %s.",
        response.status_code,
    )

    return data


def save_json(
    data: dict[str, object],
    output_file: Path,
) -> Path:
    """Guarda una respuesta JSON en disco."""

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open(mode="w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    logging.info("La respuesta JSON fue guardada en %s.", output_file)

    return output_file


def download_streaming(
    client: httpx.Client,
    url: str,
    output_file: Path,
    max_attempts: int = 3,
    initial_delay: float = 0.5,
    chunk_size: int = 8192,
) -> Path:
    """Descarga un archivo por streaming con reintentos."""

    output_file.parent.mkdir(parents=True, exist_ok=True)

    temporary_file = output_file.with_suffix(f"{output_file.suffix}.part")

    delay = initial_delay

    for attempt in range(1, max_attempts + 1):
        try:
            logging.info(
                "Descargando archivo desde %s. Intento %s de %s.",
                url,
                attempt,
                max_attempts,
            )

            with client.stream("GET", url) as response:
                response.raise_for_status()

                with temporary_file.open(mode="wb") as file:
                    for chunk in response.iter_bytes(chunk_size=chunk_size):
                        file.write(chunk)

            temporary_file.replace(output_file)

            logging.info(
                "Archivo descargado correctamente en %s.",
                output_file,
            )

            return output_file

        except httpx.HTTPStatusError as error:
            temporary_file.unlink(missing_ok=True)

            status_code = error.response.status_code

            if not is_retryable_status(status_code) or attempt == max_attempts:
                raise

            wait_before_retry(
                attempt,
                delay,
                f"código HTTP {status_code}",
            )

        except httpx.RequestError as error:
            temporary_file.unlink(missing_ok=True)

            if attempt == max_attempts:
                raise

            wait_before_retry(
                attempt,
                delay,
                str(error),
            )

        except OSError:
            temporary_file.unlink(missing_ok=True)
            raise

        delay *= 2

    raise RuntimeError("La descarga terminó sin crear el archivo.")


def demonstrate_retries(client: httpx.Client) -> None:
    """Ejecuta una prueba controlada de reintentos HTTP."""

    logging.info("Iniciando prueba controlada de reintentos.")

    try:
        get_with_retries(
            client,
            RETRY_TEST_URL,
            max_attempts=3,
            initial_delay=0.5,
        )

    except httpx.HTTPStatusError as error:
        logging.info(
            "La prueba terminó como se esperaba con código HTTP %s.",
            error.response.status_code,
        )


def main() -> None:
    """Coordina las operaciones del cliente HTTP."""

    configure_logging()

    logging.info("Inicio del laboratorio de consumo HTTP.")

    timeout = httpx.Timeout(
        timeout=10.0,
        connect=5.0,
    )

    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            headers={
                "User-Agent": "python-training-orders/1.0",
                "Accept": "application/json, image/png",
            },
        ) as client:
            api_data = fetch_json(client, JSON_URL)

            json_file = save_json(
                api_data,
                API_OUTPUT_FILE,
            )

            downloaded_file = download_streaming(
                client,
                DOWNLOAD_URL,
                DOWNLOAD_OUTPUT_FILE,
            )

            demonstrate_retries(client)

        downloaded_size = downloaded_file.stat().st_size

        print()
        print("Procesamiento HTTP completado.")
        print(f"Respuesta JSON: {json_file}")
        print(f"Archivo descargado: {downloaded_file}")
        print(f"Tamaño descargado: {downloaded_size} bytes")

        logging.info("Laboratorio finalizado correctamente.")

    except httpx.TimeoutException as error:
        logging.error(
            "La operación superó el tiempo permitido: %s",
            error,
        )

    except httpx.HTTPStatusError as error:
        logging.error(
            "La API respondió con código HTTP %s para %s.",
            error.response.status_code,
            error.request.url,
        )

    except httpx.RequestError as error:
        logging.error(
            "No fue posible completar la petición a %s: %s",
            error.request.url,
            error,
        )

    except json.JSONDecodeError as error:
        logging.error(
            "La respuesta recibida no contiene JSON válido: %s",
            error,
        )

    except ValueError as error:
        logging.error("La respuesta recibida es inválida: %s", error)

    except OSError as error:
        logging.error(
            "No fue posible escribir un archivo en disco: %s",
            error,
        )


if __name__ == "__main__":
    main()
