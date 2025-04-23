from eth_account import Account
from eth_account.messages import encode_defunct
from web3.auto import w3

def sign_message(private_key: str, message_hash: bytes) -> dict:
    signed_message = Account.sign_message(message_hash, private_key)
    return {
        "v": signed_message.v,
        "r": signed_message.r.to_bytes(32, 'big').hex(),
        "s": signed_message.s.to_bytes(32, 'big').hex()
    }

def hash_message(device_address: str, nonce: int):
    message_hash = w3.solidity_keccak(["address", "uint256"], [device_address, nonce])

    return encode_defunct(message_hash)


