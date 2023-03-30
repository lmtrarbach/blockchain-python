import json
import ecdsa

class Transaction:
    def __init__(self, sender_address, sender_private_key, recipient_address, amount):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.amount = amount

    def to_dict(self):
        return {
            "sender_address": self.sender_address,
            "recipient_address": self.recipient_address,
            "amount": self.amount
        }

    def sign_transaction(self):
        # Create a digital signature using sender's private key
        print(self.sender_private_key)
        private_key = ecdsa.SigningKey.from_pem(self.sender_private_key)
        message = json.dumps(self.to_dict()).encode()
        signature = private_key.sign(message)

        # Add the digital signature to the transaction
        self.signature = signature.hex()