from beautifultable import BeautifulTable
from cryptography.fernet import Fernet
from sucursales import sucursales
from asignacion import asignacion
from empleados import empleados
from usuarios import usuarios
from termcolor import colored
from tipos import tipos
from os import system
from DAO import DAO
import maskpass
import requests
import os



class funciones():
    __d = DAO()
    __tip = tipos
    __user = usuarios()
    __emple = empleados()
    __sucur = sucursales()
    __asignar = asignacion()



    def __init__(self):
        pass

#||------------------------------------------------------------------------------------------------------------------------||
#Inicio de Sesion(14.11) 

    def menuInicial(self):
        while True:
            try:
                system("cls")
                print(colored("===== MENU INICIAL =====", "light_blue"))
                print(colored("1.", "light_blue") + " Iniciar sesión")
                print(colored("2.", "light_blue") + " Comprobar conexión")
                print(colored("3.", "light_blue") + " Salir")
                opcion=int(input(colored("Seleccione una opcion del menu: ", "light_blue")))
                if opcion==1:
                    self.iniciarSesion()
                elif opcion==2:
                    self.__d.comprobarBD()
                elif opcion==3:
                    self.__salir()
                else:
                    print("ERROR: opción de menu principal incorrecta")
                    system("pause")
                    
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")

    def iniciarSesion(self):
        global rutAcces
        global conAcces
        try:
            while True:
                system("cls")
                print(colored("=== INICIO DE SESION ===", "light_blue"))
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                rutAcces = str(input(colored("Digite El Rut Del Usuario: ","light_blue")))
                if (len(rutAcces.strip())>9 and len(rutAcces.strip())<=10) and rutAcces[-2] == '-':
                    break
                elif (len(rutAcces.strip())==0):
                    self.menuInicial()
                else:
                    print(colored("El RUT Debe Tener Entre 11 y 12 Caracteres!! ---","light_yellow"))
                    system("pause")
        except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")

        try:
            while True:
                system("cls")
                print(colored("=== INICIO DE SESION ===", "light_blue"))
                conAcces = maskpass.askpass(colored("Digite su Contraseña: ","light_blue"))    # Maskpass deja ocultos los caracteres escritos
                if len(conAcces.strip())>=4 or len(conAcces.strip())<=20:
                    break
                else:
                    print(colored("La Contraseña Debe Tener Entre 4 y 20 Caracteres!! ---","light_yellow"))
                    system("pause")
        except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")
                self.menuInicial()

        try:
            self.user = self.__d.login(rutAcces, conAcces)
            if self.user is None:
                print(colored("Usuario y/o Contraseña son incorrectos...", "light_yellow"))
                system("pause")
                self.iniciarSesion()
            else:
                system("cls")
                print(colored("--- Credenciales Correctas!! ---","light_green"))
                print(f"--- Bienvenido(a) Usuario(a) ({ self.user.getNombre() })", end="\n\n")
                system("pause")
                if self.user.getTipo() == 1:
                    self.__menuAdmin()
                elif self.user.getTipo() == 2:
                    self.__menuAyuda()
        except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause") 

#||------------------------------------------------------------------------------------------------------------------------||
    #MENUS DE ACCESO (Segun Perfiles Admin & Mesa de Ayuda) (ACTUALIZADO 14.11)

    def __menuAdmin(self):
        while True:
            system("cls")
            try:
                print(colored("Sesion: ","light_blue") + "Administrador")
                print(colored("======MENU ADMIN======", "light_blue")) #(ACTUALIZADO 09.11) Este formato (Haciendo el pip install termcolor e importarlo) nos ayuda a dar color a prints 
                # Menú con números coloreados
                print(colored("1.", "light_blue") + " Empleados")
                print(colored("2.", "light_blue") + " Sucursal")
                print(colored("3.", "light_blue") + " Asignaciones")
                print(colored("4.", "light_blue") + " Recuperar datos JSON")
                print(colored("5.", "light_blue") + " Registrar nuevo usuario")
                print(colored("6.", "light_blue") + " Eliminar usuario")
                print(colored("7.", "light_blue") + " Cerrar Sesion")
                opcion=int(input(colored("Seleccione una opcion del menu: ", "light_blue")))
                if opcion==1:
                    self.__gestionarEmpleados()
                elif opcion ==2:
                    self.__gestionarSucursales()
                elif opcion==3:
                    self.__asignaciones()
                elif opcion==4:
                    self.__listaAPI()
                elif opcion==5:
                    self.__registrarUsuario()
                elif opcion==6:
                    self.__suprimirUsuario()
                elif opcion==7:
                    self.menuInicial()    
                else:
                    system("cls")
                    print(colored("Error, Opcion Incorrecta","light_yellow"))
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")              

    def __menuAyuda(self):
        while True:
            try:
                system("cls")
                print(colored("Sesion: ","light_blue") + "Gestor")
                print(colored("======MENU AYUDA======", "light_blue"))
                print(colored("1.", "light_blue") + "Agregar Asignacion")
                print(colored("2.", "light_blue") + "Listar Asignacion")
                print(colored("3.", "light_blue") + "Listar Empleados")
                print(colored("4.", "light_blue") + "Listar Sucursales")
                print(colored("5.", "light_blue") + "Cerrar sesion")
                opcion=int(input(colored("Seleccione una opcion del menu: ", "light_blue")))
                if opcion==1:
                    self.__crearAsignaciones()
                elif opcion==2:
                    self.__listarAsignaciones()
                elif opcion==3:
                    self.__listarEmpleados()
                elif opcion==4:
                    self.__listarSucursales()
                elif opcion==5:
                    self.menuInicial()
                else:
                    print("Error de opcion en el menu de ayuda..")
                    system("pause")
                    
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")

