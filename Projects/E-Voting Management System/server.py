import socket
import threading

HOST = '0.0.0.0'
PORT = 9999

candidates = {
    'Alice': 0,
    'Bob': 0,
    'Charlie': 0
}

ADMIN_PASSWORD = 'admin123'

def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    conn.sendall(b"Welcome to the Online Vote Casting System\n")
    conn.sendall(b"Commands: LIST, VOTE <name>, RESULTS <password>, HELP, EXIT\n")
    conn.sendall(b"Enter command:\n")

    try:
        while True:
            data = b""
            while not data.endswith(b"\n"):
                chunk = conn.recv(1024)
                if not chunk:
                    print(f"[-] {addr} disconnected")
                    return
                data += chunk
            cmd = data.decode().strip()
            if not cmd:
                conn.sendall(b"Enter command:\n")
                continue
            parts = cmd.split()
            command = parts[0].upper()

            if command == 'LIST':
                msg = "Candidates:\n"
                for name in candidates:
                    msg += f"- {name}\n"
                conn.sendall(msg.encode() + b"Enter command:\n")

            elif command == 'VOTE':
                if len(parts) < 2:
                    conn.sendall(b"Usage: VOTE <name>\nEnter command:\n")
                    continue
                name = parts[1]
                if name in candidates:
                    candidates[name] += 1
                    conn.sendall(f"Vote cast for {name}!\n".encode() + b"Enter command:\n")
                else:
                    conn.sendall(b"Invalid candidate name.\nEnter command:\n")

            elif command == 'RESULTS':
                if len(parts) < 2 or parts[1] != ADMIN_PASSWORD:
                    conn.sendall(b"Access denied.\nEnter command:\n")
                    continue
                msg = "Current Results:\n"
                for name, count in candidates.items():
                    msg += f"{name}: {count} votes\n"
                conn.sendall(msg.encode() + b"Enter command:\n")

            elif command == 'HELP':
                help_msg = b"Commands: LIST, VOTE <name>, RESULTS <password>, HELP, EXIT\nEnter command:\n"
                conn.sendall(help_msg)

            elif command == 'EXIT':
                conn.sendall(b"Goodbye!\n")
                print(f"[-] {addr} disconnected")
                break

            else:
                conn.sendall(b"Unknown command. Type HELP for options.\nEnter command:\n")

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] VoteServer listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == '__main__':
    start_server()
