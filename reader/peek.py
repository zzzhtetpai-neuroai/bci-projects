import socket, json, urllib.request

BOARD_IP = "192.168.4.1"
PC_IP = "192.168.4.2"
PORT = 8899

# 1. open our door first
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", PORT))
srv.listen(1)
srv.settimeout(15)
print("Listening on", PORT)

# 2. tell the board where to send data (OpenBCI WiFi API)
body = json.dumps({"ip": PC_IP, "port": PORT, "output": "raw",
                   "delimiter": True, "latency": 10000}).encode()
req = urllib.request.Request(f"http://{BOARD_IP}/tcp", data=body,
                             headers={"Content-Type": "application/json"})
print("POST /tcp ->", urllib.request.urlopen(req, timeout=5).read().decode())

# 3. wait for the board to call in
conn, addr = srv.accept()
print("Board connected from", addr)

# 4. start streaming
print("stream/start ->", urllib.request.urlopen(
    f"http://{BOARD_IP}/stream/start", timeout=5).read().decode())

# 5. read 10 frames
buf, frames = b"", 0
conn.settimeout(5)
while frames < 10:
    buf += conn.recv(1024)
    while len(buf) >= 33:
        i = buf.find(b"\xA0")
        if i < 0: buf = b""; break
        if len(buf) - i < 33: buf = buf[i:]; break
        f = buf[i:i+33]
        if f[32] & 0xF0 == 0xC0:
            print(f"frame {f[1]:3d}:", f.hex(" "))
            frames += 1; buf = buf[i+33:]
        else:
            buf = buf[i+1:]

urllib.request.urlopen(f"http://{BOARD_IP}/stream/stop", timeout=5)
conn.close(); srv.close()
print("Done")