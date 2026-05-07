import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Monitor de Brechas", layout="centered")
st.title("📊 Monitor de Tasas y Brechas")

# --- 1. CARGA DE DATOS ---
def cargar_datos():
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
        # CRUCIAL: Convertir a fecha real y ORDENAR por ese valor numérico
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df.sort_values('fecha')
    return pd.DataFrame(columns=['fecha', 'bcv', 'banco', 'binance'])

df = cargar_datos()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("📝 Nuevos Precios")
    f_input = st.date_input("Fecha", datetime.date.today(), format="DD/MM/YYYY")
    v_bcv = st.number_input("Tasa BCV", value=498.00, format="%.2f")
    v_ban = st.number_input("Tasa Banco", value=611.00, format="%.2f")
    v_bin = st.number_input("Tasa Binance", value=660.00, format="%.2f")
    
    if st.button("🚀 Actualizar y Guardar"):
        nueva_fila = pd.DataFrame({
            'fecha': [pd.to_datetime(f_input)],
            'bcv': [v_bcv],
            'banco': [v_ban],
            'binance': [v_bin]
        })
        df_final = pd.concat([df, nueva_fila]).sort_values('fecha')
        df_final.to_csv('data.csv', index=False)
        st.rerun()

# --- 3. VISUALIZACIÓN ---
if not df.empty:
    # Creamos la etiqueta SOLO para mostrarla, no para ordenar
    df['fecha_label'] = df['fecha'].dt.strftime('%d-%b').str.lower()
    ultimo = df.iloc[-1]

    st.subheader(f"Análisis (Fecha: {ultimo['fecha_label']})")
    
    # Métricas
    c1, c2, c3 = st.columns(3)
    b_bin_bcv = ((ultimo['binance'] - ultimo['bcv']) / ultimo['bcv']) * 100
    b_ban_bcv = ((ultimo['banco'] - ultimo['bcv']) / ultimo['bcv']) * 100
    b_bin_ban = ((ultimo['binance'] - ultimo['banco']) / ultimo['banco']) * 100

    c1.metric("Binance / BCV", f"{b_bin_bcv:.1f}%")
    c2.metric("Banco / BCV", f"{b_ban_bcv:.1f}%")
    c3.metric("Binance / Banco", f"{b_bin_ban:.1f}%")

    # --- EL CAMBIO DEFINITIVO PARA EL GRÁFICO ---
    # Usamos la FECHA REAL como índice. Streamlit detecta que es tiempo y 
    # coloca marzo, abril y mayo en ese orden exacto.
    df_grafico = df.copy()
    df_grafico = df_grafico.set_index('fecha')
    st.line_chart(df_grafico[['bcv', 'banco', 'binance']])

    # --- TABLA DETALLADA (CON PORCENTAJES) ---
    with st.expander("Ver historial detallado"):
        df_h = df.copy()
        df_h['Brecha Bin/BCV %'] = ((df_h['binance'] - df_h['bcv']) / df_h['bcv']) * 100
        df_h['Brecha Ban/BCV %'] = ((df_h['banco'] - df_h['bcv']) / df_h['bcv']) * 100
        df_h['Brecha Bin/Ban %'] = ((df_h['binance'] - df_h['banco']) / df_h['banco']) * 100
        
        df_h['fecha'] = df_h['fecha'].dt.strftime('%d/%m/%Y')
        
        columnas = ['fecha', 'bcv', 'banco', 'binance', 'Brecha Bin/BCV %', 'Brecha Ban/BCV %', 'Brecha Bin/Ban %']
        formatos = {c: '{:.2f}' for c in columnas if c != 'fecha'}
        # Añadir el símbolo % a los formatos de las brechas
        for c in ['Brecha Bin/BCV %', 'Brecha Ban/BCV %', 'Brecha Bin/Ban %']:
            formatos[c] = '{:.2f}%'

        st.dataframe(df_h[columnas].style.format(formatos), use_container_width=True)
