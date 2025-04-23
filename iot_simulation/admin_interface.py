from web3 import Web3
import json
import os
from dotenv import load_dotenv
from eth_account import Account
import time

load_dotenv()



# Adresse et clé privée de l'admin (NE PAS exposer en dur dans le code en prod)
private_key = os.getenv("PRIVATE_KEY")
admin_address = os.getenv("ADMIN_ADDRESS")
infura_url = os.getenv("INFURA_URL")

# Connexion à Sepolia via Infura
w3 = Web3(Web3.HTTPProvider(infura_url))

# Charger l'ABI du contrat
with open("IoTStrongAuth.json") as f:
    abi = json.load(f)["abi"]

contract_address = "0xc41F8f967CaB0DFF9a5C5173f65dfb0bEfa41F06"
contract = w3.eth.contract(address=contract_address, abi=abi)

def send_transaction(function):
    nonce = w3.eth.get_transaction_count(admin_address)

    tx = function.build_transaction({
        "chainId": 11155111,
        "gas": 200000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": nonce,
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)

    start_time = time.time()
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"⏱️ Temps pour inclusion de la transaction : {elapsed:.2f} secondes")

    return receipt

def register_device(address):
    tx_function = contract.functions.registerDevice(address)
    receipt = send_transaction(tx_function)
    print(f"✅ Device {address} registered in tx {receipt.transactionHash.hex()}")

def deactivate_device(address):
    tx_function = contract.functions.revokeDevice(address)
    receipt = send_transaction(tx_function)
    print(f"🚫 Device {address} deactivated in tx {receipt.transactionHash.hex()}")

def show_nonce(address):
    nonce = contract.functions.getNonce(address).call()
    print(f"🔢 Nonce de {address} : {nonce}")

def create_device():
    # Générer un nouveau wallet (clé privée + adresse)
    new_account = Account.create()

    print(f"✅ Nouvelle adresse : {new_account.address}")
    print(f"🔐 Clé privée : {new_account.key.hex()}")
    amount_eth = 0.01
    tx = {
        'nonce': w3.eth.get_transaction_count(admin_address),
        'to': new_account.address,
        'value': w3.to_wei(amount_eth, 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei('5', 'gwei'),
        'chainId': 11155111
    }

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)

    start_time = time.time()
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"⏱️ Temps pour inclusion de la transaction : {elapsed:.2f} secondes")

    print(f"✅ {amount_eth} ETH envoyés à {new_account.address} | tx hash: {tx_hash.hex()}")

def menu():
    while True:
        print("\n[Admin Menu]")
        print("1. Enregistrer un device")
        print("2. Désactiver un device")
        print("3. Voir le nonce d’un device")
        print("4. Créer un device")
        print("0. Quitter")

        choice = input("Choix : ")
        if choice == "1":
            addr = input("Adresse du device : ")
            register_device(addr)
        elif choice == "2":
            addr = input("Adresse du device : ")
            deactivate_device(addr)
        elif choice == "3":
            addr = input("Adresse du device : ")
            show_nonce(addr)
        elif choice == "4":
            create_device()
        elif choice == "0":
            break

if __name__ == "__main__":
    menu()