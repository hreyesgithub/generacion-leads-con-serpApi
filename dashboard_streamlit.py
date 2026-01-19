# 04_dashboard_streamlit.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from pyairtable import Api
import os
import glob

archivos = glob.glob("clientes_potenciales_*.csv")

# Configuración de página
st.set_page_config(
    page_title="Dashboard Leads - Eficiencia Total",
    page_icon="📊",
    layout="wide"
)

class DashboardLeads:
    def __init__(self):
        # Conexión a Airtable
        self.api_key = st.secrets.get("AIRTABLE_API_KEY", os.getenv('AIRTABLE_API_KEY'))
        self.base_id = st.secrets.get("AIRTABLE_BASE_ID", os.getenv('AIRTABLE_BASE_ID'))
        
        if self.api_key and self.base_id:
            self.api = Api(self.api_key)
            self.table = self.api.table(self.base_id, 'Leads')
        else:
            st.warning("⚠️ Configura las credenciales de Airtable en secrets.toml")
            self.table = None
    
    def cargar_datos(self):
        """Carga datos desde Airtable o CSV local"""
        if self.table:
            records = self.table.all()
            df = pd.DataFrame([record['fields'] for record in records])
        else:
            # Modo demo con datos locales
            if not archivos:
                raise FileNotFoundError("No se encontraron archivos de clientes_potenciales")

            archivo_mas_reciente = max(archivos, key=os.path.getctime)
            df = pd.read_csv(archivo_mas_reciente)
        
        return df
    
    def calcular_metricas_clave(self, df):
        """Calcula métricas importantes para el dashboard"""
        metricas = {
            'total_leads': len(df),
            'alta_prioridad': len(df[df['Prioridad'] == 'ALTA PRIORIDAD']),
            'sin_web': len(df[df['Sitio Web'] == 'No disponible']),
            'rating_bajo': len(df[df['Calificación'] < 4]),
            'tasa_conversion_estimada': f"{(len(df[df['Prioridad'] == 'ALTA PRIORIDAD']) / len(df) * 100):.1f}%",
            'valor_potencial_total': len(df) * 2500,  # Estimación $2,500 por cliente
        }
        return metricas
    
    def crear_grafico_distribucion(self, df):
        """Gráfico de distribución por tipo de negocio y prioridad"""
        fig = px.sunburst(
            df, 
            path=['Tipo Negocio', 'Prioridad'],
            title='Distribución de Leads por Tipo y Prioridad',
            color='Calificación',
            color_continuous_scale='RdYlGn',
            range_color=[1, 5]
        )
        fig.update_layout(height=500)
        return fig
    
    def crear_mapa_calor_ubicacion(self, df):
        """Mapa de calor por ubicación (simulado)"""
        # En una implementación real, geocodificarías las direcciones
        fig = px.density_map(
            df,
            lat=[39.86] * len(df),  # Ejemplo: Toledo
            lon=[-4.04] * len(df),
            z=df['Calificación'],
            radius=10,
            center=dict(lat=39.86, lon=-4.04),
            zoom=10,
            map_style="open-street-map",
            title='Concentración de Leads por Zona',
            height=600
        )
        return fig
    
    def crear_grafico_evolucion(self, df):
        """Gráfico de evolución temporal (si hay fechas)"""
        if 'Fecha_Ingreso' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha_Ingreso'])
            df_diario = df.groupby(df['Fecha'].dt.date).size().reset_index(name='Leads')
            
            fig = px.line(
                df_diario,
                x='Fecha',
                y='Leads',
                title='Evolución Diaria de Leads Capturados',
                markers=True
            )
        else:
            # Gráfico de barras simple
            df_plot = (
                df['Tipo Negocio']
                .value_counts()
                .reset_index(name='count')
                .rename(columns={'index': 'Tipo Negocio'})
            )

            fig = px.bar(
                df_plot,
                x='Tipo Negocio',
                y='count',
                title='Leads por Tipo de Negocio',
                color='Tipo Negocio'
            )

        return fig

def main():
    st.title("📊 Dashboard de Leads - Paquete Eficiencia Total")
    st.markdown("---")
    
    dashboard = DashboardLeads()
    
    # Cargar datos
    with st.spinner("Cargando datos..."):
        df = dashboard.cargar_datos()
    
    if df.empty:
        st.error("No se encontraron datos. Ejecuta primero el colector de leads.")
        return
    
    # Sidebar con filtros
    st.sidebar.header("🔍 Filtros")
    
    tipo_negocio = st.sidebar.multiselect(
        "Tipo de Negocio",
        options=df['Tipo Negocio'].unique(),
        default=df['Tipo Negocio'].unique()
    )
    
    prioridad = st.sidebar.multiselect(
        "Prioridad",
        options=df['Prioridad'].unique(),
        default=df['Prioridad'].unique()
    )
    
    rating_min, rating_max = st.sidebar.slider(
        "Rango de Calificación",
        min_value=float(df['Calificación'].min()),
        max_value=float(df['Calificación'].max()),
        value=(0.0, 5.0)
    )
    
    # Aplicar filtros
    df_filtrado = df[
        (df['Tipo Negocio'].isin(tipo_negocio)) &
        (df['Prioridad'].isin(prioridad)) &
        (df['Calificación'] >= rating_min) &
        (df['Calificación'] <= rating_max)
    ]
    
    # Métricas principales
    st.subheader("📈 Métricas Clave")
    
    col1, col2, col3, col4 = st.columns(4)
    
    metricas = dashboard.calcular_metricas_clave(df_filtrado)
    
    with col1:
        st.metric("Total Leads", metricas['total_leads'])
    
    with col2:
        st.metric("Alta Prioridad", metricas['alta_prioridad'])
    
    with col3:
        st.metric("Sin Sitio Web", metricas['sin_web'])
    
    with col4:
        st.metric("Valor Potencial", f"${metricas['valor_potencial_total']:,.0f}")
    
    # Gráficos
    st.markdown("---")
    st.subheader("📊 Visualizaciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(dashboard.crear_grafico_distribucion(df_filtrado), width='stretch')
    
    with col2:
        st.plotly_chart(dashboard.crear_grafico_evolucion(df_filtrado), width='stretch')
    
    # Mapa
    st.plotly_chart(dashboard.crear_mapa_calor_ubicacion(df_filtrado), width='stretch')
    
    # Tabla interactiva de leads
    st.markdown("---")
    st.subheader("📋 Lista de Leads Filtrados")
    
    # Seleccionar columnas para mostrar
    columnas = st.multiselect(
        "Seleccionar columnas para mostrar",
        options=df_filtrado.columns.tolist(),
        default=['Nombre', 'Tipo Negocio', 'Prioridad', 'Calificación', 'Sitio Web', 'Teléfono']
    )
    
    if columnas:
        st.dataframe(
            df_filtrado[columnas],
            width='stretch',
            height=400
        )
    
    # Acciones rápidas
    st.markdown("---")
    st.subheader("🚀 Acciones Rápidas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Exportar a CSV", width='stretch'):
            csv = df_filtrado.to_csv(index=False)
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name=f"leads_filtrados_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📧 Enviar Campaña", width='stretch'):
            st.info("Esta función enviaría emails a los leads filtrados")
            # Aquí integrarías el automatizador de email
    
    with col3:
        if st.button("🔄 Sincronizar CRM", width='stretch'):
            st.info("Sincronizando con Airtable...")
            # Aquí integrarías el sincronizador

if __name__ == "__main__":
    # Para ejecutar: streamlit run 04_dashboard_streamlit.py
    main()