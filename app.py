import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Monitor de Brechas", layout="centered")

st.title("📊 Monitor de Tasas y Brechas")

# --- 1. FUNCIÓN DE CARGA Y LIMPIEZA TOTAL ---
def cargar_datos():
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
        # Forzamos la conversión a fecha real para que el orden sea cronológico
        df['fecha'] = pd.to_datetime(df['fecha'])
        # Ordenamos de pasado a futuro antes de cualquier otra cosa
        return df.sort_values(by='fecha')
    else:
        # Estructura inicial si el archivo no existe
        return pd.DataFrame(columns=['fecha', 'bcv', 'banco', 'binance'])

# --- 2. PROCESAMIENTO DE DATOS ---
df = cargar_datos()

# --- 3. PANEL LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("📝 Nuevos Precios")
    f_input = st.date_input("Selecciona la Fecha", datetime.date.today(), format="DD/MM/YYYY")
    v_bcv = st.number_input("Tasa BCV", value=498.00, format="%.2f")
    v_ban = st.number_input("Tasa Banco", value=611.00, format="%.2f")
    v_bin = st.number_input("Tasa Binance", value=660.00, format="%.2f")
    
    if st.button("🚀 Actualizar y Guardar"):
        # Creamos el nuevo registro
        nueva_fila = pd.DataFrame({
            'fecha': [pd.to_datetime(f_input)],
            'bcv': [v_bcv],
            'banco': [v_ban],
            'binance': [v_bin]
        })
        # Combinamos, ordenamos y guardamos permanentemente en el CSV
        df_final = pd.concat([df, nueva_fila]).sort_values(by='fecha')
        df_final.to_csv('data.csv', index=False)
        st.rerun()

# --- 4. VISUALIZACIÓN PRINCIPAL ---
if not df.empty:
    # Creamos la etiqueta visual DESPUÉS de ordenar por fecha real
    df['fecha_label'] = df['fecha'].dt.strftime('%d-%b').str.lower()
    ultimo = df.iloc[-1]

    # Métricas de cabecera
    st.subheader(f"Análisis de Brechas (Fecha: {ultimo['fecha_label']})")
    st.info(f"**Tasa BCV Referencia:** {ultimo['bcv']:.2f} Bs.")

    c1, c2, c3 = st.columns(3)
    
    # Cálculos de brechas para métricas
    b_bin_bcv = ((ultimo['binance'] - ultimo['bcv']) / ultimo['bcv']) * 100
    b_ban_bcv = ((ultimo['banco'] - ultimo['bcv']) / ultimo['bcv']) * 100
    b_bin_ban = ((ultimo['binance'] - ultimo['banco']) / ultimo['banco']) * 100

    c1.metric("Binance / BCV", f"{b_bin_bcv:.1f}%", f"{(ultimo['binance']-ultimo['bcv']):.2f} Bs")
    c2.metric("Banco / BCV", f"{b_ban_bcv:.1f}%", f"{(ultimo['banco']-ultimo['bcv']):.2f} Bs")
    c3.metric("Binance / Banco", f"{b_bin_ban:.1f}%", f"{(ultimo['binance']-ultimo['banco']):.2f} Bs")

    # Gráfico de líneas (usando el índice ordenado)
    st.line_chart(df.set_index('fecha_label')[['bcv', 'banco', 'binance']])

    # --- 5. TABLA DETALLADA CON TODAS LAS BRECHAS ---
    with st.expander("Ver historial detallado"):
        df_h = df.copy()
        
        # Calculamos todas las columnas de brecha para el historial
        df_h['Brecha Bin/BCV %'] = ((df_h['binance'] - df_h['bcv']) / df_h['bcv']) * 100
        df_h['Brecha Ban/BCV %'] = ((df_h['banco'] - df_h['bcv']) / df_h['bcv']) * 100
        df_h['Brecha Bin/Ban %'] = ((df_h['binance'] - df_h['banco']) / df_h['banco']) * 100
        
        # Formato de fecha para la tabla
        df_h['fecha_tabla'] = df_h['fecha'].dt.strftime('%d/%m/%Y')
        
        # Seleccionamos y ordenamos las columnas
        columnas_finales = [
            'fecha_tabla', 'bcv', 'banco', 'binance', 
            'Brecha Bin/BCV %', 'Brecha Ban/BCV %', 'Brecha Bin/Ban %'
        ]
        
        # Aplicamos el estilo numérico
        st.dataframe(
            df_h[columnas_finales].style.format({
                'bcv': '{:.2f}', 'banco': '{:.2f}', 'binance': '{:.2f}',
                'Brecha Bin/BCV %': '{:.2f}%', 
                'Brecha Ban/BCV %': '{:.2f}%', 
                'Brecha Bin/Ban %': '{:.2f}%'
            }), 
            use_container_width=True
        )
else:
    st.warning("El archivo data.csv está vacío o no existe. Agrega datos en el panel lateral.")
