# from modelo.sql.ConexionSQL import ConexionSQL
from modelo.postgres.ConexionPostgres import ConexionPostgres


conexion = ConexionPostgres()

conexion.conectar()
print(conexion.bdRegistradas())

if conexion.seleccionarBD("deck"):
    print("Conectado a la base de datos 'deck'")
else:
    print("Error al conectar con la base de datos.")
    
print("Se listan las tablas")
print(conexion.listaDeTablas())

response = conexion.ejecutarConsulta(input("Ingrese la query: "))
print(response)  # This will print the query result (list of tuples)