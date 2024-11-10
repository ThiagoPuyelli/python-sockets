import socket
import json

def start_client():
    # Configuración del cliente
    server_host = '127.0.0.1'  # IP del servidor (debe coincidir con el servidor)
    server_port = 12345        # Puerto del servidor (debe coincidir con el servidor)
    buffer_size = 1024         # Tamaño del buffer para recibir datos

    # Creación del socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    print("Conectado al servidor")
    mode = "motor"
    value = ""
    message = ""

    try:
        while True:
            # Leer mensaje del usuario
            if (mode == "motor"):
                print("Elige el motor a utilizar")
                print("1. MongoDB")
                print("2. PostgreSQL")
                message = input("Ingrese el motor (o exit si quiere salir): ")
            if (mode == "bds"):
                print("Elige la base de datos")
                print()

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
            mode = jsonRes["type"]
            value = jsonRes["value"]

            print(f"Respuesta del servidor: {response}")
    except Exception as e:
        print("Error durante la comunicación:", e)
    finally:
        client_socket.close()
        print("Conexión cerrada")

if __name__ == "__main__":
    start_client()