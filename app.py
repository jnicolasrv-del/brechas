import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Monitor de Brechas", layout="centered")
st.title("📊 Monitor de Tasas y Brechas")

# --- FUNCIÓN PARA CARGAR DATOS ---
def cargar_datos():
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df.sort_values('fecha')
    return pd.DataFrame(columns=['fecha', 'bcv', 'banco', 'binance'])

# --- LÓGICA DE ACTUALIZACIÓN ---
df = cargar_datos()

with st.sidebar:
    st.header("📝 Nuevos Precios")
    f_input = st.date_input("Fecha", datetime.date.today(), format="DD/MM/YYYY")
    v_bcv = st.number_input("Tasa BCV", value=498.00, format="%.2f")
    v_ban = st.number_input("Tasa Banco", value=611.00, format="%.2f")
    v_bin = st.number_input("Tasa Binance", value=660.00, format="%.2f")
    
    if st.button("🚀 Actualizar"):
        # Crear nueva fila
        nueva_fila = pd.DataFrame({
            'fecha': [pd.to_datetime(f_input)],
            'bcv': [v_bcv],
            'banco': [v_ban],
            'binance': [v_bin]
        })
        df = pd.concat([df, nueva_fila]).sort_values('fecha')
        df.to_csv('data.csv', index=False)
        st.rerun()

# --- VISUALIZACIÓN ---
if not df.empty:
    df['label'] = df['fecha'].dt.strftime('%d-%b').str.lower()
    ultimo = df.iloc[-1]

    st.subheader(f"Análisis (Fecha: {ultimo['label']})")
    
    # Métricas
    c1, c2, c3 = st.columns(3)
    b_bin_bcv = ((ultimo['binance'] - ultimo['bcv']) / ultimo['bcv']) * 100
    b_ban_bcv = ((ultimo['banco'] - ultimo['bcv']) / ultimo['bcv']) * 100
    b_bin_ban = ((ultimo['binance'] - ultimo['banco']) / ultimo['banco']) * 100

    c1.metric("Binance / BCV", f"{b_bin_bcv:.1f}%")
    c2.metric("Banco / BCV", f"{b_ban_bcv:.1f}%")
    c3.metric("Binance / Banco", f"{b_bin_ban:.1f}%")

    # GRÁFICO: Aquí forzamos que el orden sea cronológico usando el índice de tiempo
    st.line_chart(df.set_index('label')[['bcv', 'banco', 'binance']])

    with st.expander("Ver historial detallado"):
        df_h = df.copy()
        df_h['fecha'] = df_h['fecha'].dt.strftime('%d/%m/%Y')
        st.dataframe(df_h[['fecha', 'bcv', 'banco', 'binance']], use_container_width=True)
