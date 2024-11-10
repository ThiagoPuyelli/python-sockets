import mysql.connector as sql

from modelo.IConexion import IConexion

class ConexionSQL(IConexion):
   # Conexion mysql.
   db_config = {
      'host': 'localhost',
      'user': 'admin',
      'password': 'admin'
   }

   def __init__(self):
        self.conexion = None
        self.cursor = None
   
   def conectar(self):
     try:
            self.conexion = sql.connect(**self.db_config)
            self.cursor = self.conexion.cursor()
            print("Conectado al motor de la base de datos")
     
     except sql.Error as err:
            print(f"Error al conectar con el motor de la base de datos: {err}")


   def desconectar(self):
        """Cierra la conexión con la base de datos"""
        print("Desconectado de la base de datos.")

   def ejecutarConsulta(self, consulta: str) -> str:
        """Ejecuta la consulta que llega por parametro"""
        return f"Consulta '{consulta}' ejecutada."

   def bdRegistradas(self) -> list:
        """Lista las bases de datos registradas en un determinado motor."""
        
        
        try:
             if self.conexion is None or self.cursor is None:
                  raise Exception("La conexión no está establecida. Llame al método 'conectar()' primero.")
             
             self.cursor.execute("SHOW DATABASES") # ejecuto la query y traigo todas la bds.
             databases = self.cursor.fetchall()  # guardo las bds en una lista
             
             db_list = [db[0] for db in databases]  #guardo los nombres en el array.
             
             return db_list if db_list else []  
          
        except sql.Error as err:  
          return f"Error al listar las bases de datos: {err}"
        

   def listaDeTablas(self) -> str:
        """Lista las tablas de una determinada BD."""
        return "Lista de tablas."

   def seleccionarBD(self, bd: str) -> bool:
        """Permite seleccionar la base de datos de un determinado motor."""
        print(f"Base de datos '{bd}' seleccionada.")
        return True
