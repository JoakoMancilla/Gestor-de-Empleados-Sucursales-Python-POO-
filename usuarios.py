class usuarios():
    __id= 0
    __nombre= ""
    __rut= ""
    __contraseña = ""
    __tip= 0

    def _init_(self):
        pass

    def getID(self):
        return self.__id
    def setID(self, id):
        self.__id = id

    def getNombre(self):
        return self.__nombre
    def setNombre(self, nom):
        self.__nombre = nom

    def getRut(self):
        return self.__rut
    def setRut(self, rut):
        self.__rut = rut

    def getContraseña(self):
        return self.__contraseña
    def setContraseña(self, con):
        self.__contraseña = con

    def getTipo(self):
        return self.__tip
    def setTipo(self,tip):
        self.__tip = tip
