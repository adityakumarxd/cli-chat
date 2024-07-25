import socket
import threading
import requests

PORT = 8008 
CREDENTIALS_FILE = "credentials.txt"

clients = {}
clients_lock = threading.Lock()

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

def load_credentials():
    credentials = {}
    try:
        with open(CREDENTIALS_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split(':')
                credentials[username] = password
    except FileNotFoundError:
        print(f"Credentials file '{CREDENTIALS_FILE}' not found.")
    return credentials

def authenticate(username, password):
    credentials = load_credentials()
    return credentials.get(username) == password

def format_message(username, message):
    return f"{CYAN}{BOLD}[{username}]{RESET}: {MAGENTA}{message}{RESET}"

def get_user_count():
    with clients_lock:
        return len(clients)

def handle_client(conn, addr):
    authenticated = False
    username = None

    try:
        conn.sendall(b"Username: ")
        username = conn.recv(1024).decode().strip()

        conn.sendall(b"Password: ")
        password = conn.recv(1024).decode().strip()

        with clients_lock:
            if username in clients.values():
                conn.sendall(b"Username is already connected to the chat. Connection terminated.\n")
                return  

        if not authenticate(username, password):
            conn.sendall(b"Invalid username or password. Connection terminated.\n")
            return 

        authenticated = True
        with clients_lock:
            clients[conn] = username
        user_count = get_user_count()
        conn.sendall(f"{RED}{BOLD}Welcome, {username}! There are {user_count} users connected.{RESET}\n".encode())
        conn.sendall(f"{CYAN}{BOLD}{username}{RESET}> ".encode())  

        print(f"{CYAN}{BOLD}{username} has joined the chat.{RESET}")
        broadcast_message(format_message(username, "has joined the chat."), conn, prompt=False)

        while True:
            try:
                message = conn.recv(1024).decode().strip()
                if not message:
                    break
                formatted_message = format_message(username, message)
                print(formatted_message)
                broadcast_message(formatted_message, conn, prompt=True)   
            except ConnectionResetError:
                print(f"{RED}Connection reset error for user {username}.{RESET}")
                break
            except Exception as e:
                print(f"{RED}Unexpected error: {e}{RESET}")
                break

    finally:
        if authenticated:
            with clients_lock:
                if conn in clients:
                    del clients[conn]
            user_count = get_user_count()
            print(f"{RED}{BOLD}{username} has left the chat.{RESET}")
            broadcast_message(format_message(username, "has left the chat."), conn, prompt=False)
            broadcast_message(f"{RED}{BOLD}{username} has left the chat. There are now {user_count} users connected.{RESET}", None, prompt=False)
        conn.close()

def broadcast_message(message, sender, prompt):
    with clients_lock:
        for conn in clients:
            if conn != sender:
                try:
                    conn.sendall((message + '\n').encode())
                    if prompt:
                        conn.sendall(f"{CYAN}{BOLD}{clients[conn]}{RESET}> ".encode()) 
                except BrokenPipeError:
                    print(f"{RED}Broken pipe error. Client might have disconnected.{RESET}")
                except Exception as e:
                    print(f"{RED}Error sending message to client: {e}{RESET}")

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status() 
        ip = response.json().get('ip', 'Unknown IP')
    except requests.RequestException as e:
        print(f"{RED}Error fetching public IP: {e}{RESET}")
        ip = 'Unknown IP'
    return ip

def main():
    public_ip = get_public_ip()
    print(f"Server running on public IP {CYAN}{BOLD}{public_ip}{RESET} and port {CYAN}{BOLD}{PORT}{RESET}\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("0.0.0.0", PORT))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
