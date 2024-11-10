from modelo.IConexion import IConexion
import psycopg2
class ConexionPostgres(IConexion):
    # Conexion postgres.
    db_config = {
      'host': 'localhost',
      'user': 'postgres',
      'password': 'admin',
       'dbname': 'postgres'
   }
    
    def __init__(self):
        self.conexion = None
        self.cursor = None
        
    def conectar(self):
        try:
            self.conexion = psycopg2.connect(**self.db_config)
            self.cursor = self.conexion.cursor()
            print("Conectado al motor de la base de datos")
        
        except psycopg2.Error as err:
            print(f"Error al conectar con el motor de la base de datos: {err}")
    

    def desconectar(self):
        """Cierra la conexión con la base de datos"""
        pass

    def ejecutarConsulta(self, consulta: str) -> str:
        """Ejecuta la consulta que llega por parametro"""
        pass

    def bdRegistradas(self) -> list:
        """Lista las bases de datos registradas en un determinado motor."""
        try:
            if self.conexion is None or self.cursor is None:
                raise Exception("La conexión no está establecida. Llame al método 'conectar()' primero.")
            
            self.cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;") # traemos del catalogos todas las bd.
            databases = [db[0] for db in self.cursor.fetchall()] # guardamos los nombres de las bd en una variable.
            
            return databases if databases else []
        
        except Exception as err:
            print(f"Error al listar las tablas: {err}")
            return []

    def listaDeTablas(self) -> list:
        """Lista las tablas de una determinada BD."""
        pass
    

    def seleccionarBD(self, bd: str) -> bool:
        """Permite seleccionar la base de datos de un determinado motor."""
        try:
            if self.conexion:
                self.cursor.close()
                self.conexion.close()
            #actualizo la bd.
            self.db_config['dbname'] = bd
            
            self.conectar()
            print(f"Base de datos '{bd}' seleccionada.")
            return True
        
        except psycopg2.OperationalError as err:
            print(f"Error al seleccionar la base de datos '{bd}': {err}")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False            