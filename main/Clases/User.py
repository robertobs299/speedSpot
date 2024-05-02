class User:
    def __init__(self, id_user, cp, sexo, email, telefono, nombre, apellidos):
        self.id_user = id_user
        self.cp = self.getCp(cp)
        self.sexo = self.getSexo(sexo)
        self.email = email
        self.telefono = telefono
        self.nombre = nombre
        self.apellidos = apellidos

    def getCp(cp):
        pass

    def getSexo(self, sexo):
        pass