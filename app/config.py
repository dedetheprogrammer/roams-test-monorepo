# == Setting up SQLite database in memory ================================
# https://stackoverflow.com/a/32681822
from flask_sqlalchemy import SQLAlchemy

# Instancia la base de datos utilizando SQLAlchemy. 
db = SQLAlchemy()

# Clase de configuración para la aplicación Flask. Aquí es donde se definen 
# las configuraciones relacionadas con la base de datos y otros parámetros.
class Config:
    """
    Esta clase contiene las configuraciones de la aplicación, en particular
    las relacionadas con la base de datos.
    """
    # URI de la base de datos. En este caso, se está utilizando SQLite en memoria.
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Esta configuración habilita el seguimiento de modificaciones de los objetos
    # de la base de datos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
