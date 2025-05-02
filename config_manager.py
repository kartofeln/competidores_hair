import json
import os
from typing import Dict, Optional
import logging

class ConfigManager:
    def __init__(self):
        self.config_path = os.path.join('config', 'credentials.json')
        self._ensure_config_directory()
        
    def _ensure_config_directory(self):
        """Asegura que el directorio de configuración existe"""
        os.makedirs('config', exist_ok=True)
        
    def load_credentials(self) -> Optional[Dict]:
        """Carga las credenciales desde el archivo de configuración"""
        try:
            if not os.path.exists(self.config_path):
                logging.error("No se encontró el archivo de credenciales")
                return None
                
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error al cargar credenciales: {str(e)}")
            return None
            
    def save_credentials(self, credentials: Dict) -> bool:
        """Guarda las credenciales en el archivo de configuración"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(credentials, f, indent=4)
            return True
        except Exception as e:
            logging.error(f"Error al guardar credenciales: {str(e)}")
            return False
            
    def validate_credentials(self, credentials: Dict) -> bool:
        """Valida que las credenciales tengan la estructura correcta"""
        required_fields = {
            'google_shopping': [
                'project_id', 'private_key_id', 'private_key',
                'client_email', 'client_id'
            ],
            'amazon': [
                'access_key', 'secret_key', 'assoc_tag'
            ]
        }
        
        try:
            for section, fields in required_fields.items():
                if section not in credentials:
                    logging.error(f"Falta la sección {section} en las credenciales")
                    return False
                    
                for field in fields:
                    if field not in credentials[section]:
                        logging.error(f"Falta el campo {field} en la sección {section}")
                        return False
                        
            return True
        except Exception as e:
            logging.error(f"Error al validar credenciales: {str(e)}")
            return False
            
    def setup_credentials(self) -> bool:
        """Guía al usuario en la configuración de credenciales"""
        print("\n=== Configuración de Credenciales ===")
        
        # Google Shopping API
        print("\n1. Configuración de Google Shopping API:")
        google_credentials = {
            'project_id': input("Project ID: "),
            'private_key_id': input("Private Key ID: "),
            'private_key': input("Private Key: "),
            'client_email': input("Client Email: "),
            'client_id': input("Client ID: "),
            'auth_uri': "https://accounts.google.com/o/oauth2/auth",
            'token_uri': "https://oauth2.googleapis.com/token",
            'auth_provider_x509_cert_url': "https://www.googleapis.com/oauth2/v1/certs",
            'client_x509_cert_url': input("Client X509 Cert URL: ")
        }
        
        # Amazon API
        print("\n2. Configuración de Amazon API:")
        amazon_credentials = {
            'access_key': input("Access Key: "),
            'secret_key': input("Secret Key: "),
            'assoc_tag': input("Associate Tag: ")
        }
        
        # Combinar credenciales
        credentials = {
            'google_shopping': google_credentials,
            'amazon': amazon_credentials
        }
        
        # Validar y guardar
        if self.validate_credentials(credentials):
            if self.save_credentials(credentials):
                print("\n✅ Credenciales guardadas correctamente")
                return True
            else:
                print("\n❌ Error al guardar las credenciales")
                return False
        else:
            print("\n❌ Las credenciales no son válidas")
            return False

if __name__ == "__main__":
    config_manager = ConfigManager()
    config_manager.setup_credentials() 