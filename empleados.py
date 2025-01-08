from datetime import date
class empleados():
    __id= 0
    __rut= ""
    __nombre= ""
    __app= ""
    __apm= ""
    __corr= ""
    __tel= 0
    __ant= 0
    __sal= 0
    __fech= date

    def _init_(self):
        pass

    def getID(self):
        return self.__id
    def setID(self, id):
        self.__id = id

    def getRut(self):
        return self.__rut
    def setRut(self, rut):
        self.__rut = rut

    def getNombre(self):
        return self.__nombre
    def setNombre(self, nom):
        self.__nombre = nom

    def getApellidoP(self):
        return self.__app
    def setApellidop(self, app):
        self.__app = app

    def getApellidoM(self):
        return self.__apm
    def setApellidoM(self,apm):
        self.__apm = apm

    def getCorreo(self):
        return self.__corr
    def setCorreo(self,corr):
        self.__corr = corr

    def getTelefono(self):
        return self.__tel
    def setTelefono(self,tel):
        self.__tel = tel

    def getAntiguedad(self):
        return self.__ant
    def setAntiguedad(self,ant):
        self.__ant = ant

    def getSalario(self):
        return self.__sal
    def setSalario(self,sal):
        self.__sal = sal

    def getFecha(self):
        return self.__fech
    def setFecha(self,fech):
        self.__fech = fech