#||------------------------------------------------------------------------------------------------------------------------||
    #SUB-MENUS (EMPLEADOS Y SUCURSALES) (ACTUALIZADO 09.11)
    def __gestionarEmpleados(self):
        
        while True:
            try:
                system("cls")
                print(colored("===MENU EMPLEADOS===","light_green"))
                print(colored("1.", "light_green") + " Agregar Empleado")
                print(colored("2.", "light_green") + " Listar Empleado")
                print(colored("3.", "light_green") + " Modificar Empleado")
                print(colored("4.", "light_green") + " Eliminar empleado")
                print(colored("5.", "light_green") + " Volver")
                
                
                
                opcion=int(input(colored("Seleccione una opcion del menu: ", "light_green")))
                if opcion==1:
                    self.__crearEmpleado()
                elif opcion==2:
                    self.__listarEmpleados()
                elif opcion==3:
                    self.__actualizarEmpleado()
                elif opcion==4:
                    self.__eliminarEmpleado()
                elif opcion==5:
                    self.__retornarMenu()
                else:
                    system("cls")
                    print(colored("Error, Opcion Incorrecta","yellow"))
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

    def __gestionarSucursales(self):
        while True:
            try:
                system("cls")
                print(colored("===MENU SUCURSALES===","light_green"))
                print(colored("1.", "light_green") + " Agregar Sucursal")
                print(colored("2.", "light_green") + " Listar Sucursales")
                print(colored("3.", "light_green") + " Modificar Sucursales")
                print(colored("4.", "light_green") + " Eliminar Sucursales")
                print(colored("5.", "light_green") + " Volver")
                
                opcion=int(input(colored("Seleccione una opcion del menu: ", "light_green")))
                if opcion==1:
                    self.__crearSucursal()
                elif opcion==2:
                    self.__listarSucursales()
                elif opcion==3:
                    self.__actualizarSucursal()
                elif opcion==4:
                    self.__eliminarSucursal()
                elif opcion==5:
                    self.__retornarMenu()
                else:
                    system("cls")
                    print(colored("Error, Opcion Incorrecta","yellow"))
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

    def __asignaciones(self):
        while True:
            try:
                system("cls")
                print(colored("===MENU ASIGNACIONES===","light_green"))
                print(colored("1.", "light_green") + " Agregar Asignacion")
                print(colored("2.", "light_green") + " Listar Asignaciones")
                print(colored("3.", "light_green") + " Re-Asignar")
                print(colored("4.", "light_green") + " Volver")
                
                opcion=int(input(colored("Seleccione una opcion del menu: ", "light_green")))
                if opcion==1:
                    self.__crearAsignaciones()
                elif opcion==2:
                    self.__listarAsignaciones()
                elif opcion==3:
                    self.__reAsignacion()
                elif opcion==4:
                    self.__retornarMenu()
                else:
                    system("cls")
                    print(colored("Error, Opcion Incorrecta","yellow"))
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   
#||------------------------------------------------------------------------------------------------------------------------||
    #FUNCIONES EMPLEADOS (Actualizado 05.11)
    def __crearEmpleado(self):

        Registros = []                                  #Creamos Una variable(lista) para almacenar los datos de la bd y poder mostrarlos

        #Esta funcion (Tomada de Mostar Registros) nos permite validar si datos unicos (como RUT, Telefono, Correo) ya fueron Ingresados
        respuesta= self.__d.obtenerEmpleado()           #Llama a la fx de DAO que verifica registros
        for x in respuesta:
            Registros.append([x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]])

        #RUT (Actualizado 05.11)
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                rut=str(input("Ingrese el Rut del empleado: "))
                
                #Verificamos que este dato no este registrado 
                if any(rut == x[1] for x in respuesta):
                    system("cls")
                    print(colored("El Rut ya Existe...","yellow"))
                    system("pause")
                    self.__gestionarEmpleados()
                    break
                elif (len(rut.strip())==0):
                    self.__retornarMenu()
                elif (len(rut.strip())>9 and len(rut.strip())<=10) and rut[-2] == '-': #Valiodamos que el rut tenga los caracteres correspondientes y ademas le decimos que valide el digito verificador (guion) en la segunda psoicion de atras hacia adelante
                    break

                else:
                    system("cls")
                    print("El Rut debe tener entre 11 a 12 caracteres el el guion verificador")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        #Nombre
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                nom=str(input("Ingrese el Nombre del empleado: "))
                if len(nom.strip())>2 and len(nom.strip())<=20:
                    break
                elif (len(nom.strip())==0):
                    self.__retornarMenu()
                else:
                    system("cls")
                    print("El Nombre debe tener entre 2 a 20 caracteres")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        #Ape P
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                apep=str(input("Ingrese Apellido Paterno del empleado: "))
                if len(apep.strip())>2 and len(apep.strip())<=20:
                    break
                elif (len(apep.strip())==0):
                    self.__retornarMenu()
                else:
                    system("cls")
                    print(colored("El Apellido Paterno debe tener entre 1 a 20 caracteres","yellow"))
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        #Ape M
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                apem=str(input("Ingrese Apellido Materno del empleado: "))
                if len(apem.strip())>1 and len(apem.strip())<=20:
                    break
                elif (len(apem.strip())==0):
                    self.__retornarMenu()
                else:
                    system("cls")
                    print("El Apellido Materno debe tener entre 1 a 20 caracteres")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        #Correo (Actualizado 05.11)
        while True:
            # Solicita al usuario que ingrese un correo electrónico y valida que:
            # - Tenga entre 5 y 50 caracteres de longitud
            # - Contenga al menos un "@" en cualquier posición
            # - Termine en ".com" o ".cl"
            # Si cumple todas estas condiciones, se considera un correo válido; de lo contrario, es inválido.
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                correo=str(input("Ingrese el Correo del empleado: "))

                #Verificamos que este dato no este registrado 
                if any(correo == x[5] for x in respuesta):
                    system("cls")
                    print("Este Correo Esta Asociado a otro Empleado")
                    system("pause")
                elif (len(correo.strip())==0):
                    self.__retornarMenu()

                elif (len(correo.strip())>5 and len(correo.strip())<=50) and '@' in correo and (correo.endswith(".com") or correo.endswith(".cl")):
                    break
                else:
                    system("cls")
                    print("El correo electrónico es inválido. Asegúrate de que contenga '@' y termine en '.com' o '.cl'.")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        #Telefono (Actualizado 05.11)
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                tel=str(input("Ingrese el Telefono del empleado: (+56) 9 "))

                #Verificamos que este dato no este registrado 
                if any(tel == x[6] for x in respuesta):
                    system("cls")
                    print(colored("Este Telefono Esta Asociado a otro Empleado","yellow"))
                    system("pause")
                elif (len(tel.strip())==0):
                    self.__retornarMenu()

                elif len(tel.strip()) == 8:
                    break
                else:
                    system("cls")
                    print(colored("El Telefono debe tener entre 9 caracteres","yellow"))
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        #Antiguedad
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione 0 y luego ENTER","grey"))
                ant=int(input("Ingrese los años de antigüedad del empleado: "))
                if ant >= 1 and ant <= 30:
                    break
                elif ant == 0:
                    self.__retornarMenu()
                else:
                    system("cls")
                    print("La antigüedad debe ser de tipo numerico")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        #Salario
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione 0 y luego ENTER","grey"))
                sal=int(input("Ingrese su salario: "))
                if sal >= 500000 and sal <= 10000000:
                    break
                elif sal == 0:
                    self.__retornarMenu()
                else:
                    system("cls")
                    print("El salario mínimo es $500.000 y máximo $10.000.000")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        #Fecha Inicio Contrato (Actualizado 05.11)
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                contra=str(input("Ingrese la fecha de inicio del contrato (Formato DD-MM-YYYY): "))
                if len(contra.strip()) == 10 and contra[-5] == '-' and contra[-8] == '-':
                    break
                elif (len(contra.strip())==0):
                    self.__retornarMenu()
                else:
                    system("cls")
                    print("Error en agregar la fecha de inicio del empleado")
                    print("Siga la forma DD-MM-YYYY")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        self.__emple.setRut(rut)
        self.__emple.setNombre(nom)
        self.__emple.setApellidop(apep)
        self.__emple.setApellidoM(apem)
        self.__emple.setCorreo(correo)
        self.__emple.setTelefono(tel)
        self.__emple.setAntiguedad(ant)
        self.__emple.setSalario(sal)
        self.__emple.setFecha(contra)
        self.__d.agregarEmpleado(self.__emple)

        system("cls")
        print(colored("Empleado fue agregado correctamente","light_green"))
        system("pause")

    def __listarEmpleados(self):
        system("cls")
        respuesta= self.__d.obtenerEmpleado()           #llama a la fx de DAO que verifica registros
        if len(respuesta) == 0:
            print("No existen registros de Empleados en la tabla")
            system("pause")
        else:
            system("cls")
            print("===== EMPLEADOS (LISTA) =====")
            tabla= BeautifulTable()
            tabla.columns.header= [ "ID", "RUT", "NOMBRE","APELLIDO PATERNO", "APELLIDO MATERNO", "CORREO", "TELEFONO", "ANTIGUEDAD", "SALARIO", "INICIO CONTRATO"]
            for x in respuesta:
                tabla.rows.append([x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]])
            
            #(ACTUALIZADO 08.11)
            # Ajustar estilo para que las columnas se adapten al contenido
            tabla.set_style(BeautifulTable.STYLE_BOX)  # estilo cuadrado
            
            print(tabla)
            system("pause")
            self.__retornarMenu()

    #Actualizado (20.11)
    def __actualizarEmpleado(self):
        newRut= ""
        newNom= ""
        newApep= ""
        newApem= ""
        newCorreo= ""
        newTel= ""
        newSal= 0
        newContra= ""
        newAntig= 0
        Registros= []                                  #Creamos Una variable(lista) para almacenar los datos de la bd y poder mostrarlos

        #Esta funcion (Tomada de Mostar Registros) nos permite validar si datos unicos (como RUT, Telefono, Correo) ya fueron Ingresados
        respuesta= self.__d.obtenerEmpleado()           #Llama a la fx de DAO que verifica registros
        for x in respuesta:
            Registros.append([x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]])
        
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione 0 y luego ENTER","grey"))
                id = int(input(colored("Seleccione la ID del Empleado que desea modificar: ","light_magenta")))
                if any(id == x[0] for x in respuesta):
                    break
                elif id==0:
                    self.__retornarMenu()
                else:
                    print("No existen Registro para esta ID")
                    system("pause")
                
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")
        
        
        try:
            system("cls")
            print("Modificacion para: " + (colored(f"ID {id}","light_magenta")))
            print(colored("===== EMPLEADOS (ACTUALIZAR) =====","light_magenta"))
            print(colored("Seleccione el Tipo de datos que desa ACTUALIZAR: ","light_magenta"))
            print(colored("1.","light_magenta") + " Rut, Nombre & Apellidos")
            print(colored("2.","light_magenta") + " Correo  & Telefono")
            print(colored("3.","light_magenta") + " Salario")
            print(colored("4.","light_magenta") + " Fecha de Contrato & Antiguedad Laboral")
            print(colored("5.","light_magenta") + " Actualizar Todos Los Datos")
            print(colored("6.","light_magenta") + " Volver")
            dato =  int(input(colored("Seleccione una Opcion: ","light_magenta")))
            if dato == 1:
                #RUT UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newRut=str(input("Ingrese el Rut del empleado: "))
                        if any(newRut == x[1] for x in respuesta):
                            system("cls")
                            print(colored("El Rut ya Existe...","yellow"))
                            system("pause")
                        elif (len(newRut.strip())==0):
                            self.__retornarMenu()
                        elif (len(newRut.strip())>9 and len(newRut.strip())<=10) and newRut[-2] == '-': #Valiodamos que el rut tenga los caracteres correspondientes y ademas le decimos que valide el digito verificador (guion) en la segunda psoicion de atras hacia adelante
                            break
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                #Nombre UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newNom=str(input("Ingrese el Nombre del empleado: "))
                        if len(newNom.strip())>2 and len(newNom.strip())<=20:
                            break
                        elif (len(newNom.strip())==0):
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print("El Nombre debe tener entre 2 a 20 caracteres")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause") 
                #Ape P UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newApep=str(input("Ingrese Apellido Paterno del empleado: "))
                        if len(newApep.strip())>1 and len(newApep.strip())<=20:
                            break
                        elif (len(newApep.strip())==0):
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print(colored("El Apellido Paterno debe tener entre 1 a 20 caracteres","yellow"))
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                #Ape M UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newApem=str(input("Ingrese Apellido Materno del empleado: "))
                        if len(newApem.strip())>1 and len(newApem.strip())<=20:
                            break
                        elif (len(newApem.strip())==0):
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print("El Apellido Materno debe tener entre 1 a 20 caracteres")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause") 

            if dato == 2:
                #Correo UPDATE
                while True:
                    # Solicita al usuario que ingrese un correo electrónico y valida que:
                    # - Tenga entre 5 y 50 caracteres de longitud
                    # - Contenga al menos un "@" en cualquier posición
                    # - Termine en ".com" o ".cl"
                    # Si cumple todas estas condiciones, se considera un correo válido; de lo contrario, es inválido.
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newCorreo=str(input("Ingrese el Correo del empleado: "))

                        #Verificamos que este dato no este registrado 
                        if any(newCorreo == x[5] for x in respuesta):
                            system("cls")
                            print("Este Correo Esta Asociado a otro Empleado")
                            system("pause")
                        elif (len(newCorreo.strip())==0):
                            self.__retornarMenu()

                        elif (len(newCorreo.strip())>5 and len(newCorreo.strip())<=50) and '@' in newCorreo and (newCorreo.endswith(".com") or newCorreo.endswith(".cl")):
                            break
                        else:
                            system("cls")
                            print("El correo electrónico es inválido. Asegúrate de que contenga '@' y termine en '.com' o '.cl'.")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                #Telefono UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newTel=str(input("Ingrese el Telefono del empleado: (+56) 9 "))

                        #Verificamos que este dato no este registrado 
                        if any(newTel == x[6] for x in respuesta):
                            system("cls")
                            print(colored("Este Telefono Esta Asociado a otro Empleado","yellow"))
                            system("pause")
                        elif (len(newTel.strip())==0):
                            self.__retornarMenu()

                        elif len(newTel.strip()) == 8:
                            break
                        else:
                            system("cls")
                            print(colored("El Telefono debe tener entre 9 caracteres","yellow"))
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")

            if dato == 3:
                #Salario
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione 0 y luego ENTER","grey"))
                        newSal=int(input("Ingrese su salario: "))
                        if newSal >= 500000 and newSal <= 10000000:
                            break
                        elif newSal == 0:
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print("El salario mínimo es $500.000 y máximo $10.000.000")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                self.__d.updateSucursal(id,dato,newSal)

            if dato == 4:
                #Fecha Inicio Contrato UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newContra=str(input("Ingrese la fecha de inicio del contrato (Formato DD-MM-YYYY): "))
                        if len(newContra.strip()) == 10 and newContra[-5] == '-' and newContra[-8] == '-':
                            break
                        elif (len(newContra.strip())==0):
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print("Error en agregar la fecha de inicio del empleado")
                            print("Siga la forma DD-MM-YYYY")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                #Antiguedad UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione 0 y luego ENTER","grey"))
                        newAntig=int(input("Ingrese los años de antigüedad del empleado (Maximo 65 años): "))
                        if newAntig >= 1 and newAntig <= 65:
                            break
                        elif newAntig == 0:
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print("La antigüedad debe ser de tipo numerico")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")

            if dato == 5:
                #RUT UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newRut=str(input("Ingrese el Rut del empleado: "))
                        if any(newRut == x[1] for x in respuesta):
                            system("cls")
                            print(colored("El Rut ya Existe...","yellow"))
                            system("pause")
                            self.__gestionarEmpleados()
                            break
                        elif (len(newRut.strip())==0):
                            self.__retornarMenu()
                        elif (len(newRut.strip())>9 and len(newRut.strip())<=10) and newRut[-2] == '-': #Valiodamos que el rut tenga los caracteres correspondientes y ademas le decimos que valide el digito verificador (guion) en la segunda psoicion de atras hacia adelante
                            break
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                #Nombre UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newNom=str(input("Ingrese el Nombre del empleado: "))
                        if len(newNom.strip())>2 and len(newNom.strip())<=20:
                            break
                        elif (len(newNom.strip())==0):
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print("El Nombre debe tener entre 2 a 20 caracteres")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause") 
                #Ape P UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newApep=str(input("Ingrese Apellido Paterno del empleado: "))
                        if len(newApep.strip())>1 and len(newApep.strip())<=20:
                            break
                        elif (len(newApep.strip())==0):
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print(colored("El Apellido Paterno debe tener entre 1 a 20 caracteres","yellow"))
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                #Ape M UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newApem=str(input("Ingrese Apellido Materno del empleado: "))
                        if len(newApem.strip())>1 and len(newApem.strip())<=20:
                            break
                        elif (len(newApem.strip())==0):
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print("El Apellido Materno debe tener entre 1 a 20 caracteres")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause") 
                #Correo UPDATE
                while True:
                    # Solicita al usuario que ingrese un correo electrónico y valida que:
                    # - Tenga entre 5 y 50 caracteres de longitud
                    # - Contenga al menos un "@" en cualquier posición
                    # - Termine en ".com" o ".cl"
                    # Si cumple todas estas condiciones, se considera un correo válido; de lo contrario, es inválido.
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newCorreo=str(input("Ingrese el Correo del empleado: "))

                        #Verificamos que este dato no este registrado 
                        if any(newCorreo == x[5] for x in respuesta):
                            system("cls")
                            print("Este Correo Esta Asociado a otro Empleado")
                            system("pause")
                        elif (len(newCorreo.strip())==0):
                            self.__retornarMenu()

                        elif (len(newCorreo.strip())>5 and len(newCorreo.strip())<=50) and '@' in newCorreo and (newCorreo.endswith(".com") or newCorreo.endswith(".cl")):
                            break
                        else:
                            system("cls")
                            print("El correo electrónico es inválido. Asegúrate de que contenga '@' y termine en '.com' o '.cl'.")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                #Telefono UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newTel=str(input("Ingrese el Telefono del empleado: (+56) 9 "))

                        #Verificamos que este dato no este registrado 
                        if any(newTel == x[6] for x in respuesta):
                            system("cls")
                            print(colored("Este Telefono Esta Asociado a otro Empleado","yellow"))
                            system("pause")
                        elif (len(newTel.strip())==0):
                            self.__retornarMenu()

                        elif len(newTel.strip()) == 8:
                            break
                        else:
                            system("cls")
                            print(colored("El Telefono debe tener entre 9 caracteres","yellow"))
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                #Salario
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione 0 y luego ENTER","grey"))
                        newSal=int(input("Ingrese su salario: "))
                        if newSal >= 500000 and newSal <= 10000000:
                            break
                        elif newSal == 0:
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print("El salario mínimo es $500.000 y máximo $10.000.000")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                #Fecha Inicio Contrato UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                        newContra=str(input("Ingrese la fecha de inicio del contrato (Formato DD-MM-YYYY): "))
                        if len(newContra.strip()) == 10 and newContra[-5] == '-' and newContra[-8] == '-':
                            break
                        elif (len(newContra.strip())==0):
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print("Error en agregar la fecha de inicio del empleado")
                            print("Siga la forma DD-MM-YYYY")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")
                #Antiguedad UPDATE
                while True:
                    try:
                        system("cls")
                        print(colored("Para Volver al Menu Presione 0 y luego ENTER","grey"))
                        newAntig=int(input("Ingrese los años de antigüedad del empleado (Maximo 65 años): "))
                        if newAntig >= 1 and newAntig <= 65:
                            break
                        elif newAntig == 0:
                            self.__retornarMenu()
                        else:
                            system("cls")
                            print("La antigüedad debe ser de tipo numerico")
                            system("pause")
                    except Exception as e:
                        system("cls")
                        print(colored(f"Detalles del error: {e}","red"))
                        system("pause")

            if dato == 6:
                self.__retornarMenu()

            self.__d.updateEmpleado(id,dato,newRut,newNom,newApep,newApem,newCorreo,newTel,newSal,newContra,newAntig)

        except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")

    #Actualizado (19.11)
    def __eliminarEmpleado(self):
        system("cls")
        #===========PRIMERA VALIDACION (VERIFICAR EXISTENCIA DE LA ID EN EMPLEADOS)===========
        Registros = []
        respuesta = self.__d.obtenerEmpleado()
        for x in respuesta:
            Registros.append([x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]]) 
        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey")) 
        id=int(input(colored("Ingrese el ID del Empleado que desea eliminar: ","light_magenta")))
        #Verificamos que este dato no este registrado
        if any(id == x[0] for x in respuesta):
            system("cls")
            #===========SEGUNDA VALIDACION (VERIFICAR SI EL EMPLEADO ESTA ASOCIADO A UNA EMPRESA)===========
            RegistrosAsig = []
            respuesta= self.__d.obtenerAsignaciones()
            for x in respuesta:
                RegistrosAsig.append([x[0], x[1], x[2]])
            while True:                                             # Dato 1 ID EMPLEADO
                try:
                    if any(id == x[1] for x in respuesta):
                        system("cls")
                        print(colored("Error al eliminar el empleado...","red"))
                        print(colored("El Empleado se encuentra Asignado a una Sucursal","light_yellow"))
                        system("pause")
                        self.__retornarMenu()
                    else:
                        system("cls")
                        print(colored(f"Empleado {id} fue eliminado correctamente...","light_green"))
                        self.__d.deleteEmpleado(id)
                        system("pause")
                        self.__retornarMenu()
                        
                except Exception as e:
                    system("cls")
                    print(colored(f"Detalles del error: {e}","red"))
                    system("pause")
        else:
            system("cls")
            print(colored("El ID ingresado no existe...","light_yellow"))
            system("pause")
            self.__retornarMenu()

