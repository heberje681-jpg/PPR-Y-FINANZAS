import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard Financiero", layout="wide", initial_sidebar_state="expanded")

# Inyección de CSS Personalizado (Estilo Minimalista/Fintech)
st.markdown("""
<style>
    :root {
        --primary-blue: #007AFF;
        --pure-white: #ffffff;
        --card-bg: #1c1c1e;
    }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="metric-container"] {
        background-color: var(--card-bg);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        border-top: 4px solid var(--pure-white);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 25px rgba(0, 122, 255, 0.2);
        border-top: 4px solid var(--primary-blue);
    }
    .stSlider > div > div > div > div {
        background-color: var(--pure-white) !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# FUNCIÓN PARA FORMATEAR NÚMEROS A "M" y "k"
# -------------------------------------------------------------------
def formatear_kpi(numero):
    if numero >= 1_000_000:
        formateado = f"${numero/1_000_000:.1f}M"
        return formateado.replace(".0M", "M") # Quita el .0 si es entero (Ej. 10.0M -> 10M)
    elif numero >= 1_000:
        formateado = f"${numero/1_000:.1f}k"
        return formateado.replace(".0k", "k")
    else:
        return f"${numero:,.0f}"

# -------------------------------------------------------------------
# LÓGICA DE NAVEGACIÓN
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Control Maestro")
    menu = st.radio("Selecciona el módulo:", ("📈 Simulador de Retiro", "💼 Presupuesto Mensual"))
    st.markdown("---")
    st.caption("Desarrollado en 🐍 Python")

# -------------------------------------------------------------------
# PÁGINA 1: SIMULADOR DE RETIRO
# -------------------------------------------------------------------
if menu == "📈 Simulador de Retiro":
    st.title("📈 Proyección de Patrimonio")
    st.markdown("Visualiza cómo crece tu dinero en el tiempo con el poder del interés compuesto.")

    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            capital_inicial = st.number_input("Capital Inicial ($)", min_value=0, value=0, step=5000)
        with c2:
            aportacion_mensual = st.number_input("Aportación Mensual ($)", min_value=1000, value=15500, step=500)
        with c3:
            anos = st.slider("Años invirtiendo", min_value=5, max_value=40, value=25)
        with c4:
            tasa_real = st.slider("Tasa Real Anual (%)", min_value=1.0, max_value=15.0, value=7.0, step=0.5)

    tasa_mensual = (tasa_real / 100) / 12
    meses_totales = anos * 12
    
    datos = []
    saldo_actual = capital_inicial
    total_aportado_acum = capital_inicial

    for mes in range(1, meses_totales + 1):
        saldo_actual = saldo_actual * (1 + tasa_mensual) + aportacion_mensual
        total_aportado_acum += aportacion_mensual
        if mes % 12 == 0:
            ano_actual = mes // 12
            datos.append({
                "Año": ano_actual,
                "Capital Propio": total_aportado_acum,
                "Rendimientos Generados": saldo_actual - total_aportado_acum,
                "Total": saldo_actual
            })
            
    df = pd.DataFrame(datos)
    patrimonio_final = df["Total"].iloc[-1]
    aportado_final = df["Capital Propio"].iloc[-1]
    ganancia_final = df["Rendimientos Generados"].iloc[-1]
    sueldo_pasivo_mensual = (patrimonio_final * 0.05) / 12

    # APLICAMOS LA NUEVA FUNCIÓN A LAS TARJETAS (KPIs)
    st.markdown("### Resumen de tu Retiro")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Aportado", formatear_kpi(aportado_final))
    k2.metric("Rendimientos", formatear_kpi(ganancia_final))
    k3.metric("Patrimonio Final", formatear_kpi(patrimonio_final))
    k4.metric("Sueldo Mensual Libre", formatear_kpi(sueldo_pasivo_mensual))

    st.markdown("<br>", unsafe_allow_html=True)
    fig = px.area(df, x="Año", y=["Capital Propio", "Rendimientos Generados"], color_discrete_sequence=["#E5E5EA", "#007AFF"])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------------
# PÁGINA 2: CONTROL DE PRESUPUESTO
# -------------------------------------------------------------------
elif menu == "💼 Presupuesto Mensual":
    st.title("💼 Presupuesto Base Cero")
    st.markdown("Controla exactamente a dónde va cada peso de tus ingresos combinados.")

    # 1. Ingreso Total
    ingreso_total = st.number_input("Ingreso Total Disponible del Mes ($)", min_value=1000.0, value=82500.0, step=1000.0)

    # 2. Desglose de Costos Fijos
    st.markdown("### 1. Tus Costos Fijos Exactos")
    with st.expander("Haz clic para detallar los gastos fijos de este mes", expanded=True):
        g1, g2, g3 = st.columns(3)
        with g1:
            renta = st.number_input("🏠 Hipoteca / Renta ($)", value=12000.0, step=500.0)
            servicios = st.number_input("⚡ Servicios (Luz, Internet, etc.) ($)", value=2500.0, step=100.0)
        with g2:
            auto = st.number_input("🚗 Autos (Mensualidad y Gasolina) ($)", value=6000.0, step=500.0)
            supermercado = st.number_input("🛒 Supermercado / Comida ($)", value=8000.0, step=500.0)
        with g3:
            seguros = st.number_input("🛡️ Seguros (Médico, Auto) ($)", value=2000.0, step=100.0)
            otros = st.number_input("📦 Otros fijos ($)", value=1500.0, step=100.0)

    # Cálculos Matemáticos de Fijos
    total_fijos = renta + servicios + auto + supermercado + seguros + otros
    pct_fijos = (total_fijos / ingreso_total) * 100
    dinero_restante = ingreso_total - total_fijos
    pct_restante = 100.0 - pct_fijos

    st.markdown("### 2. Asignación del Restante")
    
    # Validaciones para evitar que gasten más de lo que ganan
    if dinero_restante < 0:
        st.error(f"⚠️ Peligro: Tus gastos fijos (${total_fijos:,.2f}) superan tu ingreso. Estás perdiendo dinero.")
    else:
        st.info(f"Tus gastos fijos suman **${total_fijos:,.2f}** y consumen el **{pct_fijos:.1f}%** de tu sueldo. Tienes un **{pct_restante:.1f}%** libre para Inversión y Estilo de Vida.")
        
        col_sliders, col_grafica = st.columns([1, 1])

        with col_sliders:
            st.write(f"Distribuye el {pct_restante:.1f}% sobrante:")
            # El slider tiene como máximo el porcentaje restante, calculando en automático el estilo de vida
            pct_inversion = st.slider("📈 Porcentaje para el Retiro (S&P 500) %", min_value=0.0, max_value=float(pct_restante), value=float(pct_restante)*0.5, step=1.0)
            pct_estilo = pct_restante - pct_inversion
            
            st.write(f"✈️ Estilo de Vida se ajusta automáticamente a: **{pct_estilo:.1f}%**")

        monto_inversion = ingreso_total * (pct_inversion / 100)
        monto_estilo = ingreso_total * (pct_estilo / 100)

        with col_grafica:
            labels = ['Gastos Fijos', 'Inversión', 'Estilo de Vida']
            values = [total_fijos, monto_inversion, monto_estilo]
            colores = ['#FFFFFF', '#007AFF', '#3A3A3C']
            
            fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=colores, line=dict(color='#000000', width=2)))])
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white", margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Resumen Final (Pesos Exactos)")
        t1, t2, t3 = st.columns(3)
        t1.metric("🏠 Para Costos Fijos", formatear_kpi(total_fijos))
        t2.metric("📈 Para el Broker (Retiro)", formatear_kpi(monto_inversion))
        t3.metric("✈️ Para Disfrutar", formatear_kpi(monto_estilo))
