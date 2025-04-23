import socket, threading, json, time, random
from utils.web3_config import w3, contract, verify_signature, authenticate_device
from utils.crypto_utils import sign_message, hash_message
import os
from dotenv import load_dotenv
load_dotenv()

MY_PRIVATE_KEY = os.getenv("PRIVATE_KEY_DEVICE2")
MY_ADDRESS = w3.eth.account.from_key(MY_PRIVATE_KEY).address

MY_PORT = 6002

def handle_connection(conn, addr):
    print(f"[📥] Connexion de {addr}")
    data = conn.recv(4096)
    if not data:
        return

    try:
        payload = json.loads(data.decode())
        sig = payload['signature']
        sender = payload['sender']
        name = payload['nom']
        nonce = contract.functions.getNonce(sender).call()

        # Reconstruction hash + vérification
        msg_hash = contract.functions.getMessageHash(sender, nonce).call()
        is_authenticated = verify_signature(msg_hash, sig)
        if is_authenticated:
            print(f"[✅] Authentification validée de {name} avec l'address {sender}")
            #authenticate_device(msg_hash, sig, MY_ADDRESS, MY_PRIVATE_KEY, name)
        else:
            print(f"[❌] Authentification échouée de {name} avec l'address {sender}")

    except Exception as e:
        print(f"[⚠️] Erreur traitement message : {e}")

    conn.close()

def server_thread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", MY_PORT))
        s.listen()
        print(f"[🟢] IoT listening on port {MY_PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_connection, args=(conn, addr)).start()

def client_thread():
    while True:
        try:
            with open("peers.txt", "r") as f:
                peers = f.read().splitlines()
            peers = [p for p in peers if not p.endswith(f":{MY_PORT}")]

            if peers:
                target = random.choice(peers)
                ip, port = target.split(":")
                port = int(port)

                nonce = contract.functions.getNonce(MY_ADDRESS).call()
                msg_hash = hash_message(MY_ADDRESS, nonce)
                sig = sign_message(MY_PRIVATE_KEY, msg_hash)
                
                payload = {
                    "nom" : "device2",
                    "sender": MY_ADDRESS,
                    "signature": {
                        "v": sig['v'],
                        "r": sig['r'],
                        "s": sig['s']
                    }
                }

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((ip, port))
                    s.sendall(json.dumps(payload).encode())
                    print(f"[📤] Envoyé à {ip}:{port}")
        except Exception as e:
            print(f"[⚠️] Erreur envoi : {e}")
        time.sleep(30)

threading.Thread(target=server_thread, daemon=True).start()
threading.Thread(target=client_thread, daemon=True).start()

while True:
    time.sleep(1)