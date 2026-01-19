# generacion-leads-con-serpApi
Generar y buscar leads con serpApi

## Descripción

Generador de Leads Inteligente es una herramienta profesional de Python diseñada para identificar negocios locales que requieren servicios de optimización tecnológica. El sistema se conecta a la API de Google Maps a través de SerpApi para extraer información de empresas, analizar sus necesidades potenciales y priorizarlas según criterios específicos de oportunidad comercial.

Este script forma parte del Paquete de Eficiencia Total, una solución integrada que combina optimización de redes WiFi, domótica para ahorro energético y automatización de captación de clientes para pequeñas y medianas empresas.

## Características Principales

### Búsqueda Inteligente

Búsqueda en Google Maps por categorías específicas (talleres mecánicos, agencias de seguros, clínicas, etc.)

+ Configuración flexible de ciudad y tipos de negocio

+ Extracción estructurada de datos comerciales

## Análisis y Priorización Automática

1. Detección de oportunidades: Identifica negocios con rating bajo (<4 estrellas)

2. Evaluación de presencia digital: Detecta empresas sin sitio web

3. Sistema de etiquetado: Clasificación automática como "ALTA PRIORIDAD" o "Normal"

4. Criterios combinados: Empresas con múltiples necesidades reciben máxima prioridad

## Gestión de Datos Profesional

+ Exportación automática a formato CSV

+ Codificación UTF-8 para compatibilidad multilingüe

+ Estructura de datos normalizada y lista para importar en CRM

+ Generación de archivo separado para leads de alta prioridad

## Instalación y Configuración

### Prerrequisitos

+ Python 3.8 o superior

+ Conexión a Internet

+ Cuenta activa en SerpApi (nivel gratuito disponible)

## # CONFIGURACIÓN PERSONALIZABLE

+ API_KEY = "tu_clave_api_real_aquí"   # API Key de SerpApi

+ CIUDAD = "Tu Ciudad Aquí"            # Ciudad para la búsqueda

+ TIPOS_NEGOCIO = [                    # Tipos de negocio a buscar
    "Talleres mecánicos",
    "Agencias de seguros", 
    "Clínicas"
]

+ MAX_RESULTADOS = 20                  # Máximo de resultados por búsqueda

## Criterios de Priorización

### Negocios de ALTA PRIORIDAD

El sistema identifica automáticamente oportunidades comerciales mediante:

Rating bajo (< 4 estrellas):

+ Indica posibles problemas de satisfacción del cliente

+ Sugiere necesidad de mejorar procesos y atención

+ Oportunidad para ofrecer soluciones de optimización

Falta de sitio web:

+ Ausencia de presencia digital básica

+ Pérdida de visibilidad y captación online

+ Necesidad urgente de infraestructura tecnológica