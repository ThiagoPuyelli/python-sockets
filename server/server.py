import socket
import mysql.connector

#setting up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a new socket
PORT = 12345
server_socket.bind(('localhost', PORT))  # Bind to localhost on port 12345
server_socket.listen(1) # Listen for incoming connections

print("Server is listening for connections...")


# MySQL database connection
db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin',
    'database': 'flashcards'
}

# Connect to DB
try:
    db_connection = mysql.connector.connect(**db_config)
    db_cursor = db_connection.cursor()
    print("Connected to the database!!")

except mysql.connector.Error as err:
    print(f"Error connecting to database: {err}")
    exit(1)


while True:
    #Accept client connection
    client_socket, client_address = server_socket.accept()
    print(f"Connected to client at {client_address}")

    try:
        # Receive the SQL query from the client
        query = client_socket.recv(1024).decode()
        print(f"Received query from client: {query}")

        #Execute the query
        db_cursor.execute(query)
        result = db_cursor.fetchall() # Fetch all results
        
        # Send results back to the client
        response = str(result) # convert the result to a string.
        client_socket.send(response.encode())
    except Exception as e:
            print(f"Error executing query: {e}")
            client_socket.send(f"Error: {str(e)}".encode())
    finally:
        # Close the client socket
        client_socket.close()