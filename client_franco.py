import socket
import json

def start_client():
    # Configuración del cliente
    server_host = '127.0.0.1'  # IP del servidor (debe coincidir con el servidor)
    server_port = 1234       # Puerto del servidor (debe coincidir con el servidor)
    buffer_size = 1024         # Tamaño del buffer para recibir datos

    # Creación del socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    print("Conectado al servidor")
    mode = "motor"
    value = ""
    message = ""
    tablas = ""
    bdElegida = ""

    try:
        while True:
            # Leer mensaje del usuario
            if (mode == "motor"):
                print("Elige el motor a utilizar")
                print("1. MongoDB")
                print("2. PostgreSQL")
                print("3. MySQL")
                message = input("Ingrese el motor (o exit si quiere salir): ")
                if message.lower() == 'exit':
                  print("Cerrando la conexión...")
                  break
                bds = ["MONGO", "POSTGRE", "MYSQL"]
                if (message.isdigit() is False or int(message) > len(bds) or int(message) < 1):
                    print("El motor no es válido")
                    continue
                message = bds[int(message) - 1]
                bdElegida = message
            if (mode == "bds"):
                print("Elige la base de datos")
                i = 1
                for x in value:
                    print(str(i) + ". " + x)
                    i += 1
                message = input("Ingrese la base de datos (o exit si quiere salir): ")
                if message.lower() == 'exit':
                  print("Cerrando la conexión...")
                  break
                if (message.isdigit() is False or int(message) > len(value) or int(message) < 1):
                    print("La base de datos no es válida")
                    continue
                message = value[int(message) - 1]
            if (mode == "consulta"):
                print("Lista de tablas")
                i = 1
                for x in tablas:
                    print(str(i) + ". " + x)
                    i += 1
                print("Puede hacer una consulta")
                message = input("Ingrese la consulta (o exit si quiere salir): ")
                if message.lower() == 'exit':
                  print("Cerrando la conexión...")
                  break

            

            # Envía el mensaje al servidor
            message = {
                "action": mode,
                "value": message
            }
            client_socket.send(json.dumps(message).encode('utf-8'))

            # Recibe la respuesta del servidor
            response = client_socket.recv(buffer_size).decode('utf-8')
            jsonRes = json.loads(response)["response"]
            if (mode == "bds" and jsonRes["type"] == "consulta"):
                tablas = jsonRes["value"]
            elif (mode == "consulta"):
                if (bdElegida == "MONGO"):
                    print("Resultado: " + json.dumps(jsonRes["value"]).replace("\\", ""))
                else:
                    # print("Resultado: " + jsonRes["value"])
                    print("Resultado: " + response)
            mode = jsonRes["type"]
            value = jsonRes["value"]

    except Exception as e:
        print("Error durante la comunicación:", e)
    finally:
        client_socket.close()
        print("Conexión cerrada")

if __name__ == "__main__":
    start_client()