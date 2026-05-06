import streamlit as st
import pandas as pd

# Configuración para que el celular no se vea "apretado"
st.set_page_config(page_title="Monitor de Brechas", layout="centered")

st.title("📊 Monitor de Tasas y Brechas")

# 1. Mantenemos el historial en la sesión
if 'historico' not in st.session_state:
    st.session_state.historico = [
        {"fecha": "27-mar", "bcv": 468.51, "banco": 570.00, "binance": 630.00},
        {"fecha": "30-abr", "bcv": 487.00, "banco": 611.00, "binance": 645.00}
    ]

# 2. Interfaz lateral (En móvil se esconde en un menú arriba a la izquierda)
with st.sidebar:
    st.header("📝 Añadir nuevos precios")
    f = st.text_input("Fecha", "06-may")
    v_bcv = st.number_input("Tasa BCV", value=490.00, format="%.2f")
    v_ban = st.number_input("Tasa Banco", value=615.00, format="%.2f")
    v_bin = st.number_input("Tasa Binance", value=650.00, format="%.2f")
    if st.button("🚀 Actualizar y Graficar"):
        st.session_state.historico.append({"fecha": f, "bcv": v_bcv, "banco": v_ban, "binance": v_bin})
        st.rerun()

# Preparar datos
df = pd.DataFrame(st.session_state.historico)

# --- SECCIÓN DE MÉTRICAS (Lo que mejor se ve en el móvil) ---
st.subheader("Último Registro")
ultimo = st.session_state.historico[-1]
col1, col2, col3 = st.columns(3)

# Calculamos brechas del último registro para mostrar en grande
brecha_bin_bcv = ((ultimo['binance'] - ultimo['bcv']) / ultimo['bcv']) * 100
brecha_ban_bcv = ((ultimo['banco'] - ultimo['bcv']) / ultimo['bcv']) * 100

col1.metric("BCV", f"{ultimo['bcv']:.2f}")
col2.metric("Brecha Bin/BCV", f"{brecha_bin_bcv:.1f}%", delta=f"{(ultimo['binance']-ultimo['bcv']):.2f} Bs")
col3.metric("Brecha Ban/BCV", f"{brecha_ban_bcv:.1f}%", delta=f"{(ultimo['banco']-ultimo['bcv']):.2f} Bs")

# --- GRÁFICO RESPONSIVO (Sustituye a Matplotlib) ---
st.subheader("Evolución de Tasas")
# Creamos un formato que st.line_chart entienda mejor
df_plot = df.set_index('fecha')[['bcv', 'banco', 'binance']]
st.line_chart(df_plot)

# --- ANÁLISIS DE BRECHAS DETALLADO ---
with st.expander("Ver detalle de brechas históricas"):
    df_brechas = df.copy()
    df_brechas['Brecha Bin/BCV %'] = ((df['binance'] - df['bcv']) / df['bcv']) * 100
    df_brechas['Brecha Ban/BCV %'] = ((df['banco'] - df['bcv']) / df['bcv']) * 100
    df_brechas['Brecha Bin/Ban %'] = ((df['binance'] - df['banco']) / df['banco']) * 100
    
    # Formateamos para que la tabla sea legible
    st.dataframe(df_brechas.style.format("{:.2f}"), use_container_width=True)

st.info("💡 En el celular, puedes girar la pantalla horizontalmente para ver mejor el historial.")
