import json
from config import db

# -- MORTGAGE ------------------------------------------------------------
class Mortgage(db.Model):
    """
    ---
    description: Modelo que representa una hipoteca asociada a un cliente.
    properties:
        dni:
            type: string
            description: Documento Nacional de Identidad del cliente asociado a la hipoteca.
            example: "12345678A"
        tae:
            type: integer
            description: Tasa Anual Equivalente (TAE) de la hipoteca.
            example: 3
        years:
            type: integer
            description: Numero de años de duracion de la hipoteca.
            example: 20
        monthly_fee:
            type: integer
            description: Cuota mensual de la hipoteca en euros.
            example: 500
        total_fee:
            type: integer
            description: Calculo del total a pagar durante la duracion completa de la hipoteca.
            example: 120000
    """
    dni = db.Column(db.String(9), db.ForeignKey('client.dni'), nullable=False)
    tae = db.Column(db.Integer, primary_key=True)
    years = db.Column(db.Integer, primary_key=True)
    monthly_fee = db.Column(db.Integer, nullable=False)
    client = db.relationship("Client", back_populates='mortgages')

    def get_dict(self):
        """
        Convierte la instancia de la hipoteca a un diccionario.

        Returns:
            dict: Un diccionario con la informacion de la hipoteca.

        Example:
            {
                "dni": "12345678A",
                "tae": 3,
                "years": 20,
                "monthly_fee": 500,
                "total_fee": 120000
            }
        """
        return {
            "dni": self.dni,
            "tae": self.tae,
            "years": self.years,
            "monthly_fee": self.monthly_fee,
            "total_fee": self.monthly_fee * self.years * 12,
        }

    def __repr__(self):
        """
        Representacion en formato JSON del objeto Mortgage.

        Returns:
            str: Representacion JSON del objeto.

        Example:
            '{"dni": "12345678A", "tae": 3, "years": 20, "monthly_fee": 500, "total_fee": 120000}'
        """
        return json.dumps(self.get_dict())