from config import db, Config
from flask import Flask, render_template
from models import Client, Mortgage
from routes import client_bp, mortgage_bp
from waitress import serve

# from waitress import serve
HOST = '127.0.0.1'
PORT = 8080

# == Creating the server app =============================================
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(client_bp)
app.register_blueprint(mortgage_bp)

@app.route("/")
def index():
    rules = []
    for rule in app.url_map.iter_rules():
        try:
            if rule.rule.startswith("/api"):
                rules.append({
                    "name": rule.rule,
                    "method": ''.join(rule.methods - {"HEAD", "OPTIONS"}),
                    "html": render_template(f"{rule.endpoint.split('.')[-1]}.html", host=f'http://{HOST}', endpoint=rule.rule)
                })
        except:
            rules.append({
                "name": rule.rule,
                "method": ''.join(rule.methods - {"HEAD", "OPTIONS"}),
                "html": '<p>No template defined</p>'
            })
    return render_template("index.html", rules=rules)

# == Starting the server =================================================
if __name__ == '__main__':
    # Execute the database
    with app.app_context():
        db.init_app(app)
        db.create_all()
    # Execute the server
    print(f"Serving server at http://{HOST}:{PORT}, you can use the API at this address.")
    serve(app, host=HOST, port=PORT)
