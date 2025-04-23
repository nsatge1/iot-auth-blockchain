from web3 import Web3
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

infura_url = os.getenv("INFURA_URL")

# Connexion à Sepolia via Infura
w3 = Web3(Web3.HTTPProvider(infura_url))

CONTRACT_ADDRESS = "0xc41F8f967CaB0DFF9a5C5173f65dfb0bEfa41F06"  # adresse du contrat déployé


with open("ioTStrongAuth.json") as f:
    ABI = json.load(f)["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)


def verify_signature(message_hash: bytes, signature: dict) -> bool:
    try:
        is_authenticated = contract.functions.isAuthenticated(
            message_hash,
            v=signature["v"],
            r=Web3.to_bytes(hexstr=signature["r"]),
            s=Web3.to_bytes(hexstr=signature["s"])
        ).call()
        return is_authenticated
    except Exception as e:
        print(f"🚫 Erreur lors de la vérification de la signature: {str(e)}")
        return False

def authenticate_device(message_hash: bytes, signature: dict, address: str, private_key: str, name: str):
    try:
        nonce = w3.eth.get_transaction_count(address)

        tx = contract.functions.authenticate(
            message_hash,
            signature["v"],
            Web3.to_bytes(hexstr=signature["r"]),
            Web3.to_bytes(hexstr=signature["s"])
        ).build_transaction({
            "chainId": 11155111,  # Sepolia
            "gas": 200000,
            "gasPrice": w3.to_wei("20", "gwei"),
            "nonce": nonce,
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)

        start_time = time.time()

        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        duration = time.time() - start_time
        auth_success_event = contract.events.AuthSuccess().process_receipt(receipt)
        if auth_success_event:
            event_data = auth_success_event[0]['args']
            signer = event_data['device']
            success = event_data['success']
        else:
            print(f"⚠️ Aucun événement AuthSuccess trouvé. (tx: {tx_hash.hex()}, durée : {duration:.2f}s)")


        print(f"✅ Authentification réussie de {name} avec l'address {signer}")
        print(f"⏱️ Temps pour inclusion de la transaction : {duration:.2f} secondes")
    except Exception as e:
        print(f"🚫 Erreur d'authentification : {str(e)}")