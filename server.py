import socket
import threading

clients = {}
message_history = []


# Function to broadcast a message to all clients
# message is added to message history
def broadcast_message(message, sender=None):
    message_history.append(message)
    
    for client_socket in clients.keys():
        if client_socket != sender:
            try:
                client_socket.send(message.encode())
            except:
                del clients[client_socket]


#handle client, store username and send message history
# if client disconnects remove them
# broadcast message to all clients
def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode()
        clients[client_socket] = username
        print(f"{username} connected.")
        
        for message in message_history:
            client_socket.send(message.encode())

        while True:
            message = client_socket.recv(1024).decode()
            if message.lower() == 'end':
                print(f"{username} disconnected.")
                del clients[client_socket]
                client_socket.close()
                break
            broadcast_message(message)
    except:
        if client_socket in clients:
            del clients[client_socket]
        client_socket.close()


# Function to start the server bind to IP address and port
# Listen for incoming connections 
# start a thread for each client
def start_server():
    ip_address = input("Enter IP address (press Enter for localhost): ") or '127.0.0.1'
    port = int(input("Enter port number (press Enter for default port): ") or 12345)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((ip_address, port))
        print("Server started. Waiting for connections...")
        server_socket.listen()

        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()


# Run the server
if __name__ == "__main__":
    start_server()
