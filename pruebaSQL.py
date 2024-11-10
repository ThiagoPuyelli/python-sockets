from modelo.sql.ConexionSQL import ConexionSQL


conexion = ConexionSQL()

conexion.conectar()
print(conexion.bdRegistradas())