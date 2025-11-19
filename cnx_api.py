# -*- coding: utf-8 -*-
"""
Módulo para realizar solicitudes HTTP a APIs con manejo de tokens Bearer.
"""

###############################################################################
# Importamos librerias
from typing import Optional, Mapping, Any
import requests

################################################################################
# Funcion
def request_api(
    method: str,
    url: str,
    *, # Indica que los siguientes argumentos son solo keywords
    params: Optional[Mapping[str, Any]] = None,
    json_data: Optional[Mapping[str, Any]] = None,
    headers: Optional[Mapping[str, str]] = None,
    bearer_token: Optional[str] = None,
    session: Optional[requests.Session] = None,
    timeout: float = 15.0,
) -> requests.Response:
    """
    Realiza una solicitud HTTP a una API y retorna el objeto Response.
    Maneja automáticamente la inclusión de un token Bearer en los headers
    y deja propagar las excepciones de `requests`.

    Ejemplo de uso:
    >>> response = request_api(
    ...     method='GET',
    ...     url='https://api.example.com/data',
    ...     params={'key': 'value'},
    ...     bearer_token='your_token_here'
    ... )

    Parameters
    ----------
    method : str
        Método HTTP a utilizar (por ejemplo: 'GET', 'POST', 'PUT', 'DELETE').
    url : str
        URL del endpoint de la API.
    params : Optional[Mapping[str, Any]], optional
        Parámetros de la query string.
    json_data : Optional[Mapping[str, Any]], optional
        Cuerpo de la solicitud en formato JSON.
    headers : Optional[Mapping[str, str]], optional
        Headers HTTP adicionales.
    bearer_token : Optional[str], optional
        Token de autenticación Bearer. Si se envía y no existe un header
        'Authorization', se añadirá automáticamente.
    session : Optional[requests.Session], optional
        Sesión de `requests` para reutilizar conexiones. Recomendado cuando
        se realizan múltiples llamadas a la misma API.
    timeout : float, optional
        Tiempo máximo de espera para la solicitud en segundos.
        Por defecto, 15.0 segundos.

    Returns
    -------
    requests.Response
        Objeto Response de la solicitud HTTP realizada.

    Raises
    ------
    requests.exceptions.RequestException
        Si ocurre cualquier error durante la solicitud (conexión, timeout,
        HTTPError por códigos de estado >= 400, etc.).
    """
    # Normalizar método HTTP
    method = method.upper()

    # Preparación de headers (copiamos para no mutar el original)
    final_headers = dict(headers or {})

    # Inclusión del token Bearer si no existe Authorization
    if bearer_token and "Authorization" not in final_headers:
        final_headers["Authorization"] = f"Bearer {bearer_token}"

    # Selección de la función de solicitud
    request_func = session.request if session is not None else requests.request

    # Realización de la solicitud (dejamos que las excepciones se propaguen)
    response = request_func(
        method=method,
        url=url,
        params=params,
        json=json_data,
        headers=final_headers,
        timeout=timeout,
    )

    # Lanza una excepción requests.HTTPError si el código de estado es >= 400
    response.raise_for_status()

    return response
