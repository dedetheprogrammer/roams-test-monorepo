import os
from config import db, Config
from flask import Flask, render_template
from routes import client_bp, mortgage_bp
from waitress import serve

# Se verifica desde que direccion IP y puerto de inicio del servidor
HOST = os.getenv("HOST", "127.0.0.1")
PORT = os.getenv("PORT", "8080")

# Se crea una instancia de la aplicación Flask
app = Flask(__name__)

# Se carga la configuración de la aplicación desde un objeto de configuración
# Config es un objeto que debe contener variables como HOST, PORT, DATABASE_URI, etc.
app.config.from_object(Config)

# Se registran los blueprints para las rutas de cliente y hipoteca
# Estos blueprints están definidos en otro lugar y contienen las rutas relacionadas
# con las operaciones CRUD para clientes y sus hipotecas.
app.register_blueprint(client_bp)
app.register_blueprint(mortgage_bp)

# Ruta principal que se activa cuando se hace una solicitud GET a la raíz "/"
@app.route("/")
def index():
    """
    Esta es la ruta principal de la aplicación. Su propósito es generar un
    índice que lista todas las rutas de la API registradas que comienzan con "/api".
    
    El resultado es una página web que muestra las rutas y sus métodos HTTP 
    correspondientes permitiendo ademas su uso en tiempo real.

    Respuesta:
        - HTML con la lista de rutas disponibles en la API.
    """
    # Lista para almacenar las rutas de la API que se mostrarán
    rules = []
    
    # Itera sobre todas las reglas de URL registradas en la aplicación
    for rule in app.url_map.iter_rules():
        try:
            # Si la ruta comienza con "/api", se agrega a la lista de reglas
            if rule.rule.startswith("/api"):
                rules.append({
                    "name": rule.rule,
                    "method": ''.join(rule.methods - {"HEAD", "OPTIONS"}),  # Excluye métodos HEAD y OPTIONS
                    # Intenta renderizar la plantilla HTML asociada con el endpoint
                    "html": render_template(f"{rule.endpoint.split('.')[-1]}.html", host=f'http://{HOST}', endpoint=rule.rule)
                })
        except:
            # Si hay un error al intentar renderizar la plantilla, se agrega una entrada
            rules.append({
                "name": rule.rule,
                "method": ''.join(rule.methods - {"HEAD", "OPTIONS"}),
                "html": '<p>No template defined</p>'  # Mensaje por defecto si no se encuentra una plantilla
            })
    
    # Renderiza la página HTML con la lista de reglas de la API
    return render_template("index.html", rules=rules)


# == Starting the server =================================================
# Esta sección se ejecuta cuando el archivo es ejecutado como script (python app.py)
if __name__ == '__main__':
    """
    Al ejecutar la aplicación, este bloque inicializa la base de datos y
    arranca el servidor web que gestionará las solicitudes entrantes.
    """

    # Inicializa la base de datos
    with app.app_context():
        # Establece la aplicación en el contexto de la base de datos
        db.init_app(app)
        # Crea las tablas de la base de datos si no existen
        db.create_all()
    
    # Arranca el servidor en el host y puerto especificados
    print(f"Serving server at http://{HOST}:{PORT}, you can use the API at this address.")
    # Llama a la función `serve` para iniciar el servidor web
    serve(app, host=HOST, port=PORT)
