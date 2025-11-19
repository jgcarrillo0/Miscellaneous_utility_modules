# -*- coding: utf-8 -*-
"""
Módulo de limpieza de texto.
Este módulo proporciona funciones para limpiar y normalizar texto, eliminando
espacios innecesarios y caracteres especiales. Incluye un decorador que valida
el tipo de entrada para asegurar que las funciones reciban un string o None.
"""

###############################################################################
# Importamos librerias
import re
from typing import (Optional,
                    Final,
                    Iterable,
                    Callable,
                    TypeVar)
from functools import wraps
# Final: Se usa para indicar que una variable no debe ser reasignada.
# Callable[[TipoArgumentos], TipoRetorno]: Se usa para indicar que un parámetro
# o variable es una función o cualquier objeto que pueda ser llamado.

# Sirve para indicar que una función, clase o decorador acepta cualquier tipo,
# y que el tipo de entrada se debe conservar como tipo de salida.
T = TypeVar("T")

################################################################################
# Decorador
def decorador_validar_texto(func: Callable[..., T]) -> Callable[..., Optional[T]]:
    '''
    Decorador que valida que el primer argumento `texto` sea str o None.
    - Si texto es None: retorna None directamente.
    - Si texto no es str: lanza TypeError.
    - Si texto es str: ejecuta la función original.    

    Parameters
    ----------
    func : Callable[..., T]
        Función que será decorada. Debe recibir como primer parámetro un argumento 
        llamado `texto`.

    Returns
    -------
    TYPE
        Una nueva función que envuelve a la original, garantizando la
        validación del parámetro `texto` antes de su ejecución.

    Raises
    ------
    TypeError
        Se lanza cuando el primer argumento recibido no es un string ni None.
    '''
    # @wraps(func) es un decorador cuyo objetivo es copiar la información de la
    # función original a la función interna (wrapper) que la reemplaza.
    @wraps(func)
    def wrapper(texto: Optional[str], *args, **kwargs) -> Optional[T]:
        if texto is None:
            return None

        if not isinstance(texto, str):
            raise TypeError(
                f"Se esperaba 'str' o None, pero se recibió {type(texto).__name__!r}"
            )
        return func(texto, *args, **kwargs)
    return wrapper

################################################################################
# Funciones
# Patrón compilado para mejorar rendimiento cuando la función se llama muchas veces.
PATRON_MULTIESPACIO: Final = re.compile(r"\s{2,}")

@decorador_validar_texto
def limpiar_espacios(texto: Optional[str]) -> Optional[str]:
    """
    Normaliza espacios innecesarios en un texto.

    - Reemplaza dos o más espacios consecutivos por un único espacio.
    - Elimina espacios al inicio y al final.
    - Si el valor es None, devuelve None.

    Parameters
    ----------
    texto : str | None
        Texto de entrada a limpiar.

    Returns
    -------
    str | None
        Texto con espacios normalizados o None si la entrada es None.
    """
    texto_limpio = PATRON_MULTIESPACIO.sub(" ", texto).strip()
    return texto_limpio

#-------------------------------------------------------------------------------
@decorador_validar_texto
def limpiar_caracteres(texto: Optional[str],
                       permitir_caracter: Iterable[str] = ()) -> Optional[str]:
    '''
    Limpia caracteres especiales de un texto, permitiendo ciertos caracteres específicos.
    - Elimina todos los caracteres especiales excepto letras, números, espacios
      y aquellos explícitamente permitidos.
    
    Parameters
    ----------
    texto : str | None
        Texto de entrada a limpiar.
    
    permitir_caracter : Iterable[str], optional
        Caracteres especiales que se desean conservar en el texto.
    
    Returns
    -------
    str | None
        Texto limpio o None si la entrada es None.
    '''
    # Escapa los caracteres permitidos para evitar problemas con regex
    caracteres_permitidos = re.escape("".join(permitir_caracter))

    # Construye la expresión regular
    patron = rf"[^a-zA-Z0-9\s{caracteres_permitidos}]"
    texto_limpio = re.sub(patron, "", texto)
    return texto_limpio
