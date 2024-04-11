import socket
import threading
import tkinter as tk
import tkinter.font as tkFont

message_history = []

#receive messages from server
def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message + '\n')
                text_area.config(state=tk.DISABLED)
                text_area.yview(tk.END)  # Auto-scrolling
                message_history.append(message + '\n')
            else:
                raise Exception("Server disconnected")
        except Exception as e:
            print(e)  
            client_socket.close()
            break

#send message to server
def send_message(client_socket, message_entry, username):
    message = message_entry.get()
    if message:
        if message.lower() == 'end':
            client_socket.close()
        else:
            client_socket.send(f"{username}: {message}".encode())
            message_entry.delete(0, tk.END)



# start client connection ask for ip and port and username
# start tkinter window

def start_client():
    server_ip = input("Enter server's IP address: ")
    server_port = int(input("Enter server's port number: "))
    username = input("Enter your username: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
        print("Connected to server.")

        client_socket.send(username.encode())

        root = tk.Tk()
        root.title("Chat Room")
        root.minsize(width=800, height=600)  

        textFont = tkFont.Font(family="Helvetica", size=14)  
        entryFont = tkFont.Font(family="Helvetica", size=12)  

        text_area = tk.Text(root, height=20, width=50, font=textFont)
        text_area.config(state=tk.DISABLED)
        text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)  
        
        message_entry = tk.Entry(root, width=50, font=entryFont)
        message_entry.pack(padx=10, pady=10, expand=True, fill=tk.X)  
        message_entry.bind("<Return>", lambda event: send_message(client_socket, message_entry, username))  
              
        send_button = tk.Button(root, text="Send", command=lambda: send_message(client_socket, message_entry, username))
        send_button.pack(padx=10, pady=10)

        
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, text_area))
        receive_thread.daemon = True  
        receive_thread.start()

        def on_closing():
            """Handle window closing event."""
            try:
                client_socket.send("end".encode())
                client_socket.close()
            finally:
                root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        root.mainloop()

    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()


#start client
if __name__ == "__main__":
    start_client()
