import socket
import sys
import time

def test_connect(path):
    print(f"Connecting to {path}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('127.0.0.1', 8086))
        
        req = (
            f"GET {path} HTTP/1.1\r\n"
            "Host: localhost:8086\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        ).encode()
        
        s.sendall(req)
        
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = s.recv(4096)
            if not chunk:
                break
            resp += chunk
            
        if b"101 Switching Protocols" in resp:
            print(f"SUCCESS: Connected to {path}")
            return True
        else:
            print(f"FAILURE: Could not connect to {path}. Response:\n{resp.decode('utf-8', 'ignore')}")
            return False
    except ConnectionRefusedError:
        print("FAILURE: Connection refused. Is the server running?")
        return False
    finally:
        s.close()

if __name__ == "__main__":
    # Wait a bit for server to start
    time.sleep(2)
    
    success = True
    if not test_connect("/alpha"): success = False
    if not test_connect("/beta"): success = False
    if not test_connect("/"): success = False
    
    if success:
        print("\nAll connections successful.")
        sys.exit(0)
    else:
        print("\nSome connections failed.")
        sys.exit(1)
