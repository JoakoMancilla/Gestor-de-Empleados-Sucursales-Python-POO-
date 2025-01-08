from funciones import funciones

class Principal():

    __f = funciones() #Hacemos una intancia (Privada) de la clase Funciones almacenandola en el atributo "f"

    def __init__(self):
        pass

    def ejecutarPrograma(self):
        self.__f.menuInicial()


p = Principal()
p.ejecutarPrograma()