#||------------------------------------------------------------------------------------------------------------------------||
    #FUNCIONES SUCURSALES (Actualizado 05.11)
    def __crearSucursal(self):
        
        #NOMBRE SUCURSAL
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                nom=str(input("Ingrese nombre de la sucursal: "))
                if len(nom.strip())>1 and len(nom.strip())<=50:
                    break
                elif (len(nom.strip())==0):
                    self.__retornarMenu()
                else:
                    system("cls")
                    print("El Nombre debe tener entre 1 a 50 caracteres")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        #DIRECCION SUCURSAL
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                dir=str(input("Ingrese la Direccion de la sucursal: "))
                if len(dir.strip())>1 and len(dir.strip())<=100:
                    break
                elif (len(dir.strip())==0):
                    self.__retornarMenu()
                else:
                    print("EL campo de dirección no puede quedar vacio")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        #FECHA SUCURSAL (Actualizado 05.11)
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                fech=str(input("Ingrese fecha de Constitucion Legal de la Sucursal: "))
                if len(fech.strip()) == 10 and fech[-5] == '-' and fech[-8] == '-':
                    break
                elif (len(fech.strip())==0):
                    self.__retornarMenu()
                else:
                    system("cls")
                    print("Error en agregar la fecha de Constitucion Legal de la Sucursal")
                    print("Siga la forma DD-MM-YYYY")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        self.__sucur.setNombre(nom)
        self.__sucur.setDireccion(dir)
        self.__sucur.setFecha(fech)
        self.__d.agregarSucursal(self.__sucur)

        print("La sucursal fue agregada correctamente")
        system("pause")
    
    def __listarSucursales(self):
        system("cls")
        respuesta= self.__d.obtenerSucursal()           #llama a la fx de DAO que verifica registros
        if len(respuesta) == 0:
            print("No existen registros de Sucursales en la tabla")
            system("pause")
        else:
            system("cls")
            print("===== EMPLEADOS (LISTA) =====")
            tabla= BeautifulTable()
            tabla.columns.header= [ "ID", "NOMBRE SUCURSAL", "DIRECCIÓN", "FECHA"]
            for x in respuesta:
                tabla.rows.append([x[0], x[1], x[2] , x[3]])
            
            #(ACTUALIZADO 08.11)
            # Ajustar estilo para que las columnas se adapten al contenido
            tabla.set_style(BeautifulTable.STYLE_BOX)  # estilo cuadrado
            
            print(tabla)
            system("pause")
            self.__retornarMenu()

    #Actualizado (20.11)
    def __actualizarSucursal(self):
        newDir= ""
        newFec= ""
        newNom= ""
        Registros = []                                  #Creamos Una variable(lista) para almacenar los datos de la bd y poder mostrarlos

        #Esta funcion (Tomada de Mostar Registros) nos permite validar si datos unicos (como RUT, Telefono, Correo) ya fueron Ingresados
        respuesta= self.__d.obtenerSucursal()           #Llama a la fx de DAO que verifica registros
        for x in respuesta:
            Registros.append([x[0], x[1], x[2] , x[3]])
        
        while True:
            try:
                system("cls")
                print(colored("Para Volver al Menu Presione 0 y luego ENTER","grey"))
                id = int(input(colored("Seleccione la ID de la Sucursal que desea modificar: ","light_magenta")))
                if any(id == x[0] for x in respuesta):
                    break
                elif id==0:
                    self.__retornarMenu()
                else:
                    print("No existen Registro para esta ID")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")
        try:
            system("cls")
            print("===== SUCURSAL (ACTUALIZAR) =====")
            print("Seleccione el Tipo de datos que desa ACTUALIZAR: ")
            print("1. Nombre")
            print("2. Direccion")
            print("3. Fecha de Constitucion Legal")
            print("4. Actualizar Todos Los Datos")
            print("5. Volver")
            dato =  int(input("Seleccione una Opcion: "))
            
            if dato == 1:
                #SOLO Nombre UPDATE
                while True:
                    system("cls")
                    print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                    newNom= str(input("Ingrese El Nuevo Nombre: "))
                    if len(newNom.strip())>1 and len(newNom.strip())<=50:
                        break
                    elif (len(newNom.strip())==0):
                        self.__retornarMenu()
                    else:
                        system("cls")
                        print("El Nombre debe tener entre 1 a 50 caracteres")
                        system("pause")

            if dato == 2:
                #SOLO Direccion UPDATE
                while True:
                    system("cls")
                    print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                    newDir= str(input("Ingrese La Nueva Direccion: "))
                    if len(newDir.strip())>1 and len(newDir.strip())<=100:
                        break
                    elif (len(newDir.strip())==0):
                        self.__retornarMenu()
                    else:
                        system("cls")
                        print("El Nombre debe tener entre 2 a 20 caracteres")
                        system("pause")

            if dato == 3:
                #SOLO Fecha de Cons. Legal UPDATE
                while True:
                    system("cls")
                    print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                    newFec= str(input("Ingrese La Nueva Fecha de Cons. Legal: "))
                    if len(newFec.strip()) == 10 and newFec[-5] == '-' and newFec[-8] == '-':
                        break
                    elif (len(newFec.strip())==0):
                        self.__retornarMenu()
                    else:
                        system("cls")
                        print("El Nombre debe tener entre 2 a 20 caracteres")
                        system("pause")

            if dato == 4:
                #Nombre UPDATE
                while True:
                    system("cls")
                    print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                    newNom= str(input("Ingrese El Nuevo Nombre: "))
                    if len(newNom.strip())>2 and len(newNom.strip())<=20:
                        break
                    elif (len(newNom.strip())==0):
                        self.__retornarMenu()
                    else:
                        system("cls")
                        print("El Nombre debe tener entre 2 a 20 caracteres")
                        system("pause")
                #Direccion UPDATE
                while True:
                    system("cls")
                    print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                    newDir= str(input("Ingrese La Nueva Direccion: "))
                    if len(newDir.strip())>1 and len(newDir.strip())<=100:
                        break
                    elif (len(newDir.strip())==0):
                        self.__retornarMenu()
                    else:
                        system("cls")
                        print("El Nombre debe tener entre 2 a 20 caracteres")
                        system("pause")
                #Fecha de Cons. Legal UPDATE
                while True:
                    system("cls")
                    print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                    newFec= str(input("Ingrese La Nueva Fecha de Cons. Legal: "))
                    if len(newFec.strip()) == 10 and newFec[-5] == '-' and newFec[-8] == '-':
                        break
                    elif (len(newFec.strip())==0):
                        self.__retornarMenu()
                    else:
                        system("cls")
                        print("El Nombre debe tener entre 2 a 20 caracteres")
                        system("pause")

            if dato == 5:
                self.__retornarMenu()

            self.__d.updateSucursal(id,dato,newNom,newDir,newFec)

        except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")

    #Actualizado (19.11)
    def __eliminarSucursal(self):
        system("cls")
        #===========PRIMERA VALIDACION (VERIFICAR EXISTENCIA DE LA ID EN SUCURSAL)===========
        Registros = []
        respuesta = self.__d.obtenerSucursal()
        for x in respuesta:
            Registros.append([x[0], x[1], x[2]]) 
        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey")) 
        id=int(input(colored("Ingrese el ID de la Sucursal que desea eliminar: ","light_magenta")))
        #Verificamos que este dato no este registrado
        if any(id == x[0] for x in respuesta):
            system("cls")
            #===========SEGUNDA VALIDACION (VERIFICAR SI LA SUCURSAL ESTA ASOCIADA A UN EMPLEADO)===========
            RegistrosAsigSuc = []
            respuesta= self.__d.obtenerAsignaciones()
            for x in respuesta:
                RegistrosAsigSuc.append([x[0], x[1], x[2]])
            while True:                                             # Dato 1 ID SUCURSAL
                try:
                    if any(id == x[2] for x in respuesta):
                        system("cls")
                        print(colored("Error al eliminar la sucursal...","red"))
                        print(colored("La sucursal se encuentra asignada a un empleado","light_yellow"))
                        system("pause")
                        self.__retornarMenu()
                    else:
                        system("cls")
                        print(colored(f"Sucursal {id} fue eliminada correctamente...","light_green"))
                        self.__d.deleteSucursal(id)
                        system("pause")
                        self.__retornarMenu()
                        
                except Exception as e:
                    system("cls")
                    print(colored(f"Detalles del error: {e}","red"))
                    system("pause")
        else:
            system("cls")
            print(colored("El ID ingresado no existe...","light_yellow"))
            system("pause")
            self.__retornarMenu()
        
