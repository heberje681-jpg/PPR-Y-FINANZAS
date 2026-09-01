import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard Financiero", layout="wide", initial_sidebar_state="expanded")

# Inyección de CSS Avanzado (Modo Desarrollador Pro)
st.markdown("""
<style>
    :root {
        --primary-blue: #007AFF;
        --neon-blue: #00d2ff;
        --pure-white: #ffffff;
        --card-bg: #1c1c1e;
        --bg-color: #121212;
    }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    div[data-testid="stThumbValue"] {
        background-color: var(--primary-blue) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.5);
    }
    div[data-testid="metric-container"] {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        border-left: 5px solid var(--primary-blue); 
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 122, 255, 0.25);
        border-left: 5px solid var(--neon-blue); 
    }
    header {visibility: hidden;}
    hr { border-color: #333333 !important; }
    .disclaimer-box {
        background-color: #2c2c2e;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid var(--pure-white);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# FUNCIÓN PARA FORMATEAR NÚMEROS A "M" y "k"
# -------------------------------------------------------------------
def formatear_kpi(numero):
    if numero >= 1_000_000:
        formateado = f"${numero/1_000_000:.1f}M"
        return formateado.replace(".0M", "M")
    elif numero >= 1_000:
        formateado = f"${numero/1_000:.1f}k"
        return formateado.replace(".0k", "k")
    else:
        return f"${numero:,.0f}"

# -------------------------------------------------------------------
# LÓGICA DE NAVEGACIÓN
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Centro de Control")
    menu = st.radio("Selecciona el módulo:", ("📈 Simulador de Retiro", "💼 Presupuesto Mensual"))
    st.markdown("---")
    st.caption("Desarrollado por **Heber Orduño**")

# -------------------------------------------------------------------
# PÁGINA 1: SIMULADOR DE RETIRO (Se mantiene igual)
# -------------------------------------------------------------------
if menu == "📈 Simulador de Retiro":
    st.title("📈 Proyección de Patrimonio")
    st.markdown("Visualiza cómo crece tu dinero en el tiempo con el poder del interés compuesto.")

    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            capital_inicial = st.number_input("Capital Inicial ($)", min_value=0, value=0, step=5000)
        with c2:
            aportacion_mensual = st.number_input("Aportación Mensual ($)", min_value=1000, value=12300, step=500)
        with c3:
            anos = st.slider("Años invirtiendo", min_value=5, max_value=40, value=31)
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
    st.markdown("### Resumen de tu Retiro")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Aportado", formatear_kpi(df["Capital Propio"].iloc[-1]))
    k2.metric("Rendimientos", formatear_kpi(df["Rendimientos Generados"].iloc[-1]))
    k3.metric("Patrimonio Final", formatear_kpi(df["Total"].iloc[-1]))
    k4.metric("Sueldo Mensual Libre", formatear_kpi((df["Total"].iloc[-1] * 0.05) / 12))

    fig = px.area(df, x="Año", y=["Capital Propio", "Rendimientos Generados"], color_discrete_sequence=["#E5E5EA", "#007AFF"])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white", hovermode="x unified", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------------
# PÁGINA 2: CONTROL DE PRESUPUESTO (ACTUALIZADA)
# -------------------------------------------------------------------
elif menu == "💼 Presupuesto Mensual":
    st.title("💼 Presupuesto Base Cero")
    st.markdown("Controla exactamente a dónde va cada peso de tus ingresos combinados.")

    # GUÍA FINANCIERA (DISCLAIMER)
    st.markdown("""
    <div class="disclaimer-box">
        <b>💡 Tip Financiero: La Regla 50/30/20 (Adaptada)</b><br>
        Lo ideal para unas finanzas blindadas es apuntar a: 
        <span style="color:var(--pure-white);"><b>50% Gastos Fijos</b></span> | 
        <span style="color:#007AFF;"><b>20% Inversión (Retiro)</b></span> | 
        <span style="color:#00d2ff;"><b>10% Liquidez (Ahorro corto plazo)</b></span> | 
        <span style="color:#8E8E93;"><b>20% Estilo de Vida</b></span>.
    </div>
    """, unsafe_allow_html=True)

    ingreso_total = st.number_input("Ingreso Total Disponible del Mes ($)", min_value=1000.0, value=82500.0, step=1000.0)

    st.markdown("### 1. Tus Costos Fijos Exactos")
    with st.expander("Desglosar gastos fijos mensuales", expanded=False):
        g1, g2, g3 = st.columns(3)
        with g1:
            renta = st.number_input("🏠 Hipoteca / Renta ($)", value=12000.0, step=500.0)
            servicios = st.number_input("⚡ Servicios (Luz, Internet) ($)", value=2500.0, step=100.0)
        with g2:
            auto = st.number_input("🚗 Autos (Pago y Gasolina) ($)", value=6000.0, step=500.0)
            supermercado = st.number_input("🛒 Supermercado ($)", value=8000.0, step=500.0)
        with g3:
            seguros = st.number_input("🛡️ Seguros ($)", value=2000.0, step=100.0)
            otros = st.number_input("📦 Otros fijos ($)", value=1500.0, step=100.0)

    total_fijos = renta + servicios + auto + supermercado + seguros + otros
    pct_fijos = (total_fijos / ingreso_total) * 100
    dinero_restante = ingreso_total - total_fijos
    pct_restante = 100.0 - pct_fijos

    st.markdown("### 2. Asignación del Restante (Inversión, Liquidez y Estilo)")
    
    if dinero_restante < 0:
        st.error(f"⚠️ Peligro: Tus gastos fijos (${total_fijos:,.2f}) superan tu ingreso.")
    else:
        st.info(f"Tus gastos fijos consumen el **{pct_fijos:.1f}%** de tu sueldo. Tienes un **{pct_restante:.1f}%** libre.")
        
        col_sliders, col_grafica = st.columns([1, 1])

        with col_sliders:
            st.write(f"Distribuye el {pct_restante:.1f}% sobrante:")
            
            # SLIDER 1: Inversión a largo plazo (Retiro)
            pct_inversion = st.slider("📈 Inversión Largo Plazo (Retiro) %", min_value=0.0, max_value=float(pct_restante), value=float(pct_restante)*0.4, step=1.0)
            
            # SLIDER 2: Liquidez (Ahorro corto plazo). Su máximo es lo que sobra después de Inversión.
            limite_liquidez = pct_restante - pct_inversion
            pct_liquidez = st.slider("💧 Liquidez / Emergencias %", min_value=0.0, max_value=float(limite_liquidez), value=float(limite_liquidez)*0.4, step=1.0)
            
            # El resto se va en automático a Estilo de Vida
            pct_estilo = pct_restante - pct_inversion - pct_liquidez
            st.write(f"✈️ Estilo de Vida se ajusta automáticamente a: **{pct_estilo:.1f}%**")

        monto_inversion = ingreso_total * (pct_inversion / 100)
        monto_liquidez = ingreso_total * (pct_liquidez / 100)
        monto_estilo = ingreso_total * (pct_estilo / 100)

        with col_grafica:
            labels = ['Gastos Fijos', 'Inversión (S&P 500)', 'Liquidez (Efectivo)', 'Estilo de Vida']
            values = [total_fijos, monto_inversion, monto_liquidez, monto_estilo]
            colores = ['#2C2C2E', '#007AFF', '#00d2ff', '#E5E5EA'] # Gris oscuro, Azul primario, Azul Neón (Liquidez), Blanco
            
            fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.55, marker=dict(colors=colores, line=dict(color='#1c1c1e', width=3)))])
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white", margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Tus Transferencias de ESTE MES")
        t1, t2, t3, t4 = st.columns(4)
        t1.metric("🏠 Costos Fijos", formatear_kpi(total_fijos))
        t2.metric("📈 Broker (Retiro)", formatear_kpi(monto_inversion))
        t3.metric("💧 Cuenta Liquidez", formatear_kpi(monto_liquidez))
        t4.metric("✈️ Estilo de Vida", formatear_kpi(monto_estilo))

        st.markdown("---")
        
        # PROYECCIÓN ANUAL
        st.markdown("### 📅 Proyección Anual (Forecast a 12 meses)")
        st.caption("Esto es lo que acumularás o gastarás en un año si mantienes exactamente este mismo presupuesto todos los meses.")
        
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Gastado en Fijos", formatear_kpi(total_fijos * 12))
        a2.metric("Total Invertido", formatear_kpi(monto_inversion * 12))
        a3.metric("Efectivo Ahorrado", formatear_kpi(monto_liquidez * 12))
        a4.metric("Gastado en Estilo", formatear_kpi(monto_estilo * 12))
