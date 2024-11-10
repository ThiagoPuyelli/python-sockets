import socket

#Set up the client 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 12345
client_socket.connect(('localhost', PORT)) # connect to the server

#Send a SQL query to the server 
query = input("Enter SQL query to send to server: ")
client_socket.send(query.encode())

#Receive and print the response from the server
response  = client_socket.recv(1024).decode()
print(f"Received from server: {response}")

# Close the client socket.
client_socket.close()