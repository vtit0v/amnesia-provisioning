import random
import secrets
from config import settings

class ProvisioningService:
    @staticmethod
    def generate_random_hashes():
        return {
            'h1': random.randint(1000000000, 4294967295),
            'h2': random.randint(1000000000, 4294967295),
            'h3': random.randint(1000000000, 4294967295),
            'h4': random.randint(1000000000, 4294967295),
        }
    
    @staticmethod
    def generate_conf(client_id: str, h1: int, h2: int, h3: int, h4: int) -> str:
        private_key = secrets.token_urlsafe(32)[:32]
        public_key = secrets.token_urlsafe(32)[:32]
        peer_ip = f"10.77.77.{random.randint(2, 254)}"
        
        conf = f"[Interface]\nAddress = {peer_ip}/32\nPrivateKey = {private_key}\n\nJc = 4\nJmin = 8\nJmax = 80\nS1 = 30\nS2 = 45\nS3 = 0\nS4 = 0\nH1 = {h1}\nH2 = {h2}\nH3 = {h3}\nH4 = {h4}\n\n[Peer]\nPublicKey = {public_key}\nAllowedIPs = 0.0.0.0/0\nEndpoint = 148.253.208.101:{settings.awg_listen_port}"
        return conf
