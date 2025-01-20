from config import db

# -- CLIENT --------------------------------------------------------------
class Client(db.Model):
    """
    ---
    description: Modelo que representa un cliente con sus datos personales y capital.
    properties:
        dni:
            type: string
            description: Documento Nacional de Identidad del cliente.
            example: "12345678A"
        name:
            type: string
            description: Nombre completo del cliente.
            example: "Juan Perez"
        email:
            type: string
            description: Correo electrónico del cliente.
            example: "juan.perez@example.com"
        capital:
            type: integer
            description: Capital financiero del cliente.
            example: 5000
        mortgages:
            type: array
            items:
                type: object
                properties:
                    id:
                        type: integer
                        description: ID de la hipoteca asociada al cliente.
                    amount:
                        type: integer
                        description: Monto de la hipoteca.
    """
    dni = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    capital = db.Column(db.Integer, nullable=True)
    # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_building_relationship.htm
    mortgages = db.relationship('Mortgage', back_populates='client', cascade="all, delete-orphan")

    # Get dictionary from client
    def get_dict(self):
        """
        Convierte la instancia del cliente a un diccionario.

        Returns:
            dict: Un diccionario con la información del cliente.
        Example:
            {
                "dni": "12345678A",
                "name": "Juan Pérez",
                "email": "juan.perez@example.com",
                "capital": 5000,
                "mortgages": []
            }
        """
        return {
            "dni": self.dni.upper(),
            "name": self.name,
            "email": self.email,
            "capital": self.capital,
            "mortgages": [mortgage.get_dict() for mortgage in self.mortgages]
        }

    # Representation 
    def __repr__(self):
        """
        Representacion en formato JSON del objeto Client.

        Returns:
            str: Representación JSON del objeto.
        Example:
            '{"dni": "12345678A", "name": "Juan Pérez", "email": "juan.perez@example.com", "capital": 5000, "mortgages": [...]}'
        """
        return json.dumps(self.get_dict())
