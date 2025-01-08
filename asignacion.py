from sucursales import sucursales
from empleados import empleados

class asignacion():
    empleado = empleados()
    sucursal = sucursales()
    
    

    def __init__(self):
        pass

    def getID(self):
        return self.__id
    def setID(self, id):
        self.__id = id

