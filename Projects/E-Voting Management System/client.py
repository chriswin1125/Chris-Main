import socket
import sys

HOST = '127.0.0.1'
PORT = 9999

def readline_from_sock(sock):
    """
    Reads a line from the socket, handling incomplete messages.
    """
    buf = b''
    while True:
        try:
            chunk = sock.recv(1)
            if not chunk:
                return None
            buf += chunk
            if chunk == b'\n':
                return buf.decode('utf-8').strip()
        except socket.error:
            return None

def interactive():
    """
    Handles the interactive client-server communication.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f"Connection refused. Ensure the server is running on {HOST}:{PORT}")
            return
        
        while True:
            line = readline_from_sock(s)
            if line is None:
                print('Disconnected by server', flush=True)
                return
            print(line, flush=True)
            if line.endswith('Enter command:'):
                break

        while True:
            try:
                cmd = input('> ').strip()
                if not cmd:
                    continue
                s.sendall((cmd + '\n').encode('utf-8'))

                if cmd.upper().startswith('EXIT'):
                    print('Goodbye!', flush=True)
                    break

                while True:
                    response_line = readline_from_sock(s)
                    if response_line is None:
                        print('Server closed connection', flush=True)
                        return
                    print(response_line, flush=True)
                    if response_line.endswith('Enter command:'):
                        break

            except (IOError, socket.error):
                print("Connection lost.")
                break
            except KeyboardInterrupt:
                print('\nExiting client', flush=True)
                sys.exit(0)

if __name__ == '__main__':
    interactive()
