import sys
from config import db
from flask  import Blueprint, request
from models import Client, Mortgage
from services import verify_dni, verify_client, verify_mortgage
# Se define el Blueprint 'client_routes' para agrupar todas las rutas relacionadas con clientes
client_bp = Blueprint('client_routes', __name__)

# Ruta para obtener todos los clientes
@client_bp.route('/api/client', methods=['GET'])
def get_client_all():
    """
    Ruta para obtener todos los clientes.
    
    Metodo: GET
    URL: /api/client
    
    Respuesta esperada:
    Si hay clientes en la base de datos:
    {
        "value": [lista de clientes]
    }
    
    En caso de error:
    - 200: Si se pueden recuperar los clientes.
    - 500: Error interno del servidor.
    """
    try:
        # Debugging: Se imprime la solicitud recibida
        print("/api/client -- GET")
        # Se obtienen todos los clientes desde la base de datos
        clients = db.session.query(Client).all()
        # Se transforma la lista de clientes en formato de diccionario para enviar como respuesta
        for i in range(len(clients)):
            clients[i] = clients[i].get_dict()
        # Respuesta con todos los clientes
        return {"value": clients}, 200
    except Exception as e:
        # En caso de error, se imprime y se retorna un error 500
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500


# Ruta para obtener un cliente por su DNI
@client_bp.route('/api/client/<dni>', methods=['GET'])
def get_client(dni):
    """
    Ruta para obtener un cliente por su DNI.
    
    Metodo: GET
    URL: /api/client/<dni>
    
    Parametros:
    - dni: El DNI del cliente
    
    Respuesta esperada:
    Si el DNI es valido y el cliente existe:
    {
        "value": datos del cliente
    }
    
    En caso de error:
    - 200: Si el client existe y se puede recuperar.
    - 400: Si el DNI no es valido.
    - 404: Si no se encuentra un cliente con el DNI proporcionado.
    - 500: Error interno del servidor.
    """
    try:
        # Debugging: Se imprime el DNI recibido
        print("/api/client/<dni> -- GET. Received client: ", dni)
        # Verificacion del DNI
        error  = verify_dni(dni)
        if error:
            return {"error": {"dni": error}}, 400
        # Se obtiene el cliente desde la base de datos
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        else:
            # Respuesta con los datos del cliente
            return client.get_dict(), 200
    except Exception as e:
        # En caso de error, se imprime y se retorna un error 500
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500


# Ruta para agregar un nuevo cliente
@client_bp.route('/api/client', methods=['POST'])
def add_client():
    """
    Ruta para agregar un nuevo cliente.
    
    Metodo: POST
    URL: /api/client
    
    Parametros:
    Se espera un JSON con los siguientes campos:
    {
        "dni": "12345678A",
        "name": "Nombre del Cliente",
        "email": "cliente@example.com",
        "capital": 10000
    }

    Respuesta esperada:
    {
        "value": el cliente creado
    }
    
    Codigos de retorno:
    - 200: Si el cliente se ha agregado exitosamente.
    - 400: Si ya existe un cliente con el mismo DNI o si los datos son invalidos.
    - 500: Error interno del servidor.
    """
    try:
        # Se obtiene el cliente desde el cuerpo de la solicitud (JSON)
        changes = request.get_json()
        print("/api/client -- POST. Received client: ", changes)
        # Se verifica si los datos del cliente son validos
        errors = verify_client(changes)
        if errors:
            return {"error": errors}, 400
        # Se verifica si el cliente ya existe
        check = db.session.get(Client, changes["dni"].lower())
        if check:
            return {"error": {"client": f"Client under '{changes["dni"]}' already exists"}}, 400 
        # Se agrega el nuevo cliente a la base de datos
        client = Client(dni=changes["dni"].lower(), name=changes["name"], email=changes["email"], capital=changes["capital"])
        db.session.add(client)
        db.session.commit()
        # Respuesta indicando que el cliente se agrego correctamente
        return {"value": client.get_dict()}, 200
    except Exception as e:
        # En caso de error, se imprime y se retorna un error 500
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500


