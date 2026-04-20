# Writeup: Knight Squad Academy Jail 2 (KnightCTF 2025)
**Category:** Python Jail / Misc | **Points:** 320 | **Challenge Author:** NomanProdhan

## Description
The challenge presents a restricted Python sandbox (Jail). Our objective is to bypass the restrictions or find a hidden mechanism to leak the flag.
> **Hint:** "In the world of Knight Squad Academy jail only a knight can help you!"

## Exploration
Initial interaction with the server showed that almost all standard built-ins (`print`, `chr`, `eval`) were blocked or removed. However, error messages revealed a specific behavior:
* Standard input: `error`
* Undefined function call: `name() doesn't exist`

Following the hint, I discovered a custom function: `knight()`.

### The `knight()` Function Logic
Through manual testing, I identified the following constraints:
* **Input Length:** Must be exactly **30 characters**.
* **Output:** Two integers (e.g., `1 0`).
* **Feedback System:** This is a **Mastermind/Wordle-style** feedback system.
    * **1st Number:** Count of characters in the correct position.
    * **2nd Number:** Count of correct characters in the wrong position.

## Exploitation Strategy
Since we receive immediate feedback on the number of correct positions, we can perform a **linear brute-force** (character-by-character) instead of an exponential one.

### Automated Solver (Python)
```python
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
```

## Conclusion
**Flag:** `KCTF{_only_A_knight_can_bot}`
The challenge highlights the importance of analyzing side-channel leaks (in this case, scoring feedback) to bypass sandbox restrictions.