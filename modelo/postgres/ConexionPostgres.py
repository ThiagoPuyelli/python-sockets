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
        try:
            if self.conexion is None or self.cursor is None:
                raise Exception("La conexión no está establecida. Llame al método 'conectar()' primero.")
            
            self.cursor.execute(consulta)
            # hago un fetch de los resultados si es un SELECT.
            if consulta.strip().lower().startswith("select"):
                rows = self.cursor.fetchall()
                # formateo los resultados.
                response = ",".join([str(row) for row in rows])
                return response
            
            self.conexion.commit()
            return "consulta ejecutada correctamente!"
        
        except psycopg2.Error as err:
            print(f"Error al ejecutar la consulta: {err}")
            return f"Error al ejecutar la consulta: {err}"
        
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
        
        finally:
            self.conectar()
            
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
        try:
            if self.conexion is None or self.cursor is None:
                raise Exception("La conexión no está establecida. Llame al método 'conectar()' primero.")
            # obtengo las tablas del catalogo en el cursor.
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            
            tables = [row[0] for row in self.cursor.fetchall()]
            
            # Para cada tabla, obtengo sus columnas.
            tables_with_columns = []
            for table in tables:
            # Obtengo las columnas de la tabla.
                self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}';")
                columns = [row[0] for row in self.cursor.fetchall()]
            
            # Agrego el nombre de la tabla con los atributos entre paréntesis.
            table_str = f"{table} ({', '.join(columns)})"
            tables_with_columns.append(table_str)
            return tables_with_columns if tables else []
        
        except Exception as err:
            print(f"Error al listar las tablas: {err}")
            return []
    

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
