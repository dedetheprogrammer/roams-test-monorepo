import sys
from config import db
from flask  import Blueprint
from models import Mortgage

mortgage_bp = Blueprint('mortgage_routes', __name__)

@mortgage_bp.route('/api/mortgage', methods=['GET'])
def get_mortgage_all():
    """
    Ruta para obtener todas las hipotecas
    
    Metodo: GET
    URL: /api/mortgage
    
    Parametros:
    - Ninguno
    
    Respuesta esperada:
    Lista con todos las hipotecas
    {
        "value": [...]
    }
    
    Codigos de retorno
    - 200: Todo bien
    - 500: Error interno del servidor
    """
    # Debug
    print("/api/mortgage -- GET")
    # Obtener todos los clientes
    try:
        mortgages = db.session.query(Mortgage).all()
        for i in range(len(mortgages)):
            mortgages[i] = mortgages[i].get_dict()
        # Return value
        return {"value": mortgages}, 200
    except Exception as e:
        print(e, file=sys.stderr)
        return {"error": "Server internal error"}, 500