import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Monitor de Brechas", layout="centered")

st.title("📊 Monitor de Tasas y Brechas")

# --- 1. HISTORIAL INICIAL ---
# Nota: Ahora guardamos la fecha como un objeto de fecha real para que Python sepa ordenarlo
if 'historico' not in st.session_state:
    st.session_state.historico = [
        {"fecha": datetime.date(2026, 3, 27), "bcv": 468.51, "banco": 570.00, "binance": 630.00},
        {"fecha": datetime.date(2026, 4, 30), "bcv": 487.00, "banco": 611.00, "binance": 645.00}
    ]

# --- 2. SIDEBAR PARA DATOS (IMPLEMENTACIÓN PUNTO 2) ---
with st.sidebar:
    st.header("📝 Nuevos Precios")
    
    # Cambiamos st.text_input por st.date_input para "exigir" el formato correcto
    f_seleccionada = st.date_input("Selecciona la Fecha", datetime.date(2026, 5, 7))
    
    v_bcv = st.number_input("Tasa BCV", value=490.00, format="%.2f")
    v_ban = st.number_input("Tasa Banco", value=615.00, format="%.2f")
    v_bin = st.number_input("Tasa Binance", value=650.00, format="%.2f")
    
    if st.button("🚀 Actualizar"):
        st.session_state.historico.append({
            "fecha": f_seleccionada, 
            "bcv": v_bcv, 
            "banco": v_ban, 
            "binance": v_bin
        })
        st.rerun()

# --- 3. PROCESAMIENTO DE DATOS (IMPLEMENTACIÓN PUNTO 1) ---
df = pd.DataFrame(st.session_state.historico)

# IMPORTANTE: Ordenamos por fecha real antes de graficar
df = df.sort_values('fecha')

# Creamos una columna de texto solo para mostrar en las etiquetas del gráfico/tabla (ej: "07-may")
df['fecha_texto'] = df['fecha'].apply(lambda x: x.strftime('%d-%b').lower())

ultimo = df.iloc[-1] # Tomamos el último según el orden cronológico

# --- 4. MÉTRICAS DE BRECHAS ---
st.subheader(f"Análisis de Brechas (Fecha: {ultimo['fecha_texto']})")
st.info(f"**Tasa BCV Referencia:** {ultimo['bcv']:.2f} Bs.")

c1, c2, c3 = st.columns(3)

b_bin_bcv = ((ultimo['binance'] - ultimo['bcv']) / ultimo['bcv']) * 100
b_ban_bcv = ((ultimo['banco'] - ultimo['bcv']) / ultimo['bcv']) * 100
b_bin_ban = ((ultimo['binance'] - ultimo['banco']) / ultimo['banco']) * 100

c1.metric("Binance / BCV", f"{b_bin_bcv:.1f}%", f"{(ultimo['binance']-ultimo['bcv']):.2f} Bs")
c2.metric("Banco / BCV", f"{b_ban_bcv:.1f}%", f"{(ultimo['banco']-ultimo['bcv']):.2f} Bs")
c3.metric("Binance / Banco", f"{b_bin_ban:.1f}%", f"{(ultimo['binance']-ultimo['banco']):.2f} Bs")

# --- 5. GRÁFICO (ORDENADO CRONOLÓGICAMENTE) ---
# Usamos 'fecha_texto' como índice para que el eje X sea legible pero respetando el orden del DF
st.line_chart(df.set_index('fecha_texto')[['bcv', 'banco', 'binance']])

# --- 6. TABLA DETALLADA ---
with st.expander("Ver historial detallado"):
    df_h = df.copy()
    df_h['Brecha Bin/BCV %'] = ((df['binance'] - df['bcv']) / df['bcv']) * 100
    df_h['Brecha Ban/BCV %'] = ((df['banco'] - df['bcv']) / df['bcv']) * 100
    
    # Quitamos la columna de fecha 'cruda' para mostrar solo la formateada
    df_mostrar = df_h[['fecha_texto', 'bcv', 'banco', 'binance', 'Brecha Bin/BCV %', 'Brecha Ban/BCV %']]
    
    columnas_numericas = ['bcv', 'banco', 'binance', 'Brecha Bin/BCV %', 'Brecha Ban/BCV %']
    st.dataframe(df_mostrar.style.format(subset=columnas_numericas, formatter="{:.2f}"), use_container_width=True)
