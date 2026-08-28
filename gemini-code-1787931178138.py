import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración inicial de la página (Debe ser la primera línea)
st.set_page_config(page_title="Dashboard Financiero", layout="wide", initial_sidebar_state="expanded")

# Inyección de CSS Personalizado (Magia UI/UX)
st.markdown("""
<style>
    /* Variables de color: Acentos en verde oscuro y fondos oscuros elegantes */
    :root {
        --dark-green: #0a4a27;
        --light-green: #148043;
        --card-bg: #1e1e1e;
    }

    /* Estilo global y tipografía más limpia */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Tarjetas de métricas con bordes redondeados, sombras y efecto Hover */
    div[data-testid="metric-container"] {
        background-color: var(--card-bg);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        border-left: 6px solid var(--dark-green);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 20px rgba(20, 128, 67, 0.3);
    }

    /* Estilo para los Sliders (Acento verde) */
    .stSlider > div > div > div > div {
        background-color: var(--light-green) !important;
    }

    /* Botones más curvos y con hover */
    div.stButton > button {
        border-radius: 25px;
        background-color: var(--dark-green);
        color: white;
        font-weight: 600;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(20, 128, 67, 0.4);
        background-color: var(--light-green);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# LÓGICA DE NAVEGACIÓN
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Control Maestro")
    menu = st.radio(
        "Selecciona el módulo:",
        ("📈 Simulador de Retiro", "💼 Presupuesto Mensual")
    )
    st.markdown("---")
    st.caption("Hecho con 🐍 Python y Streamlit")

# -------------------------------------------------------------------
# PÁGINA 1: SIMULADOR DE RETIRO
# -------------------------------------------------------------------
if menu == "📈 Simulador de Retiro":
    st.title("📈 Proyección de Patrimonio e Interés Compuesto")
    st.markdown("Visualiza cómo crece tu dinero en el tiempo con aportaciones recurrentes.")

    # Fila de Controles (Sliders) en un contenedor
    with st.container():
        st.subheader("Ajustes del Modelo")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            capital_inicial = st.number_input("Capital Inicial ($)", min_value=0, value=0, step=5000)
        with c2:
            aportacion_mensual = st.number_input("Aportación Mensual ($)", min_value=1000, value=15500, step=500)
        with c3:
            anos = st.slider("Años invirtiendo", min_value=5, max_value=40, value=25)
        with c4:
            tasa_real = st.slider("Tasa Real Anual (%)", min_value=1.0, max_value=15.0, value=7.0, step=0.5)

    # Motor de Cálculo del Interés Compuesto
    tasa_mensual = (tasa_real / 100) / 12
    meses_totales = anos * 12
    
    datos = []
    saldo_actual = capital_inicial
    total_aportado_acum = capital_inicial

    for mes in range(1, meses_totales + 1):
        saldo_actual = saldo_actual * (1 + tasa_mensual) + aportacion_mensual
        total_aportado_acum += aportacion_mensual
        if mes % 12 == 0:  # Guardar datos anuales para la gráfica
            ano_actual = mes // 12
            rendimiento_ganado = saldo_actual - total_aportado_acum
            datos.append({
                "Año": ano_actual,
                "Aportado (Tus bolsillos)": total_aportado_acum,
                "Interés Compuesto (Ganancia)": rendimiento_ganado,
                "Total": saldo_actual
            })
            
    df = pd.DataFrame(datos)
    patrimonio_final = df["Total"].iloc[-1]
    aportado_final = df["Aportado (Tus bolsillos)"].iloc[-1]
    ganancia_final = df["Interés Compuesto (Ganancia)"].iloc[-1]
    
    # Cálculo del retiro mensual seguro (5% anual recomendado para dejar herencia o 4% conservador)
    sueldo_pasivo_mensual = (patrimonio_final * 0.05) / 12

    # Fila de KPIs (Tarjetas)
    st.markdown("### Resumen a 25 años")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Aportado", f"${aportado_final:,.2f}")
    k2.metric("Ganancias de Inversión", f"${ganancia_final:,.2f}")
    k3.metric("Patrimonio Final", f"${patrimonio_final:,.2f}")
    k4.metric("Sueldo Mensual (5%)", f"${sueldo_pasivo_mensual:,.2f}", "+ Libertad")

    # Gráfico de Área Apilada (Estilo profesional)
    st.markdown("<br>", unsafe_allow_html=True)
    fig = px.area(
        df, 
        x="Año", 
        y=["Aportado (Tus bolsillos)", "Interés Compuesto (Ganancia)"],
        color_discrete_sequence=["#1f77b4", "#148043"], # Azul y Verde oscuro
        title="Crecimiento del Portafolio"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        legend_title_text="",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------------
# PÁGINA 2: CONTROL DE PRESUPUESTO
# -------------------------------------------------------------------
elif menu == "💼 Presupuesto Mensual":
    st.title("💼 Asignación de Presupuesto Base Cero")
    st.markdown("Divide tus ingresos combinados (Sueldo + Negocio) de forma exacta.")

    # Ingreso Total en grande
    st.markdown("### Ingreso del Mes")
    ingreso_total = st.number_input("Ingreso Total Disponible ($)", min_value=0.0, value=82500.0, step=1000.0)

    st.markdown("### Distribución Porcentual")
    col_sliders, col_grafica = st.columns([1, 1])

    with col_sliders:
        st.write("Ajusta los sliders. La suma debe ser exactamente 100%.")
        pct_fijos = st.slider("Gastos Fijos (Casa, Autos, Servicios) %", 0, 100, 50)
        pct_inversion = st.slider("Retiro e Inversiones (S&P 500) %", 0, 100, 25)
        pct_estilo = st.slider("Estilo de Vida (Viajes, Salidas) %", 0, 100, 25)
        
        suma_pct = pct_fijos + pct_inversion + pct_estilo
        
        if suma_pct == 100:
            st.success("✅ ¡Perfecto! Presupuesto cuadrado al 100%.")
        elif suma_pct > 100:
            st.error(f"⚠️ Te pasaste por {suma_pct - 100}%. Reduce alguna categoría.")
        else:
            st.warning(f"⚠️ Te falta asignar {100 - suma_pct}%. Aprovecha al máximo tu dinero.")

    # Cálculos en pesos
    monto_fijos = ingreso_total * (pct_fijos / 100)
    monto_inversion = ingreso_total * (pct_inversion / 100)
    monto_estilo = ingreso_total * (pct_estilo / 100)

    with col_grafica:
        # Gráfico de Dona para los porcentajes
        labels = ['Gastos Fijos', 'Inversión', 'Estilo de Vida']
        values = [monto_fijos, monto_inversion, monto_estilo]
        colores = ['#4A90E2', '#148043', '#F5A623'] # Azul, Verde Oscuro, Naranja
        
        fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=colores))])
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Tarjetas de Sobres Finales
    st.markdown("### Tus Transferencias del Mes")
    t1, t2, t3 = st.columns(3)
    t1.metric("🏠 Gastos Fijos", f"${monto_fijos:,.2f}")
    t2.metric("📈 Inversión Segura", f"${monto_inversion:,.2f}")
    t3.metric("✈️ Estilo de Vida", f"${monto_estilo:,.2f}")