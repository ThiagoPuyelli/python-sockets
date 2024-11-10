from pymongo import MongoClient
from modelo.IConexion import IConexion
import json

class ConexionMongo(IConexion):

   def __init__(self):
        self.conexion = None
        self.bd = None
        self.bdName = ""
   
   def conectar(self):
     try:
            self.conexion = MongoClient("mongodb://localhost:27017/")
            print("Conectado al motor de la base de datos")
     
     except Exception as e:
            print(f"Error al conectar con el motor de la base de datos: {e}")
            

   def desconectar(self):
        """Cierra la conexión con la base de datos"""
        print("Desconectado de la base de datos.")

   def ejecutarConsulta(self, consulta: str) -> str:
        """Ejecuta la consulta que llega por parametro"""
        db = self.conexion[self.bdName]
        resultado = eval(consulta)
        resultado = list(resultado) if hasattr(resultado, '__iter__') else [resultado]
        res = json.dumps(resultado, default=str)
        return res

   def bdRegistradas(self) -> list:
        """Lista las bases de datos registradas en un determinado motor."""
        return self.conexion.list_database_names()

   def listaDeTablas(self) -> list:
        """Lista las tablas de una determinada BD."""
        return self.bd.list_collection_names()

   def seleccionarBD(self, bd: str) -> bool:
        """Permite seleccionar la base de datos de un determinado motor."""
        self.bd = self.conexion.get_database(bd)
        self.bdName = bd
        return True
