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
        self.bdName = None
   
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
        try:
            if self.conexion is None or self.cursor is None:
                raise Exception("La conexión no está establecida. Llame al método 'conectar()' primero.")
            self.cursor.execute(consulta)
            if consulta.strip().upper().startswith("SELECT"):
                results = self.cursor.fetchall()  # Fetch all results of the SELECT query
                return results if results else "No se encontraron resultados."
            self.conexion.commit()
            return f"Consulta '{consulta}' ejecutada con éxito."
        except sql.Error as err:
            print(f"Error al ejecutar la consulta: {err}")
            return f"Error al ejecutar la consulta: {err}"
        
        finally:
            self.conectar()
            self.seleccionarBD(self.bdName)
        	
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
        
   def listaDeTablas(self) -> list:
        """Lista las tablas de una determinada BD."""
        try:
            if self.conexion is None or self.cursor is None:
                raise Exception("La conexión no está establecida. Llame al método 'conectar()' primero.")
            
            self.cursor.execute("SHOW TABLES")
            tables = [table[0] for table in self.cursor.fetchall()]
            # Para cada tabla, obtengo sus columnas.
            tables_with_columns = []
            for table in tables:
                # Obtengo las columnas de la tabla.
                self.cursor.execute(f"SHOW COLUMNS FROM {table}")
                columns = [row[0] for row in self.cursor.fetchall()]
            
                # Agrego el nombre de la tabla con los atributos entre paréntesis.
                table_str = f"{table} ({', '.join(columns)})"
                tables_with_columns.append(table_str)

            return tables_with_columns if tables_with_columns else []
            
        except sql.Error as err:
            print(f"Error al listar las tablas: {err}")
            return []
            
   def seleccionarBD(self, bd: str) -> bool:
       """Permite seleccionar la base de datos de un determinado motor."""
       try:
           if self.conexion is None or self.cursor is None:
               raise Exception("La conexión no está establecida. Llame al método 'conectar()' primero.")
           self.cursor.execute(f"USE {bd}")
           self.conexion.commit()  # Commit the transaction
           print(f"Base de datos '{bd}' seleccionada.")
           self.bdName = bd
           return True
       except sql.Error as err:
           print(f"Error al seleccionar la base de datos '{bd}': {err}")
           return False
