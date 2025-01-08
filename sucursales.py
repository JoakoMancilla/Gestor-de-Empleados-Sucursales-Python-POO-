from datetime import date

class sucursales():
    __id=0
    __nombre= ""
    __direccion= ""
    __fecha=date

    def __init__(self):
        pass

    def getID(self):
        return self.__id
    def setID(self, id):
        self.__id = id

    def getNombre(self):
        return self.__nombre
    def setNombre(self, nom):
        self.__nombre = nom

    def getDireccion(self):
        return self.__direccion
    def setDireccion(self, direccion):
        self.__direccion = direccion

    def getFecha(self):
        return self.__fecha
    def setFecha(self, fecha):
        self.__fecha = fecha