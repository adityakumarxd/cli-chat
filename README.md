# cli-chat-python 

This is a simple command-line based chat application written in Python. It allows users to connect using `netcat` and share encrypted & anonymous messages in a terminal environment. This is our playground.

## Setup

1. Clone this repository to your local machine.

2. Open the `main.py` file and locate the `PORT` constant at the top of the file:
```python
PORT = 8008  # Change this to your desired port
```

3. Create a credentials.txt file in the same directory as main.py with the following format:
  ```makefile
username1:password1
username2:password2
  ```
Each line represents a username and password pair.

4. Install the necessary dependencies by running the following command:
```bash
pip install requests
```
5. Run the server by executing the following command in your terminal:
```bash
python main.py
```

## Connecting
Open a new terminal.

Connect to the server using one of the following methods:

### netcat Command:

```bash
nc <server_public_ip> <port>
```
### PuTTY (Windows): 
If you're on Windows, select the raw connection type and fill in the host's IP and port in PuTTY's configuration.
Alternatively, run cmd and enter:

```bash
putty -raw <server_public_ip> <port>
```
SSH (Secure Shell): Not supported yet.

## Closing Connection
1. Execute the Ctrl+C command.
2. Enter clear to clear the terminal.

## Additional Features
Each user's messages are prefixed with their username for easy identification.
The server broadcasts messages to all connected users.
Users cannot connect with the same username more than once.
Color-coded messages for better readability.
The server shows the number of users upon authentication and updates when users join or leave the chat.

## Working Screenshot
<img width="1536" alt="Screenshot 2024-07-25 at 6 04 03 PM" src="https://github.com/user-attachments/assets/eb480403-3ca7-49ad-8918-87aba0b46c3d">







