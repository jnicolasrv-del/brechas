import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monitor de Brechas", layout="wide")
st.title("📊 Monitor de Tasas y Brechas")

# 1. Mantenemos el historial en la sesión
if 'historico' not in st.session_state:
    st.session_state.historico = [
        {"fecha": "27-mar", "bcv": 468.51, "banco": 570.00, "binance": 630.00},
        {"fecha": "30-abr", "bcv": 487.00, "banco": 611.00, "binance": 645.00}
    ]

# 2. Interfaz lateral para nuevos datos
with st.sidebar:
    st.header("Añadir nuevos precios")
    f = st.text_input("Fecha", "06-may")
    v_bcv = st.number_input("Tasa BCV", value=490.00, format="%.2f")
    v_ban = st.number_input("Tasa Banco", value=615.00, format="%.2f")
    v_bin = st.number_input("Tasa Binance", value=650.00, format="%.2f")
    if st.button("Actualizar Gráfico"):
        st.session_state.historico.append({"fecha": f, "bcv": v_bcv, "banco": v_ban, "binance": v_bin})
        st.rerun()

# 3. Lógica del gráfico REFORZADA (La que querías)
df = pd.DataFrame(st.session_state.historico)
# --- Nueva Visualización Optimizada para Móvil ---
st.divider() # Una línea sutil para separar

# Creamos un DataFrame pequeño para la gráfica interactiva
df_grafica = pd.DataFrame({
    'Referencia': ['BCV (Oficial)', 'Paralelo'],
    'Precio (Bs.)': [tasa_oficial, tasa_paralelo]
})

# Gráfica nativa de Streamlit (Se ajusta sola al ancho del celular)
st.bar_chart(df_grafica, x='Referencia', y='Precio (Bs.)', color="#007bff")

# Bloque de métricas (Esto se ve gigante y claro en el teléfono)
st.subheader("Análisis de Brecha")
m1, m2 = st.columns(2)
m1.metric(label="Diferencia en Bs.", value=f"{brecha_bs:.2f}")
m2.metric(label="Porcentaje", value=f"{brecha_porcentaje:.2f}%")

st.divider()
# Tabla al final
st.subheader("Historial de registros")
st.dataframe(df, use_container_width=True)