# Ruta para actualizar los datos de un cliente
@client_bp.route('/api/client/<dni>', methods=['PATCH'])
def upd_client(dni):
    """
    Ruta para actualizar los datos de un cliente.
    
    Metodo: PATCH
    URL: /api/client/<dni>
    
    Parametros:
    - dni: El DNI del cliente
    - datos: Un JSON con los campos a actualizar (pueden ser 'name', 'email', 'capital')
    
    Respuesta esperada:
    Si el cliente existe y se actualiza correctamente:
    {
        "value": el cliente actualizado
    }
    
    Codigos de retorno:
    - 200: El cliente se ha actualizado correctamente.
    - 400: Si los datos son invalidos.
    - 404: Si el cliente no existe.
    - 500: Error interno del servidor.
    """
    try:
        # Se obtiene la informacion de los cambios desde el cuerpo de la solicitud (JSON)
        changes = request.get_json()
        print("/api/client -- PATCH. Received client:", dni, "and changes:", changes)
        # Verificacion de los datos a actualizar
        changes["dni"] = dni
        errors = verify_client(changes)
        if errors:
            return {"error": errors}, 400
        # Se obtiene el cliente desde la base de datos
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        # Se actualizan los campos correspondientes
        if "name" in changes:
            client.name = changes["name"]
        if "email" in changes:
            client.email = changes["email"]
        if "capital" in changes:
            client.capital = changes["capital"]
        db.session.commit()
        # Respuesta indicando que los cambios fueron aplicados correctamente
        return {"value": client.get_dict()}, 200
    except Exception as e:
        # En caso de error, se imprime y se retorna un error 500
        print(e)
        return {"error": "Server internal error"}, 500


# Ruta para eliminar un cliente por su DNI
@client_bp.route('/api/client/<dni>', methods=['DELETE'])
def del_client(dni):
    """
    Ruta para eliminar un cliente por su DNI.
    
    Metodo: DELETE
    URL: /api/client/<dni>
    
    Parametros:
    - dni: El DNI del cliente a eliminar
    
    Respuesta esperada:
    Si el cliente se elimina correctamente:
    {
        "value": el cliente eliminado
    }
    
    Codigos de retorno:
    - 200: El cliente ha sido eliminado correctamente.
    - 400: Si el DNI no es valido.
    - 404: Si no se encuentra el cliente.
    - 500: Error interno del servidor.
    """
    try:
        # Se obtiene el cliente por su DNI
        print("/api/client -- DELETE. Received client: ", dni)
        # Verificacion del DNI
        error  = verify_dni(dni)
        if error:
            return {"error": {"dni": error}}, 400
        # Se obtiene el cliente desde la base de datos
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        # Se elimina el cliente
        db.session.delete(client)
        db.session.commit()
        return {"value": client.get_dict() }, 200
    except Exception as e:
        # En caso de error, se imprime y se retorna un error 500
        print(e)
        return {"error": "Server internal error"}, 500


# Ruta para obtener todas las hipotecas de un cliente
@client_bp.route('/api/client/<dni>/mortgage', methods=['GET'])
def get_client_mortgage_all(dni):
    """
    Ruta para obtener todas las hipotecas de un cliente.
    
    Metodo: GET
    URL: /api/client/<dni>/mortgage
    
    Parametros:
    - dni: El DNI del cliente
    
    Respuesta esperada:
    Si el DNI es valido y el cliente existe:
    {
        "value": [hipotecas]
    }
    
    En caso de error:
    - 200: Si el client existe y se puede recuperar.
    - 400: Si el DNI no es valido.
    - 404: Si no se encuentra un cliente con el DNI proporcionado.
    - 500: Error interno del servidor.
    """
    try:
        # Debugging: Se imprime el DNI recibido
        print("/api/client/<dni> -- GET. Received client: ", dni)
        # Verificacion del DNI
        error  = verify_dni(dni)
        if error:
            return {"error": {"dni": error}}, 400
        # Se obtiene el cliente desde la base de datos
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        else:
            # Respuesta con las hipotecas del cliente
            return client.get_dict()["mortgages"], 200
    except Exception as e:
        # En caso de error, se imprime y se retorna un error 500
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500

