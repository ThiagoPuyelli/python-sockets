from modelo import IConexion
import _mysql_connector

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

   def bdRegistradas(self) -> str:
        """Lista las bases de datos registradas en un determinado motor."""
        return "Lista de bases de datos."

   def listaDeTablas(self) -> str:
        """Lista las tablas de una determinada BD."""
        return "Lista de tablas."

   def seleccionarBD(self, bd: str) -> bool:
        """Permite seleccionar la base de datos de un determinado motor."""
        print(f"Base de datos '{bd}' seleccionada.")
        return True
