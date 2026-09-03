import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard Financiero", layout="wide", initial_sidebar_state="expanded")

# -------------------------------------------------------------------
# INYECCIÓN DE CSS ESTILO "WHOOP" / HIGH-PERFORMANCE FINTECH
# -------------------------------------------------------------------
st.markdown("""
<style>
    /* Paleta Whoop: Fondo negro profundo, gris carbón y neón */
    :root {
        --bg-black: #000000;
        --card-dark: #121212;
        --border-gray: #333333;
        --neon-cyan: #00FFCC; /* Acento principal estilo Whoop */
        --neon-blue: #007AFF;
        --text-white: #FFFFFF;
        --text-muted: #8E8E93;
    }
    html, body, [class*="css"] { 
        font-family: 'Inter', -apple-system, sans-serif; 
        background-color: var(--bg-black) !important;
    }
    
    /* Hack para los Sliders (Neón y minimalista) */
    div[data-testid="stThumbValue"] {
        background-color: var(--neon-cyan) !important;
        color: #000 !important;
        border-radius: 20px !important;
        padding: 4px 10px !important;
        font-weight: 900;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.4);
    }
    .stSlider > div > div > div > div { background-color: var(--neon-cyan) !important; }

    /* Tarjetas de KPIs (Bordes delgados, sin sombras exageradas, muy industrial) */
    div[data-testid="metric-container"] {
        background-color: var(--card-dark);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid var(--border-gray);
        border-left: 4px solid var(--neon-cyan); 
        transition: border-color 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        border: 1px solid var(--neon-cyan);
    }
    
    /* Quitar encabezado default */
    header {visibility: hidden;}
    
    /* Cajas de Alertas / Disclaimer */
    .disclaimer-box {
        background-color: var(--card-dark);
        padding: 15px 20px;
        border-radius: 8px;
        border: 1px solid var(--border-gray);
        border-left: 4px solid var(--neon-blue);
        margin-bottom: 20px;
        color: var(--text-white);
    }
    
    /* Botones y Banners de Monetización (Hover effects) */
    .monetization-btn {
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .monetization-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

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
# LÓGICA DE NAVEGACIÓN Y BARRA LATERAL (CON ZONA DE ANUNCIO)
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Sistema Financiero")
    menu = st.radio("Módulos:", ("📈 Simulador de Retiro", "💼 Presupuesto Mensual"))
    st.markdown("---")
    
    # ZONA DE MONETIZACIÓN 1: BANNER ADSENSE NATIVO (Sidebar)
    # Aquí puedes cambiar la imagen, colores y link de referido de tu anunciante.
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 12px; border: 1px solid #333; text-align: center; margin-top: 20px;">
        <p style="color: #8E8E93; font-size: 10px; margin-bottom: 10px; letter-spacing: 2px;">SPONSORED</p>
        <h3 style="color: #fff; margin-top: 0;">💳 Tarjeta Nu</h3>
        <p style="color: #aaa; font-size: 13px; margin-bottom: 15px;">Haz crecer tu liquidez. <b>14% de rendimiento anual</b> disponible 24/7.</p>
        <a href="https://nu.com.mx/" target="_blank" style="background-color: #8A05BE; color: white; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-size: 14px; font-weight: bold; display: inline-block; width: 100%;">Solicitar Ahora</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><p style='color:#8E8E93; font-size:12px; text-align:center;'>v2.0 | Heber Orduño</p>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# PÁGINA 1: SIMULADOR DE RETIRO (CON ZONA GBM+)
# -------------------------------------------------------------------
if menu == "📈 Simulador de Retiro":
    st.title("📈 Motor de Retiro")
    st.markdown("<p style='color:#8E8E93;'>Proyección de interés compuesto y acumulación de capital a largo plazo.</p>", unsafe_allow_html=True)

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
                "Rendimientos": saldo_actual - total_aportado_acum,
                "Total": saldo_actual
            })
            
    df = pd.DataFrame(datos)
    st.markdown("### 📊 Performance")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Capital Aportado", formatear_kpi(df["Capital Propio"].iloc[-1]))
    k2.metric("Rendimientos", formatear_kpi(df["Rendimientos"].iloc[-1]))
    k3.metric("Patrimonio Final", formatear_kpi(df["Total"].iloc[-1]))
    k4.metric("Flujo Mensual Libre", formatear_kpi((df["Total"].iloc[-1] * 0.05) / 12))

    fig = px.area(df, x="Año", y=["Capital Propio", "Rendimientos"], color_discrete_sequence=["#333333", "#00FFCC"])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#FFFFFF", hovermode="x unified", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # ZONA DE MONETIZACIÓN 2: CTA PARA ABRIR CUENTA (GBM+)
    # Esta es la caja de conversión. Cuando el usuario se motiva al ver sus millones, le pones la solución enfrente.
    st.markdown("""
    <div class="monetization-btn" style="background: linear-gradient(145deg, #121212, #1c1c1e); border: 1px solid #00FFCC; border-radius: 12px; padding: 30px; text-align: center; margin-top: 20px;">
        <h2 style="color: #fff; margin-bottom: 5px;">🚀 Pasa a la Acción. Abre tu cuenta de inversión hoy.</h2>
        <p style="color: #8E8E93; font-size: 16px; margin-bottom: 25px;">Abre tu cuenta en <b>GBM+</b>, realiza tu primer depósito de $100 MXN y recibe una acción gratis (con valor de hasta $350) usando mi enlace.</p>
        <a href="https://promos.gbm.com/" target="_blank" style="background: linear-gradient(90deg, #00FFCC 0%, #007AFF 100%); color: #000; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-size: 18px; font-weight: 900; display: inline-block; box-shadow: 0 4px 15px rgba(0, 255, 204, 0.3);">Reclamar mi Acción Gratis</a>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# PÁGINA 2: CONTROL DE PRESUPUESTO
# -------------------------------------------------------------------
elif menu == "💼 Presupuesto Mensual":
    st.title("💼 Ingeniería de Flujo")
    st.markdown("<p style='color:#8E8E93;'>Presupuesto Base Cero: Asigna una función a cada peso de tus ingresos.</p>", unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-box">
        <b>💡 Algoritmo de Asignación (Regla 50/30/20)</b><br>
        <span style="color:#fff;"><b>50% Fijos</b></span> | 
        <span style="color:var(--neon-cyan);"><b>20% Retiro</b></span> | 
        <span style="color:var(--neon-blue);"><b>10% Liquidez</b></span> | 
        <span style="color:#8E8E93;"><b>20% Estilo</b></span>
    </div>
    """, unsafe_allow_html=True)

    ingreso_total = st.number_input("Ingreso Total Disponible del Mes ($)", min_value=1000.0, value=82500.0, step=1000.0)

    st.markdown("### 1. Costos Fijos Operativos")
    with st.expander("Desglosar estructura de costos fijos", expanded=False):
        g1, g2, g3 = st.columns(3)
        with g1:
            renta = st.number_input("🏠 Hipoteca / Renta ($)", value=12000.0, step=500.0)
            servicios = st.number_input("⚡ Servicios ($)", value=2500.0, step=100.0)
        with g2:
            auto = st.number_input("🚗 Autos ($)", value=6000.0, step=500.0)
            supermercado = st.number_input("🛒 Supermercado ($)", value=8000.0, step=500.0)
        with g3:
            seguros = st.number_input("🛡️ Seguros ($)", value=2000.0, step=100.0)
            otros = st.number_input("📦 Otros ($)", value=1500.0, step=100.0)

    total_fijos = renta + servicios + auto + supermercado + seguros + otros
    pct_fijos = (total_fijos / ingreso_total) * 100
    dinero_restante = ingreso_total - total_fijos
    pct_restante = 100.0 - pct_fijos

    st.markdown("### 2. Distribución de Flujo Libre")
    
    if dinero_restante < 0:
        st.error(f"⚠️ Alerta: Flujo de caja negativo. Costos fijos (${total_fijos:,.2f}) > Ingresos.")
    else:
        st.info(f"Costos fijos: **{pct_fijos:.1f}%**. Capital disponible para distribuir: **{pct_restante:.1f}%**.")
        
        col_sliders, col_grafica = st.columns([1, 1])

        with col_sliders:
            st.write("")
            pct_inversion = st.slider("📈 Retiro / Largo Plazo %", min_value=0.0, max_value=float(pct_restante), value=float(pct_restante)*0.4, step=1.0)
            limite_liquidez = pct_restante - pct_inversion
            pct_liquidez = st.slider("💧 Liquidez / Emergencias %", min_value=0.0, max_value=float(limite_liquidez), value=float(limite_liquidez)*0.4, step=1.0)
            pct_estilo = pct_restante - pct_inversion - pct_liquidez
            st.write(f"✈️ Estilo de Vida (Automático): **{pct_estilo:.1f}%**")

        monto_inversion = ingreso_total * (pct_inversion / 100)
        monto_liquidez = ingreso_total * (pct_liquidez / 100)
        monto_estilo = ingreso_total * (pct_estilo / 100)

        with col_grafica:
            labels = ['Fijos', 'Retiro', 'Liquidez', 'Estilo']
            values = [total_fijos, monto_inversion, monto_liquidez, monto_estilo]
            colores = ['#333333', '#00FFCC', '#007AFF', '#E5E5EA'] 
            
            fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.65, marker=dict(colors=colores, line=dict(color='#000000', width=4)))])
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#FFFFFF", margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Target Mensual")
        t1, t2, t3, t4 = st.columns(4)
        t1.metric("🏠 Fijos", formatear_kpi(total_fijos))
        t2.metric("📈 Retiro", formatear_kpi(monto_inversion))
        t3.metric("💧 Liquidez", formatear_kpi(monto_liquidez))
        t4.metric("✈️ Estilo", formatear_kpi(monto_estilo))
