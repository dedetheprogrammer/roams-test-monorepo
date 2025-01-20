import re
import dns.resolver
import smtplib
import socket

# Verificación del nombre
def verify_name(name):
    """
    Verifica si el nombre es válido. Debe contener solo caracteres alfabéticos y espacios.

    Args:
        name (str): Nombre a verificar.

    Returns:
        str: Cadena vacía si es válido, mensaje de error si no lo es.
    """
    # Verificación base: nombre vacío o solo espacios
    if not name or name.strip() == '':
        return ''
    
    # Primera verificación: solo letras y espacios permitidos
    NAME_REGEX = r'^[a-zA-Z\s]+$'
    if re.match(NAME_REGEX, name):
        return ''
    else:
        return 'El nombre solo puede contener caracteres y espacios'

# Verificación del DNI/NIE/CIF
def verify_dni(dni):
    """
    Verifica si el identificador DNI/NIE/CIF es válido.

    Args:
        dni (str): Identificador a verificar.

    Returns:
        str: Cadena vacía si es válido, mensaje de error si no lo es.
    """
    dni = dni.upper()  # Convertir a mayúsculas para consistencia.

    # Definiciones de patrones y validaciones de documentos
    LETTERS = 'TRWAGMYFPDXBNJZSQVHLCKE'
    DNI_REGEX = r'^(\d{8})([A-Z])$'
    NIE_REGEX = r'^[XYZ]\d{7}[A-Z]$'
    CIF_LETTERS = 'JABCDEFGHI'
    CIF_REGEX = r'^([ABCDEFGHJKLMNPQRSUVW])(\d{7})([0-9A-J])$'

    def aux_cif(n):
        """Auxiliar para calcular dígitos de control del CIF."""
        n = str(int(n) * 2)
        return sum(int(digit) for digit in n)

    # Verificación base: si el identificador está vacío
    if not dni or dni == '':
        return ''
    
    # Validar DNI
    if re.match(DNI_REGEX, dni, re.IGNORECASE):
        number = int(dni[:-1])
        control = dni[-1]
        if control != LETTERS[number % 23]:
            return 'DNI incorrecto'
    
    # Validar NIE
    elif re.match(NIE_REGEX, dni, re.IGNORECASE):
        number = int(dni[1:-1])
        control = dni[-1]
        if control != LETTERS[number % 23]:
            return 'NIE incorrecto'
    
    # Validar CIF
    elif re.match(CIF_REGEX, dni, re.IGNORECASE):
        letter = dni[0]
        number = dni[1:-1]
        control = dni[-1]

        fst_term = sum(int(number[i]) for i in range(1, 7, 2))
        snd_term = sum(aux_cif(number[i]) for i in range(0, 7, 2))
        end_term = (10 - (fst_term + snd_term) % 10) % 10

        try:
            if (letter in 'NPQRSW' and control != CIF_LETTERS[end_term]) or (letter not in 'NPQRSW' and int(control) != end_term):
                return 'CIF incorrecto'
        except:
            return 'CIF incorrecto'
    else:
        return f'Identificador {dni} no válido'
    
    return ''

# Verificación del correo electrónico
def verify_email(email):
    """
    Verifica si una dirección de correo electrónico es válida.

    Args:
        email (str): Dirección de correo a verificar.

    Returns:
        str: Cadena vacía si es válida, mensaje de error si no lo es.
    """
    # Verificación base: si el correo está vacío
    if not email or email == '':
        return ''
    
    # Verificación de formato de correo electrónico
    EMAIL_REGEX = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
    if not re.match(EMAIL_REGEX, email, re.IGNORECASE):
        return 'The email address is badly formatted'
    
    # Segunda verificación: existencia del dominio a través de consulta DNS
    domain = email.split('@')[1]
    try:
        record = dns.resolver.resolve(domain, 'MX')[0].exchange.to_text()[:-1]
    except Exception as error:
        print(error)
        return 'The email service does not exist'
    
    # Tercera verificación: probar el envío de un correo
    smtp = smtplib.SMTP()
    smtp.set_debuglevel(False)
    try:
        smtp.connect(record, 25)
        smtp.helo(socket.gethostname())
        smtp.mail('me@domain.com')
        code, _ = smtp.rcpt(email)
        smtp.quit()
        if code != 250:
            return 'The email does not exist'
    except Exception as error:
        print("Cannot verify the email:", error)
    
    return ''

# Verificación del capital prestado
def verify_capital(capital):
    """
    Verifica si el valor del capital prestado es válido.

    Args:
        capital (str | int): Valor del capital a verificar.

    Returns:
        str: Cadena vacía si es válido, mensaje de error si no lo es.
    """
    # Verificación base: si el valor es nulo
    if not capital or capital == '':
        return ''
    
    # Primera verificación: intentar convertir a entero
    try:
        capital = int(capital)
    except ValueError as error:
        print(error)
        return 'Invalid capital'
    
    # Segunda verificación: no puede ser negativo
    if capital < 0:
        return 'Capital cannot be negative'
    
    return ''

# Función principal para verificar un cliente
def verify_client(client):
    """
    Verifica los datos de un cliente mediante varias funciones de validación.

    Args:
        client (dict): Diccionario con los datos del cliente a verificar.

    Returns:
        dict: Diccionario con los errores encontrados, vacío si todo es válido.
    """
    errors = {}

    if "name" in client and (error := verify_name(client["name"])):
        errors["name"] = error
    if "dni" in client and (error := verify_dni(client["dni"])):
        errors["dni"] = error
    if "email" in client and (error := verify_email(client["email"])):
        errors["email"] = error
    if "capital" in client and (error := verify_capital(client["capital"])):
        errors["capital"] = error

    return errors