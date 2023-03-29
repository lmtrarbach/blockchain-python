class Wallet:
    def __init__(self, wallet_dir):
        self.wallet_dir = wallet_dir
        self.private_key = None
        self.public_key = None
        self.load_or_create_wallet()

    def load_or_create_wallet(self):
        # Check if wallet exists
        if not os.path.exists(self.wallet_dir):
            os.makedirs(self.wallet_dir)

        # Check if private key exists
        private_key_file = os.path.join(self.wallet_dir, "private_key.pem")
        if os.path.exists(private_key_file):
            with open(private_key_file, "r") as f:
                self.private_key = ecdsa.SigningKey.from_pem(f.read())

        # If private key doesn't exist, create a new key pair
        if not self.private_key:
            self.private_key = ecdsa.SigningKey.generate()
            with open(private_key_file, "w") as f:
                f.write(self.private_key.to_pem().decode())

        # Generate public key from private key
        self.public_key = self.private_key.get_verifying_key()

    def get_address(self):
        # Generate address from public key
        public_key_bytes = self.public_key.to_string()
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        ripemd160_hash = hashlib.new("ripemd160", sha256_hash).digest()
        return binascii.hexlify(ripemd160_hash).decode()