#||------------------------------------------------------------------------------------------------------------------------||
    #ASIGNACIONES (Actualizado 06.11)
    def __crearAsignaciones(self):

        RegistrosAsig = []                                  #Creamos Una variable(lista) para almacenar los datos de la bd y poder mostrarlos

        #Esta funcion (Tomada de Mostar Registros) nos permite validar si datos unicos que no deberian repetirse en la tabla Nub (como la Id del empleado) ya fueron Ingresados
        respuesta= self.__d.obtenerAsignaciones()           #Llama a la fx de DAO que verifica registros
        for x in respuesta:
            RegistrosAsig.append([x[0], x[1], x[2]])

        while True:                                             # Dato 1 ID EMPLEADO
            try:
                system("cls")
                print(colored('Para Volver al Menu Presione "0" y luego ENTER',"grey"))
                id1=int(input("Ingrese el ID de Empleado: "))

                #Verificamos que este dato no este registrado (id 1 correspondiente a la id del empleado que no debe repetirse)
                if any(id1 == x[1] for x in respuesta):
                    system("cls")
                    print("El Empleado ya esta Asignado a una Sucursal")
                    system("pause")

                elif id1 >= 1 and id1 <= 100:
                    break
                elif id1 == 0:
                    self.__retornarMenu()
                else:
                    system("cls")
                    print("El ID debe tener entre 1 a 20 caracteres")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   
        
        while True:                                             # Dato 2 ID SUCURSAL
            try:
                system("cls")
                print(colored('Para Volver al Menu Presione "0" y luego ENTER',"grey"))
                id2=int(input("Ingrese el ID de Sucursal: "))
                if id2 >= 1 and id2 <= 100:
                    break
                elif id2 == 0:
                    self.__retornarMenu()
                else:
                    system("cls")
                    print("El ID debe tener entre 1 a 20 caracteres")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")   

        system("cls")
        print(colored("Datos Asignados Correctamente!!","light_green"))
        self.__asignar.empleado.setID(id1)
        self.__asignar.sucursal.setID(id2)
        self.__d.agregarAsignaciones(self.__asignar)
        
        system("pause")

    def __listarAsignaciones(self):
        system("cls")
        respuesta= self.__d.obtenerAsignaciones()
        if len(respuesta) == 0:
            print("No existen registros en la tabla")
            system("pause")
        else:
            system("cls")
            print("===== ASIGNACIONES (LISTA) =====")
            tabla= BeautifulTable()
            tabla.columns.header= [ "ID", "ID EMP.", "NOMBRE", "ID SUC.", "SUCURSAL"]
            for x in respuesta:
                tabla.rows.append([ x[0], x[1], x[2], x[3], x[4] ])
            
            #(ACTUALIZADO 08.11)
            # Ajustar estilo para que las columnas se adapten al contenido
            tabla.set_style(BeautifulTable.STYLE_BOX)  # estilo cuadrado
            
            print(tabla)
            system("pause")
            self.__retornarMenu()

    def __reAsignacion(self):
        system("cls")
        #===========PRIMERA VALIDACION (VERIFICAR EXISTENCIA DE LA ID EN SUCURSAL)===========
        Registros = []
        respuesta1 = self.__d.obtenerAsignaciones()
        for x in respuesta1:
            Registros.append([x[0], x[1], x[2]]) 
        print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey")) 
        id=int(input(colored("Ingrese el ID de la Asignacion: ","light_magenta")))
        #Verificamos que este dato no este registrado
        if any(id == x[0] for x in respuesta1):
            system("cls")
            #===========SEGUNDA VALIDACION (VERIFICAR SI LA SUCURSAL ESTA ASOCIADA A UN EMPLEADO)===========
            RegistrosAsigSuc = []
            respuesta2= self.__d.obtenerSucursal()
            for x in respuesta2:
                RegistrosAsigSuc.append([x[0], x[1], x[2]])
            while True:                                             # Dato 1 ID SUCURSAL
                try:
                    system("cls")
                    idnew = int(input(colored("ID de la sucursal por la cual reemplazaremos la anterior: ","light_magenta")))
                    if any(idnew == x[0] for x in respuesta2):
                        system("cls")
                        print(colored("La Re-Asignacion Fue Exitosa!!","light_green"))
                        system("pause")
                        self.__d.updateAsignaciones(id,idnew)
                        self.__retornarMenu()
                    else:
                        system("cls")
                        print(colored(f"No se ha encontrado Sucursal con ID {idnew}","light_yellow"))
                        system("pause")
                        self.__retornarMenu()
                except Exception as e:
                    system("cls")
                    print(colored(f"Detalles del error: {e}","red"))
                    system("pause")
        else:
            system("cls")
            print(colored("El ID ingresado no existe...","light_yellow"))
            system("pause")
            self.__retornarMenu()
