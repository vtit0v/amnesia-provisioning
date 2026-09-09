from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://amnesia:amnesia_secure_pass@localhost/amnesia_provisioning"
    secret_key: str = "amnesia_provisioning_secret_key_2026"
    awg_config_path: str = "/etc/amnezia/amneziawg/awg0.conf"
    awg_interface: str = "awg0"
    awg_subnet: str = "10.77.77.0/24"
    awg_listen_port: int = 1234
    
    class Config:
        env_file = ".env"

settings = Settings()
