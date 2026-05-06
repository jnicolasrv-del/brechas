import streamlit as st
import pandas as pd

st.set_page_config(page_title="Monitor de Brechas", layout="centered")

st.title("📊 Monitor de Tasas y Brechas")

# 1. Historial
if 'historico' not in st.session_state:
    st.session_state.historico = [
        {"fecha": "27-mar", "bcv": 468.51, "banco": 570.00, "binance": 630.00},
        {"fecha": "30-abr", "bcv": 487.00, "banco": 611.00, "binance": 645.00}
    ]

# 2. Sidebar para datos
with st.sidebar:
    st.header("📝 Nuevos Precios")
    f = st.text_input("Fecha", "06-may")
    v_bcv = st.number_input("Tasa BCV", value=490.00, format="%.2f")
    v_ban = st.number_input("Tasa Banco", value=615.00, format="%.2f")
    v_bin = st.number_input("Tasa Binance", value=650.00, format="%.2f")
    if st.button("🚀 Actualizar"):
        st.session_state.historico.append({"fecha": f, "bcv": v_bcv, "banco": v_ban, "binance": v_bin})
        st.rerun()

df = pd.DataFrame(st.session_state.historico)
ultimo = st.session_state.historico[-1]

# --- CORRECCIÓN 1: MÉTRICAS DE BRECHAS ---
st.subheader(f"Análisis de Brechas (Fecha: {ultimo['fecha']})")
st.info(f"**Tasa BCV Referencia:** {ultimo['bcv']:.2f} Bs.")

c1, c2, c3 = st.columns(3)

# Cálculo de las 3 brechas
b_bin_bcv = ((ultimo['binance'] - ultimo['bcv']) / ultimo['bcv']) * 100
b_ban_bcv = ((ultimo['banco'] - ultimo['bcv']) / ultimo['bcv']) * 100
b_bin_ban = ((ultimo['binance'] - ultimo['banco']) / ultimo['banco']) * 100

c1.metric("Binance / BCV", f"{b_bin_bcv:.1f}%", f"{(ultimo['binance']-ultimo['bcv']):.2f} Bs")
c2.metric("Banco / BCV", f"{b_ban_bcv:.1f}%", f"{(ultimo['banco']-ultimo['bcv']):.2f} Bs")
c3.metric("Binance / Banco", f"{b_bin_ban:.1f}%", f"{(ultimo['binance']-ultimo['banco']):.2f} Bs")

# --- GRÁFICO ---
st.line_chart(df.set_index('fecha')[['bcv', 'banco', 'binance']])

# --- CORRECCIÓN 2: TABLA SIN ERRORES (ValueError) ---
with st.expander("Ver historial detallado"):
    df_h = df.copy()
    df_h['Brecha Bin/BCV %'] = ((df['binance'] - df['bcv']) / df['bcv']) * 100
    df_h['Brecha Ban/BCV %'] = ((df['banco'] - df['bcv']) / df['bcv']) * 100
    
    # Solo damos formato a las columnas numéricas para evitar el error con la columna 'fecha'
    columnas_numericas = ['bcv', 'banco', 'binance', 'Brecha Bin/BCV %', 'Brecha Ban/BCV %']
    st.dataframe(df_h.style.format(subset=columnas_numericas, formatter="{:.2f}"), use_container_width=True)
