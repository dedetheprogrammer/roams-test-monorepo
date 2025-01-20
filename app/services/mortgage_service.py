import sys

def verify_tae(tae):
    """
    Verifica la validez de la Tasa Anual Equivalente (TAE).

    Args:
        tae (str | int): Valor de la TAE a verificar.

    Returns:
        str: Mensaje de error si la validación falla, o cadena vacía si es válido.

    Example:
        >>> verify_tae("5")
        ''
        >>> verify_tae("-1")
        'TAE cannot be negative'
        >>> verify_tae("abc")
        'Invalid tae'
    """
    # Verificación base (si está vacío o no definido)
    if not tae or tae == '':
        return ''
    
    # Primera verificación: intentar convertir a entero
    try:
        tae = int(tae)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 'Invalid tae'
    
    # Segunda verificación: no puede ser negativo
    if tae < 0:
        return 'TAE cannot be negative'
    
    # Tercera verificación: no puede ser mayor a 100
    if tae > 100:
        return 'TAE cannot be greater than 100'
    
    # TAE válido
    return ''

def verify_years(years):
    """
    Verifica la validez de los años de duración de la hipoteca.

    Args:
        years (str | int): Número de años a verificar.

    Returns:
        str: Mensaje de error si la validación falla, o cadena vacía si es válido.

    Example:
        >>> verify_years("30")
        ''
        >>> verify_years("-5")
        'Years cannot be negative'
        >>> verify_years("abc")
        'Invalid years'
    """
    # Verificación base (si está vacío o no definido)
    if not years or years == '':
        return ''
    
    # Primera verificación: intentar convertir a entero
    try:
        years = int(years)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 'Invalid years'
    
    # Segunda verificación: no puede ser negativo
    if years < 0:
        return 'Years cannot be negative'
    
    # Valor de años válido
    return ''

def verify_mortgage(mortgage):
    """
    Verifica la validez de los datos de una hipoteca.

    Args:
        mortgage (dict): Diccionario con los datos de la hipoteca a verificar.

    Returns:
        dict: Diccionario con los errores encontrados, vacío si todo es válido.

    Example:
        >>> verify_mortgage({"tae": "5", "years": "20"})
        {}
        >>> verify_mortgage({"tae": "abc", "years": "20"})
        {'tae': 'Invalid tae'}
        >>> verify_mortgage({"tae": "5", "years": "-10"})
        {'years': 'Years cannot be negative'}
    """
    errors = {}

    # Validar TAE si está presente en la hipoteca
    if "tae" in mortgage and (error := verify_tae(mortgage["tae"])):
        errors["tae"] = error

    # Validar años si está presente en la hipoteca
    if "years" in mortgage and (error := verify_years(mortgage["years"])):
        errors["years"] = error

    return errors