#||------------------------------------------------------------------------------------------------------------------------||
    def __listaAPI(self):
        # Realizamos la solicitud a la API
        respuesta = requests.get("https://elprofemiguel.com/APIS_JSON/afp_api.json")

        # Verificamos si la solicitud fue exitosa
        if respuesta.status_code == 200:
            # Convertimos la respuesta JSON en un diccionario
            datos = respuesta.json()

            # Aseguramos que estamos trabajando con la clave 'listado_afps'
            listado_afps = datos.get('listado_afps', [])

            # Creamos la tabla
            tabla = BeautifulTable()
            tabla.columns.header = ["ID", "NOMBRE", "DETALLES", "VALOR CUOTA", "CALLE", "NUMERO", "CIUDAD"]

            # Iteramos sobre las AFPs en 'listado_afps' para agregar las filas a la tabla
            for item in listado_afps:
                detalles = item.get("detalles", {})
                direccion = detalles.get("direccion", {})
                
                # Agregar una fila con todos los valores, asegurándonos de que todos estén presentes
                tabla.rows.append([
                    item.get("id", ""),  # Obtiene el ID
                    item.get("nombre", ""),  # Obtiene el nombre
                    f"Valor Cuota: {detalles.get('valor_cuota', '')}, Sucursal: {detalles.get('telefono', {}).get('sucursal', '')}",  # Detalles adicionales
                    detalles.get("valor_cuota", ""),  # Obtiene el valor de la cuota
                    direccion.get("calle", ""),  # Obtiene la calle
                    direccion.get("numero", ""),  # Obtiene el número
                    direccion.get("ciudad", ""),  # Obtiene la ciudad
                ])
            
            # Damos estilo a la tabla
            tabla.set_style(BeautifulTable.STYLE_BOX)

            # Mostramos la tabla
            system("cls")
            print(tabla)
            system("pause")
            system("cls")

        else:
            print(f"Error en la solicitud: {respuesta.status_code}")
