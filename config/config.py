# config/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    # API Keys
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '')
    AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY', '')
    AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', '')
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
    
    # Configuración del sistema
    CIUDAD_DEFAULT = os.getenv('CIUDAD_DEFAULT', 'Toledo')
    TIPOS_NEGOCIO = ['Talleres mecánicos', 'Agencias de seguros', 'Clínicas']
    
    # Rutas de archivos
    PATH_LEADS_CSV = 'data/leads.csv'
    PATH_LEADS_PRIORIZADOS = 'data/leads_priorizados.csv'
    PATH_LOGS = 'logs/'
    
    # Configuración de email
    EMAIL_FROM = os.getenv('EMAIL_FROM', 'tu_negocio@email.com')
    EMAIL_REPLY_TO = os.getenv('EMAIL_REPLY_TO', 'soporte@tudominio.com')
    
    # Configuración del dashboard
    STREAMLIT_PORT = 8501
    STREAMLIT_THEME = "dark"
    
    @classmethod
    def validar_configuracion(cls):
        """Valida que todas las configuraciones necesarias estén presentes"""
        errores = []
        
        if not cls.SERPAPI_API_KEY:
            errores.append("SERPAPI_API_KEY no configurada")
        
        if not cls.AIRTABLE_API_KEY:
            errores.append("AIRTABLE_API_KEY no configurada")
        
        if errores:
            print("⚠️ ERRORES DE CONFIGURACIÓN:")
            for error in errores:
                print(f"   • {error}")
            print("\n💡 Solución: Crea un archivo .env con las variables requeridas")
            return False
        
        return True

# Variables para Streamlit secrets (si se usa)
SECRETS_STREAMLIT = {
    "AIRTABLE_API_KEY": Config.AIRTABLE_API_KEY,
    "AIRTABLE_BASE_ID": Config.AIRTABLE_BASE_ID
}