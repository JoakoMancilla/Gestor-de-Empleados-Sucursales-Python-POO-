import pymysql
from os import system
from termcolor import colored
from cryptography.fernet import Fernet
from usuarios import usuarios

class DAO():
    def __init__(self):
        pass
    
    def __conectar(self):
            self.con = pymysql.connect(
                host = "localhost",
                user = "root",
                password = "",
                db = "proyectopoo"        
            )
            self.cursor = self.con.cursor()
            
    def __desconectar(self):
            
            self.con.close()
            
    def comprobarBD(self):
        system("cls")
        self.__conectar()
        print(colored("Conexion establecida corectamente!!!", "green"))
        system("pause")
        self.__desconectar()
#||------------------------------------------------------------------------------------------------------------------------||

    def agregarEmpleado(self, emple):
        try:
            sql = "insert into empleados (rut_emp, nom_emp, app_emp, apm_emp, cor_emp, tel_emp, ant_emp, sal_emp, fec_emp) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (emple.getRut(), emple.getNombre(), emple.getApellidoP(), emple.getApellidoM(), emple.getCorreo(), emple.getTelefono(),emple.getAntiguedad(), emple.getSalario(), emple.getFecha())
            self.__conectar()
            self.cursor.execute(sql, val)
            self.con.commit()
            self.__desconectar()
        except Exception as e:
            system("cls")
            print("Error DAO: Agregar Empleado")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

    def obtenerEmpleado(self):
        try:
            sql= "Select * from empleados"
            self.__conectar()
            self.cursor.execute(sql)
            rs =self.cursor.fetchall()
            self.__desconectar()
            return rs
        except Exception as e:
            system("cls")
            print("Error DAO: Obtener Empleado")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

    #Actualizado (20.11)
    def updateEmpleado(self,id,dato,newRut,newNom,newApep,newApem,newCorreo,newTel,newSal,newContra,newAntig):
        try:
            sql= ""
            if dato == 1:
                sql = "update empleados set rut_emp=%s, nom_emp=%s, app_emp=%s, apm_emp=%s, where id_emp=%s"
                self.__conectar()
                val = (newRut,newNom,newApep,newApem,id)
            elif dato == 2:
                sql = "update empleados set cor_emp=%s, tel_emp=%s where id_emp=%s"
                self.__conectar()
                val = (newCorreo,newTel,id)
            elif dato == 3:
                sql = "update empleados set sal_emp=%s where id_emp=%s"
                self.__conectar()
                val = (newSal,id)
            elif dato == 4:
                sql = "update empleados set ant_emp=%s, fec_emp=%s where id_emp=%s"
                self.__conectar()
                val = (newContra,newAntig,id)
            elif dato == 5:
                sql = "update empleados set rut_emp=%s, nom_emp=%s, app_emp=%s, apm_emp=%s, cor_emp=%s, tel_emp=%s, sal_emp=%s, fec_emp=%s, ant_emp=%s where id_emp=%s"
                self.__conectar()
                val = (newRut,newNom,newApep,newApem,newCorreo,newTel,newSal,newContra,newAntig,id)

            self.cursor.execute(sql,val)
            self.con.commit()
            self.__desconectar()
        except Exception as e:
            system("cls")
            print("Error DAO: Update Empleado")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

    def deleteEmpleado(self,id):
        try:
            sql= "delete from empleados where id_emp=%s"
            self.__conectar()
            val= (id)
            self.cursor.execute(sql, val)
            self.con.commit()
            self.__desconectar()
        except Exception as e:
            system("cls")
            print("Error DAO: Eliminar Empleado")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

#||------------------------------------------------------------------------------------------------------------------------||

    def agregarSucursal(self, sucur):
        try:
            sql = "insert into sucursales (nom_suc,dirc_suc,fecha_suc) values (%s, %s, %s)"
            val = (sucur.getNombre(), sucur.getDireccion(), sucur.getFecha())
            self.__conectar()
            self.cursor.execute(sql, val)
            self.con.commit()
            self.__desconectar()
        except Exception as e:
            system("cls")
            print("Error DAO: Agregar Sucursal")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

    def obtenerSucursal(self):
        try:
            sql= "select * from sucursales"
            self.__conectar()
            self.cursor.execute(sql)
            rs =self.cursor.fetchall()
            self.__desconectar()
            return rs
        except Exception as e:
            system("cls")
            print("Error DAO: Obtener Sucursal")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

    #Actualizado (20.11)
    def updateSucursal(self,id,dato,newNom,newDir,newFec):
        try:
            sql= ""
            if dato == 1:
                sql = "update sucursales set nom_suc=%s where id_suc=%s"
                self.__conectar()
                val = (newNom,id)
            elif dato == 2:
                sql = "update sucursales set dirc_suc=%s where id_suc=%s"
                self.__conectar()
                val = (newDir,id)
            elif dato == 3:
                sql = "update sucursales set fecha_suc=%s where id_suc=%s"
                self.__conectar()
                val = (newFec,id)
            elif dato == 4:
                sql = "update sucursales set nom_suc=%s, dirc_suc=%s, fecha_suc=%s where id_suc=%s"
                self.__conectar()
                val = (newNom,newDir,newFec,id)

            self.cursor.execute(sql,val)
            self.con.commit()
            self.__desconectar()
        except Exception as e:
            system("cls")
            print("Error DAO: Update Sucursal")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

    def deleteSucursal(self,id):
        try:
            sql= "delete from sucursales where id_suc=%s"
            self.__conectar()
            val= (id)
            self.cursor.execute(sql, val)
            self.con.commit()
            self.__desconectar()
        except Exception as e:
            system("cls")
            print("Error DAO: Eliminar sucursal")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

