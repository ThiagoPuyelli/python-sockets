# from modelo.sql.ConexionSQL import ConexionSQL
from modelo.postgres.ConexionPostgres import ConexionPostgres


conexion = ConexionPostgres()

conexion.conectar()
print(conexion.bdRegistradas())

# if conexion.seleccionarBD("flashcards"):
#     print("Conectado a la base de datos 'flashcards'")
# else:
#     print("Error al conectar con la base de datos.")
    
# print("Se listan las tablas")
# print(conexion.listaDeTablas())

# result = conexion.ejecutarConsulta(input("Ingrese la query: "))
# print(result)  # This will print the query result (list of tuples)