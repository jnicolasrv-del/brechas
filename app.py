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
fig, ax = plt.subplots(figsize=(12, 7))

# Líneas principales
ax.plot(df['fecha'], df['bcv'], marker='o', label='BCV', color='#1f77b4', linewidth=3)
ax.plot(df['fecha'], df['banco'], marker='s', label='BANCO', color='#ff7f0e', linewidth=3)
ax.plot(df['fecha'], df['binance'], marker='^', label='BINANCE', color='#2ca02c', linewidth=3)

# Función para dibujar las brechas (Exactamente como el código original)
def dibujar_brecha(i, alto, bajo, color, desp_x, alineacion):
    porc = ((alto - bajo) / bajo) * 100
    medio = (alto + bajo) / 2
    ax.vlines(x=df['fecha'][i], ymin=bajo, ymax=alto, colors=color, linestyles='--', alpha=0.5)
    ax.text(i + desp_x, medio, f'{porc:.1f}%', color=color, fontweight='bold', va='center', ha=alineacion, fontsize=9)

for i in range(len(df)):
    # Brechas
    dibujar_brecha(i, df['binance'][i], df['bcv'][i], '#7f7f7f', -0.07, 'right')
    dibujar_brecha(i, df['banco'][i], df['bcv'][i], '#9467bd', 0.07, 'left')
    dibujar_brecha(i, df['binance'][i], df['banco'][i], '#d62728', 0.07, 'left')

    # Etiquetas de montos sobre los puntos
    for col in ['bcv', 'banco', 'binance']:
        ax.annotate(f'{df[col][i]:,.0f}', (df['fecha'][i], df[col][i]), 
                     textcoords="offset points", xytext=(0,10), ha='center', 
                     fontsize=9, fontweight='bold')

ax.grid(True, axis='y', linestyle=':', alpha=0.6)
ax.legend(loc='upper left')
plt.tight_layout()

# Mostrar en Streamlit
st.pyplot(fig)

# Tabla al final
st.subheader("Historial de registros")
st.dataframe(df, use_container_width=True)