#||------------------------------------------------------------------------------------------------------------------------||

    def agregarAsignaciones(self, asig):
        try:
            sql = "insert into asignaciones (id_emp, id_suc) values (%s, %s)"
            val = (asig.empleado.getID(), asig.sucursal.getID())
            self.__conectar()
            self.cursor.execute(sql, val)
            self.con.commit()
            self.__desconectar()
        except Exception as e:
            system("cls")
            print("Error DAO: Agregar Asignacion")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")
    
    def obtenerAsignaciones(self):
        try:
            sql = "select asig.id_asi, asig.id_emp, emple.nom_emp, asig.id_suc, sucur.nom_suc from asignaciones asig inner join empleados emple on asig.id_emp=emple.id_emp inner join sucursales sucur on asig.id_suc=sucur.id_suc order by id_asi asc" #(ACTUALIZADO 20.11)
            self.__conectar()
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            self.__desconectar()
            return rs
        except Exception as e:
            system("cls")
            print("Error DAO: Obtener Asignacion")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

    #ACTUALIZADO 20.11
    def updateAsignaciones(self, id, idnew):
        try:
            sql= "update asignaciones set id_suc=%s where id_asi=%s"
            self.__conectar()
            val= (idnew,id)
            self.cursor.execute(sql, val)
            self.con.commit()
            self.__desconectar()
        except Exception as e:
            system("cls")
            print("Error DAO: reasignaciones")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")
            
#||------------------------------------------------------------------------------------------------------------------------||

    def login(self, rutAcces, conAcces):
        try:
            self.__conectar()
            sql = "select * from usuarios where rut_usr=%s"
            val = (rutAcces)
            self.cursor.execute(sql, val)
            rs = self.cursor.fetchone()
            self.__desconectar()
            
            if rs is None:
                return None
            else:
                
                #--- OBTENER CONTRASEÑA ENCRIPTADA EN LA BD ---
                #--- [3] ES LA POSICION DE LA CONTRASEÑA EN LA TABLA ---
                contraseña_encriptada = rs[3]
            
                #--- DESENCRIPTAR CONTRASEÑA ---
                #--- SE DEBE USAR LAS MISMA CLAVE FERNET CON LA CUAL SE ENCRIPTÓ ---
                clave_fernet = "FL-m2D5DcrRkcWJY4wjd9I7KFMFL997AdGVz4SGZ-fc="
                f = Fernet(clave_fernet)
                contraseña_desencriptada = f.decrypt(contraseña_encriptada).decode()
        
        
                #print(f"CON : { con }")
                #print(f"DES : { contraseña_desencriptada }")
                #system("pause")
        
        
                if conAcces == contraseña_desencriptada:
                    usu = usuarios()
                    usu.setNombre(rs[1].upper())
                    usu.setRut(rs[2])
                    usu.setContraseña(contraseña_encriptada)
                    usu.setTipo(rs[4])
                    
                    return usu
                else:
                    return None
        except Exception as e:
                system("cls")
                print(colored(f"Detalles del error: {e} (DAO)","red"))
                system("pause")

#||------------------------------------------------------------------------------------------------------------------------||

    def comprobarUsuario(self):
        try:
            sql= "Select * from usuarios"
            self.__conectar()
            self.cursor.execute(sql)
            rs =self.cursor.fetchall()
            self.__desconectar()
            return rs
        except Exception as e:
            system("cls")
            print("Error DAO: Obtener usuarios")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

    def regist(self,user):
        try:
            sql = "insert into usuarios (nom_usr, rut_usr, con_usr, id_tip) values (%s, %s, %s, %s)"
            val = (user.getNombre(), user.getRut(), user.getContraseña(),user.getTipo())
            self.__conectar()
            self.cursor.execute(sql, val)
            self.con.commit()
            self.__desconectar()
        except Exception as e:
            system("cls")
            print("Error DAO: Registrar Usuario")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")

    def deleteRegist(self, user):
        try:
            sql = "delete from usuarios where rut_usr = %s"
            val = (user.getRut())
            self.__conectar()
            self.cursor.execute(sql, val)
            self.con.commit()
            self.__desconectar()
        except Exception as e:
            system("cls")
            print("Error DAO: Eliminar Usuario")
            print(colored(f"Detalles del error: {e}","red"))
            system("pause")
            
#||------------------------------------------------------------------------------------------------------------------------||