# Ruta para agregar una nueva hipoteca a un cliente
@client_bp.route('/api/client/<dni>/mortgage', methods=['POST'])
def add_client_mortgage(dni):
    """
    Ruta para agregar un nuevo cliente.
    
    Metodo: POST
    URL: /api/client
    
    Parametros:
    - DNI: identificador del cliente
    Se espera un JSON con los siguientes campos:
    {
        "tae": "20",
        "years": "1"
    }

    Respuesta esperada:
    {
        "value": la hipoteca creada
    }
    
    Codigos de retorno:
    - 200: Si la hipoteca se ha agregado exitosamente.
    - 400. Si los datos no son validos.
    - 404: Si no se encuentra un cliente con el DNI proporcionado.
    - 500: Error interno del servidor.
    """
    try:
        # Se obtiene el cliente desde el cuerpo de la solicitud (JSON)
        changes = request.get_json()
        print("/api/client/<dni>/mortgage -- POST. Received client: ", dni)
        # Se verifica si los datos del cliente son validos
        changes["dni"] = dni
        tae = changes["tae"] if changes["tae"] else 0
        years = changes["years"] if changes["years"] else 0
        errors = verify_mortgage(changes)
        if errors:
            return {"error": errors}, 400
        tae = int(tae)
        years = int(years)
        # Se verifica si el cliente ya existe
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        # Se agrega el nuevo cliente a la base de datos
        mortgage = db.session.get(Mortgage, (tae, years))
        if not mortgage:
            i = tae / 1200
            n = years * 12
            monthly_fee = (client.capital * i) / (1 - (1 + i) ** (-n)) 
            mortgage = Mortgage(dni=dni.lower(), tae=tae, years=years, monthly_fee=monthly_fee, client=client)
            db.session.add(mortgage)
            db.session.commit()
        # Respuesta indicando que el cliente se agrego correctamente
        return {"value": mortgage.get_dict()}, 200
    except Exception as e:
        # En caso de error, se imprime y se retorna un error 500
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500

# Ruta para eliminar la hipoteca de un cliente por su DNI, el TAE y el plazo
@client_bp.route('/api/client/<dni>/mortgage', methods=['DELETE'])
def del_client_mortgage(dni):
    """
    Ruta para eliminar un cliente por su DNI.
    
    Metodo: DELETE
    URL: /api/client/<dni>
    
    Parametros:
    - dni: El DNI del cliente a eliminar
    - Un JSON con el tae y el plazo de la hipoteca a eliminar:
    {
        "tae": "20",
        "years": "1"
    }
    
    Respuesta esperada:
    Si el cliente se elimina correctamente:
    {
        "value": la hipoteca eliminada
    }
    
    Codigos de retorno:
    - 200: La hipoteca ha sido eliminada correctamente.
    - 400: Si el alguno de los datos no es valido.
    - 404: Si no se encuentra el cliente o la hipoteca.
    - 500: Error interno del servidor.
    """
    try:
        # Se obtienen los datos desde el cuerpo de la solicitud (JSON)
        changes = request.get_json()
        print("/api/client -- POST. Received client: ", changes)
        # Se verifica si los datos del cliente son validos
        changes["dni"] = dni
        tae = changes["tae"] if changes["tae"] else 0
        years = changes["years"] if changes["years"] else 0
        errors = verify_mortgage(changes)
        if errors:
            return {"error": errors}, 400
        tae = int(tae)
        years = int(years)
        # Se obtiene el cliente desde la base de datos
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        mortgage = db.session.get(Mortgage, (tae, years))
        if not mortgage:
            return {"error": f"No mortgage associated with the given parameters"}, 404
        # Se elimina el cliente
        db.session.delete(mortgage)
        db.session.commit()
        return {"value": mortgage.get_dict() }, 200
    except Exception as e:
        # En caso de error, se imprime y se retorna un error 500
        print(e)
        return {"error": "Server internal error"}, 500