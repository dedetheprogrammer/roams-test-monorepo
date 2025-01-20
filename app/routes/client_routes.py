import sys
from config import db
from flask  import Blueprint, request
from models import Client, Mortgage
from services import verify_name, verify_dni, verify_email, verify_capital, verify_client, verify_mortgage

client_bp = Blueprint('client_routes', __name__)

@client_bp.route('/api/client', methods=['GET'])
def get_client_all():
    try:
        # Debug
        print("/api/client -- GET")
        # Obtener todos los clientes
        clients = db.session.query(Client).all()
        for i in range(len(clients)):
            clients[i] = clients[i].get_dict()
        # Return value
        return {"value": clients}, 200
    except Exception as e:
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500


@client_bp.route('/api/client/<dni>', methods=['GET'])
def get_client(dni):
    try:
        # Debug
        print("/api/client/<dni> -- GET. Received client: ", dni)
        # Verificar el DNI
        error  = verify_dni(dni)
        if error:
            return {"error": {"dni": error}}, 400
        # Obtencion del cliente de la base de datos
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        else:
            return client.get_dict(), 200
    except Exception as e:
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500


@client_bp.route('/api/client', methods=['POST'])
def add_client():
    try:
        # Verificar el cliente
        client = request.get_json()
        print("/api/client -- POST. Received client: ", client)
        # Verificar el cliente
        errors = verify_client(client)
        if errors:
            return {"error": errors}, 400
        # Agregar un nuevo cliente
        check = db.session.get(Client, client["dni"].lower())
        if check: 
            return {"error": {"client": f"Client under '{client["dni"]}' already exists"}}, 400 

        db.session.add(Client(dni=client["dni"].lower(), name=client["name"], email=client["email"], capital=client["capital"]))
        db.session.commit()
        return {"value": "New client added"}, 200
    except Exception as e:
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500


@client_bp.route('/api/client/<dni>', methods=['PATCH'])
def upd_client(dni):
    try:
        # Debug
        changes = request.get_json()
        print("/api/client -- PATCH. Received client:", dni, "and changes:", changes)
        # Verificar el cliente
        errors = verify_client(changes)
        if errors:
            return {"error": errors}, 400
        # Actualizar el cliente
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        if "name" in changes:
            client.name = changes["name"]
        if "email" in changes:
            client.email = changes["email"]
        if "capital" in changes:
            client.capital = changes["capital"]
        db.session.commit()
        return {"value": "OK"}, 200
    except Exception as e:
        print(e)
        return {"error": "Server internal error"}, 500


@client_bp.route('/api/client/<dni>', methods=['DELETE'])
def del_client(dni):
    try:
        # Debug
        print("/api/client -- DELETE. Received client: ", dni)
        # Verificar el DNI
        error  = verify_dni(dni)
        if error:
            return {"error": {"dni": error}}, 400
        # Delete client
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        db.session.delete(client)
        db.session.commit()
        return {"value":"Client deleted"}, 200
    except Exception as e:
        print(e)
        return {"error": "Server internal error"}, 500


@client_bp.route('/api/client/<dni>/mortgage', methods=['GET'])
def get_client_mortgage_all(dni):
    try:
        # Debug
        print("/api/client/<dni>/mortgage -- GET. Received client: ", dni)
        # Verificar el DNI
        error  = verify_dni(dni)
        if error:
            return {"error": {"dni": error}}, 400
        # Obtencion del cliente de la base de datos
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        else:
            return {"value": client.get_dict()['mortgages'] }
    except Exception as e:
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500


@client_bp.route('/api/client/<dni>/mortgage', methods=['POST'])
def add_client_mortgage(dni):
    try:
        # Debug
        changes = request.get_json()
        print("/api/client/<dni>/mortgage -- POST. Received client: ", dni)
        # Verificar el DNI
        error  = verify_dni(dni)
        if error:
            return {"error": {"dni": error}}, 400
        # Verificar parametros
        tae =  changes["tae"] if "tae" in changes else 0
        years = changes["years"] if "years" in changes else 0
        errors = verify_mortgage({"tae": tae, "years": years})
        if errors:
            return {"error": errors}, 400
        tae = int(tae)
        years = int(years)
        # Obtencion del cliente de la base de datos
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        else:
            mortgage = db.session.get(Mortgage, (tae, years))
            if not mortgage:
                print("not found")
                i = tae/(1200)
                n = years * 12
                monthly_fee = client.capital * i / (1 - (1 + i) ** -n)
                mortgage = Mortgage(dni=dni, tae=tae, years=years, monthly_fee=monthly_fee, client=client)
                db.session.add(mortgage)
                db.session.commit()
            return {"value": mortgage.get_dict()}
    except Exception as e:
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500

@client_bp.route('/api/client/<dni>/mortgage', methods=['DELETE'])
def del_client_mortgage(dni):
    try:
        # Debug
        changes = request.get_json()
        print("/api/client/<dni>/mortgage -- DELETE. Received client: ", dni)
        # Verificar el DNI
        error = verify_dni(dni)
        if error:
            return {"error": {"dni": error}}, 400
        # Verificar parametros
        tae =  changes["tae"] if "tae" in changes else 0
        years = changes["years"] if "years" in changes else 0
        errors = verify_mortgage({"tae": tae, "years": years})
        if errors:
            return {"error": errors}, 400
        tae = int(tae)
        years = int(years)
        # Obtencion del cliente de la base de datos
        client = db.session.get(Client, dni.lower())
        if not client:
            return {"error": f"No client associated with the identification {dni.upper()} given"}, 404
        else:
            mortgage = db.session.get(Mortgage, (tae, years))
            db.session.delete(mortgage)
            db.session.commit()
            return {"value":"Mortgage deleted"}, 200
    except Exception as e:
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500