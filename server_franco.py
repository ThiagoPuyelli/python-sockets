import socket
import json
from modelo.mongo.ConexionMongo import ConexionMongo
from modelo.sql.ConexionSQL import ConexionSQL


def start_server():
    # Configuración del servidor
    server_host = '127.0.0.1'  # IP local
    server_port = 1234       # Puerto del servidor
    buffer_size = 1024         # Tamaño del buffer para recibir datos

    # Creación del socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(1)    # Escucha para 1 conexión (ajustable según necesidades)

    print(f"Servidor escuchando en {server_host}:{server_port}")

    # Acepta una conexión entrante
    client_socket, client_address = server_socket.accept()
    print(f"Conexión aceptada desde {client_address}")
    motor = None
    bd = None

    try:
        while True:
            # Recibe datos del cliente
            message = client_socket.recv(buffer_size).decode('utf-8')
            if not message:
                print("Conexión cerrada por el cliente")
                break

             # Intenta interpretar el mensaje como JSON
            try:
                data = json.loads(message)
                print(f"Mensaje JSON recibido: {data}")

                # Actúa en función de los atributos del JSON
                if 'action' in data:
                    if data['action'] == 'motor':
                        print(data)
                        motor = seleccionarMotor(data["value"])
                        print("PEPEPEPEPEPEPEPE")
                        print(motor)
                        motor.conectar()
                        response = {"response": {
                            "type": "bds",
                            "value": motor.bdRegistradas() # motor.getBds()
                        }}
                    elif data['action'] == 'bds':
                        elegido = motor.seleccionarBD(data["value"])
                        response = {"response": {
                            "type": "consulta" if elegido else "bds",
                            "value": motor.listaDeTablas() if elegido else "Base de datos invalida"
                        }}
                    elif data['action'] == 'consulta':
                        consulta = motor.ejecutarConsulta(data["value"])
                        response = {"response": {
                            "type": "consulta",
                            "value": consulta
                        }}
                    else:
                        response = {"error": "Acción no reconocida"}
                else:
                    response = {"error": "Falta el atributo 'action' en el JSON"}
                
                #response = f"Servidor recibió: {response}"
                print("sracatunga response!!!")
                print(response)
                client_socket.send(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError:
                response = {"error": "Formato JSON inválido"}
                #response = f"Servidor recibió: {response}"
                client_socket.send(json.dumps(response).encode('utf-8'))
            
    except Exception as e:
        print("Error durante la comunicación:", e)
    finally:
        client_socket.close()
        server_socket.close()
        print("Conexión cerrada")

def seleccionarMotor (motor):
    print("Motor value: " , motor)
    if (motor == "MONGO"):
        return ConexionMongo()
    
    if (motor.lower() == "mysql"):
        print("saracatunga in")
        return ConexionSQL()

if __name__ == "__main__":
    start_server()

