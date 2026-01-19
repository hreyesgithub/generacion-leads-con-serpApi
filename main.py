import requests
import pandas as pd
import time
import json
from datetime import datetime

class GeneradorLeads:
    def __init__(self, api_key, ciudad="Madrid"):
        """
        Inicializa el generador de leads con la API key y ciudad
        
        Args:
            api_key (str): Tu API key de SerpApi
            ciudad (str): Ciudad para la búsqueda (ej: "Madrid", "Barcelona")
        """
        self.api_key = api_key
        self.ciudad = ciudad
        self.base_url = "https://serpapi.com/search"
        self.leads = []
        
    def buscar_negocios(self, tipo_negocio, max_resultados=20):
        """
        Busca negocios específicos en Google Maps mediante SerpApi
        
        Args:
            tipo_negocio (str): "Talleres mecánicos", "Agencias de seguros" o "Clínicas"
            max_resultados (int): Número máximo de resultados a obtener
        """
        print(f"🔍 Buscando {tipo_negocio} en {self.ciudad}...")
        
        # Configurar parámetros de búsqueda
        params = {
            "engine": "google_maps",
            "q": f"{tipo_negocio} {self.ciudad}",
            "type": "search",
            "api_key": self.api_key,
            "hl": "es",
            "gl": "es",
            "num": max_resultados
        }
        
        try:
            # Realizar la solicitud a la API
            respuesta = requests.get(self.base_url, params=params, timeout=30)
            respuesta.raise_for_status()  # Lanza excepción para códigos HTTP erróneos
            
            datos = respuesta.json()
            
            # Procesar resultados
            if "local_results" in datos:
                self._procesar_resultados(datos["local_results"], tipo_negocio)
            else:
                print("⚠️ No se encontraron resultados o la estructura de respuesta cambió")
                print("Estructura recibida:", json.dumps(datos, indent=2)[:500] + "...")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en la solicitud HTTP: {e}")
        except json.JSONDecodeError as e:
            print(f"❌ Error decodificando JSON: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def _procesar_resultados(self, resultados, tipo_negocio):
        """
        Procesa y extrae información de cada negocio
        
        Args:
            resultados (list): Lista de resultados de la API
            tipo_negocio (str): Tipo de negocio para categorizar
        """
        for negocio in resultados:
            try:
                # Extraer datos básicos
                nombre = negocio.get("title", "No disponible")
                direccion = negocio.get("address", "No disponible")
                
                # Extraer teléfono (puede estar en diferentes campos)
                telefono = negocio.get("phone", "No disponible")
                if telefono == "No disponible":
                    telefono = negocio.get("phone_number", "No disponible")
                
                # Extraer calificación
                rating_str = negocio.get("rating", "0")
                try:
                    rating = float(rating_str) if rating_str else 0.0
                except ValueError:
                    rating = 0.0
                
                # Extraer sitio web
                sitio_web = negocio.get("website", "No disponible")
                
                # Determinar prioridad
                prioridad = self._determinar_prioridad(rating, sitio_web)
                
                # Crear registro del lead
                lead = {
                    "Nombre": nombre,
                    "Dirección": direccion,
                    "Teléfono": telefono,
                    "Calificación": rating,
                    "Sitio Web": sitio_web,
                    "Tipo Negocio": tipo_negocio,
                    "Prioridad": prioridad,
                    "Fecha Extracción": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Ciudad": self.ciudad
                }
                
                self.leads.append(lead)
                print(f"✓ Encontrado: {nombre} ({prioridad})")
                
            except Exception as e:
                print(f"⚠️ Error procesando negocio: {e}")
                continue
    
    def _determinar_prioridad(self, rating, sitio_web):
        """
        Determina si el negocio es de ALTA PRIORIDAD
        
        Criterios:
        1. Rating menor a 4 estrellas
        2. No tiene sitio web
        
        Args:
            rating (float): Calificación del negocio
            sitio_web (str): URL del sitio web
        
        Returns:
            str: "ALTA PRIORIDAD" o "Normal"
        """
        if rating < 4.0 or sitio_web == "No disponible":
            return "ALTA PRIORIDAD"
        return "Normal"
    
    def guardar_csv(self, filename="clientes_potenciales.csv"):
        """
        Guarda los leads en un archivo CSV
        
        Args:
            filename (str): Nombre del archivo CSV
        """
        if not self.leads:
            print("📭 No hay leads para guardar")
            return
        
        df = pd.DataFrame(self.leads)
        
        # Ordenar por prioridad (ALTA PRIORIDAD primero)
        df["Prioridad_Orden"] = df["Prioridad"].apply(lambda x: 0 if x == "ALTA PRIORIDAD" else 1)
        df = df.sort_values(by=["Prioridad_Orden", "Calificación"], ascending=[True, False])
        df = df.drop(columns=["Prioridad_Orden"])
        
        # Guardar en CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"💾 Guardados {len(self.leads)} leads en '{filename}'")
        
        # Mostrar estadísticas
        alta_prioridad = df[df["Prioridad"] == "ALTA PRIORIDAD"]
        print(f"📊 Estadísticas:")
        print(f"   • Total leads: {len(df)}")
        print(f"   • ALTA PRIORIDAD: {len(alta_prioridad)}")
        print(f"   • Sin sitio web: {len(df[df['Sitio Web'] == 'No disponible'])}")
        print(f"   • Rating < 4: {len(df[df['Calificación'] < 4])}")
    
    def ejecutar_busqueda_completa(self):
        """
        Ejecuta búsqueda para todos los tipos de negocio
        """
        tipos_negocio = [
            "Talleres mecánicos",
            "Agencias de seguros", 
            "Clínicas"
        ]
        
        for tipo in tipos_negocio:
            self.buscar_negocios(tipo)
            time.sleep(2)  # Pausa para no sobrecargar la API
        
        if self.leads:
            self.guardar_csv()
            
            # Guardar también un resumen de alta prioridad
            df = pd.DataFrame(self.leads)
            alta_prioridad = df[df["Prioridad"] == "ALTA PRIORIDAD"]
            if not alta_prioridad.empty:
                alta_prioridad.to_csv("clientes_alta_prioridad.csv", index=False, encoding='utf-8-sig')
                print(f"💾 Guardados {len(alta_prioridad)} leads de ALTA PRIORIDAD en 'clientes_alta_prioridad.csv'")
        else:
            print("❌ No se encontraron leads. Revisa tu API key o parámetros de búsqueda.")


def main():
    """
    Función principal del script
    """
    print("=" * 60)
    print("🚀 GENERADOR DE LEADS PARA SERVICIOS DE AUTOMATIZACIÓN")
    print("=" * 60)
    
    # CONFIGURACIÓN - ¡MODIFICA ESTOS VALORES!
    API_KEY = "TU_API_KEY_AQUÍ"  # 👈 Reemplaza con tu API key real
    CIUDAD = "Madrid"  # 👈 Cambia a tu ciudad
    
    # Validar API key
    if API_KEY == "TU_API_KEY_AQUÍ":
        print("❌ ERROR: Debes configurar tu API key de SerpApi")
        print("\n📝 Cómo obtener tu API key gratuita:")
        print("1. Regístrate en https://serpapi.com")
        print("2. Verifica tu email")
        print("3. Encuentra tu API key en el dashboard")
        print("4. Reemplaza 'TU_API_KEY_AQUÍ' con tu clave real")
        return
    
    # Crear instancia del generador
    generador = GeneradorLeads(api_key=API_KEY, ciudad=CIUDAD)
    
    # Ejecutar búsqueda completa
    generador.ejecutar_busqueda_completa()
    
    # Mostrar primeros resultados
    if generador.leads:
        print("\n" + "=" * 60)
        print("🎯 LEADS DE ALTA PRIORIDAD (Potenciales Clientes):")
        print("=" * 60)
        
        df = pd.DataFrame(generador.leads)
        alta_prioridad = df[df["Prioridad"] == "ALTA PRIORIDAD"]
        
        if not alta_prioridad.empty:
            for idx, lead in alta_prioridad.head(5).iterrows():
                print(f"\n🏢 {lead['Nombre']}")
                print(f"   📍 {lead['Dirección']}")
                print(f"   📞 {lead['Teléfono']}")
                print(f"   ⭐ Rating: {lead['Calificación']}")
                print(f"   🌐 Sitio Web: {lead['Sitio Web']}")
                print(f"   🏷️  {lead['Tipo Negocio']}")
        else:
            print("No se encontraron leads de alta prioridad.")
        
        print("\n" + "=" * 60)
        print("✅ Proceso completado. Revisa los archivos CSV generados.")
        print("=" * 60)


if __name__ == "__main__":
    main()