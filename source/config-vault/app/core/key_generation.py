from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import secrets
import string
from datetime import datetime, timedelta

class KeyGenerationService:
    @staticmethod
    def generate_rsa_key_pair(key_size: int = 2048) -> tuple[str, str]:
        """Generate RSA key pair and return (private_key, public_key) as PEM strings"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        
        public_key = private_key.public_key()
        
        # Serialize private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        
        # Serialize public key
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        
        return private_pem, public_pem
    
    @staticmethod
    def generate_kid() -> str:
        """Generate a unique Key ID"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(16))
    
    @staticmethod
    def calculate_expires_at(expires_in_days: int = 365) -> datetime:
        """Calculate expiration date"""
        return datetime.utcnow() + timedelta(days=expires_in_days)