#||------------------------------------------------------------------------------------------------------------------------||

    def __registrarUsuario(self):
        Registros = []                                  #Creamos Una variable(lista) para almacenar los datos de la bd y poder mostrarlos

        #Esta funcion (Tomada de Mostar Registros) nos permite validar si datos unicos (como RUT,) ya fueron Ingresados
        respuesta= self.__d.comprobarUsuario()           #Llama a la fx de DAO que verifica registros
        for x in respuesta:
            Registros.append([x[2]])

        #Nombre
        while True:
            try:
                system("cls")
                print(colored("===MENU REGISTRO===","light_blue"))
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                nom=str(input("Ingrese el Nombre del Usuario: "))
                if len(nom.strip())>2 and len(nom.strip())<=20:
                    break
                elif (len(nom.strip())==0):
                    self.__retornarMenu()
                else:
                    system("cls")
                    print("El Nombre debe tener entre 2 a 20 caracteres")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")
                
        #RUT (Actualizado 05.11)
        while True:
            try:
                system("cls")
                print(colored("===MENU REGISTRO===","light_blue"))
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                rut=str(input("Ingrese el Rut del Usuario: "))
                
                #Verificamos que este dato no este registrado 
                if any(rut == x[2] for x in respuesta):
                    system("cls")
                    print(colored("El Rut ya Existe...","yellow"))
                    system("pause")
                    self.__retornarMenu()
                elif (len(rut.strip())==0):
                    self.__retornarMenu()
                elif (len(rut.strip())>9 and len(rut.strip())<=10) and rut[-2] == '-': #Valiodamos que el rut tenga los caracteres correspondientes y ademas le decimos que valide el digito verificador (guion) en la segunda psoicion de atras hacia adelante
                    break
                else:
                    system("cls")
                    print("El Rut debe tener entre 11 a 12 caracteres el el guion verificador")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")        
                
        while True:
            try:
                system("cls")
                print(colored("===MENU REGISTRO===","light_blue"))
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                contraseña=str(input("Ingrese su contraseña: "))
                if (len(contraseña.strip())==0):
                    self.__retornarMenu()
                else:
                    system("cls")
                    print(colored("Ingrese Nuevamente su Contraseña...","yellow"))
                    system("pause")
                    system("cls")
                    print(colored("===MENU REGISTRO (Validacion Contraseña)===","light_blue"))
                    print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                    valContraseña=str(input("Ingrese su contraseña: "))
                    if (len(valContraseña.strip())==0):
                        self.__retornarMenu()
                    elif valContraseña==contraseña:
                        break
                    else:
                        system("cls")
                        print("Las contraseñas no coinciden...")
                        system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")

        #Tipo de Usuario
        while True:
            try:
                system("cls")
                print(colored("===MENU REGISTRO===","light_blue"))
                print(colored("Seleccion de Privilegios","light_blue"))
                print(colored("1.", "light_blue") + "Administrador")
                print(colored("2.", "light_green") + "Gestor")
                priviUser = int(input("Seleccione La Opcion Correspondiente: "))
                if priviUser == 1 or priviUser == 2:
                    break
                else:
                    system("cls")
                    print("Opcion Incorrecta")
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")

        clave_fernet = Fernet.generate_key()
        clave_fernet = "FL-m2D5DcrRkcWJY4wjd9I7KFMFL997AdGVz4SGZ-fc="
        f = Fernet(clave_fernet)
        contraseña_encriptada = f.encrypt(contraseña.encode())

        system("cls")
        print(colored("Datos Asignados Correctamente!!","light_green"))
        system("pause")
                
        self.__user.setNombre(nom)
        self.__user.setRut(rut)
        self.__user.setContraseña(contraseña_encriptada)
        self.__user.setTipo(priviUser)
        self.__d.regist(self.__user)


    def __suprimirUsuario(self):
        Registros = []                                  #Creamos Una variable(lista) para almacenar los datos de la bd y poder mostrarlos

        #Esta funcion (Tomada de Mostar Registros) nos permite validar si datos unicos (como RUT,) ya fueron Ingresados
        respuesta= self.__d.comprobarUsuario()           #Llama a la fx de DAO que verifica registros
        for x in respuesta:
            Registros.append([x[2]])

        #RUT (Actualizado 05.11)
        while True:
            try:
                system("cls")
                print(colored("===MENU SUPRIMIR USUARIO===","light_blue"))
                print(colored("Para Volver al Menu Presione ENTER (Sin Ingresar Datos)","grey"))
                rut=str(input("Ingrese el Rut del Usuario: "))
                
                #Verificamos que este dato no este registrado 
                if any(rut == x[2] for x in respuesta):
                    system("cls")
                    print(colored("Cargarndo Eliminacion...","yellow"))
                    system("pause")
                    break
                elif (len(rut.strip())==0):
                    self.__retornarMenu()
                else:
                    system("cls")
                    print(colored("El Rut No ha sido Encontrado...","yellow"))
                    system("pause")
            except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e}","red"))
                system("pause")
        
        system("cls")
        print(colored("Datos Eliminados Correctamente!!","light_green"))
        system("pause")

        self.__user.setRut(rut)
        self.__d.deleteRegist(self.__user)
    
#||------------------------------------------------------------------------------------------------------------------------||

    def __retornarMenu(self):
            self.user = self.__d.login(rutAcces, conAcces)
            try:
                if self.user.getTipo() == 1:
                    print(colored("--- Retornando a menu ---","light_green"))
                    self.__menuAdmin()
                elif self.user.getTipo() == 2:
                    print(colored("--- Retornando a menu ---","light_green"))
                    self.__menuAyuda()
            except Exception as e:
                    system("cls")
                    print(colored(f"Detalles del error: {e}","red"))
                    system("pause") 
    
#||------------------------------------------------------------------------------------------------------------------------||
    def __salir(self):
        system("cls")
        print(colored("Esta Seguro de Finalizar la APP?","light_yellow"))
        print(colored("1.","light_yellow") + colored(" Si", "grey"))
        print(colored("2.","light_yellow") + colored(" No (Presionar Cualquier Tecla)","grey"))
        opc=int(input(colored("Seleccione Opcion: ","light_yellow")))
        if opc == 1:
            system("cls")
            print(colored("Se a finalizado el programa... \n\n","red"))
            system("pause")
            os._exit(1)
        else:
            self.menuInicial
