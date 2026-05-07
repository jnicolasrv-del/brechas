import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Monitor de Brechas", layout="centered")

st.title("📊 Monitor de Tasas y Brechas")

# --- 1. HISTORIAL INICIAL ---
if 'historico' not in st.session_state:
    st.session_state.historico = [
        {"fecha": datetime.date(2026, 3, 27), "bcv": 468.51, "banco": 570.00, "binance": 630.00},
        {"fecha": datetime.date(2026, 4, 30), "bcv": 487.00, "banco": 611.00, "binance": 645.00}
    ]

# --- 2. SIDEBAR CON FORMATO DD/MM/AAAA ---
with st.sidebar:
    st.header("📝 Nuevos Precios")
    
    # El parámetro format="DD/MM/YYYY" cambia cómo lo ves en pantalla
    f_seleccionada = st.date_input(
        "Selecciona la Fecha", 
        datetime.date.today(),
        format="DD/MM/YYYY" 
    )
    
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

# --- 3. PROCESAMIENTO Y ORDENAMIENTO (CRUCIAL) ---
df = pd.DataFrame(st.session_state.historico)

# Convertimos a datetime por seguridad y ORDENAMOS
df['fecha'] = pd.to_datetime(df['fecha'])
df = df.sort_values(by='fecha') # Esto garantiza que Marzo < Abril < Mayo

# Creamos la etiqueta visual en formato DD-Mes
df['fecha_label'] = df['fecha'].dt.strftime('%d-%b').lower()

# Obtenemos el último registro ya ordenado
ultimo = df.iloc[-1]

# --- 4. MÉTRICAS DE BRECHAS ---
st.subheader(f"Análisis de Brechas (Fecha: {ultimo['fecha_label']})")
st.info(f"**Tasa BCV Referencia:** {ultimo['bcv']:.2f} Bs.")

c1, c2, c3 = st.columns(3)
b_bin_bcv = ((ultimo['binance'] - ultimo['bcv']) / ultimo['bcv']) * 100
b_ban_bcv = ((ultimo['banco'] - ultimo['bcv']) / ultimo['bcv']) * 100
b_bin_ban = ((ultimo['binance'] - ultimo['banco']) / ultimo['banco']) * 100

c1.metric("Binance / BCV", f"{b_bin_bcv:.1f}%", f"{(ultimo['binance']-ultimo['bcv']):.2f} Bs")
c2.metric("Banco / BCV", f"{b_ban_bcv:.1f}%", f"{(ultimo['banco']-ultimo['bcv']):.2f} Bs")
c3.metric("Binance / Banco", f"{b_bin_ban:.1f}%", f"{(ultimo['binance']-ultimo['banco']):.2f} Bs")

# --- 5. GRÁFICO ---
# Al usar st.line_chart con un dataframe ya ordenado y con la fecha como índice, se respeta el orden
df_grafico = df.set_index('fecha_label')[['bcv', 'banco', 'binance']]
st.line_chart(df_grafico)

# --- 6. TABLA DETALLADA ---
with st.expander("Ver historial detallado"):
    df_h = df.copy()
    # Formateamos la fecha de la tabla a DD/MM/YYYY
    df_h['fecha_tabla'] = df_h['fecha'].dt.strftime('%d/%m/%Y')
    
    df_h['Brecha Bin/BCV %'] = ((df_h['binance'] - df_h['bcv']) / df_h['bcv']) * 100
    df_h['Brecha Ban/BCV %'] = ((df_h['banco'] - df_h['bcv']) / df_h['bcv']) * 100
    
    df_mostrar = df_h[['fecha_tabla', 'bcv', 'banco', 'binance', 'Brecha Bin/BCV %', 'Brecha Ban/BCV %']]
    
    columnas_numericas = ['bcv', 'banco', 'binance', 'Brecha Bin/BCV %', 'Brecha Ban/BCV %']
    st.dataframe(df_mostrar.style.format(subset=columnas_numericas, formatter="{:.2f}"), use_container_width=True)
