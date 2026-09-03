import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Financiero", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    :root {
        --bg-black: #000000;
        --card-dark: #121212;
        --border-gray: #333333;
        --neon-cyan: #00FFCC; 
        --neon-blue: #007AFF;
        --text-white: #FFFFFF;
    }
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; background-color: var(--bg-black) !important; }
    div[data-testid="stThumbValue"] {
        background-color: var(--neon-cyan) !important; color: #000 !important; border-radius: 20px !important; padding: 4px 10px !important; font-weight: 900;
    }
    .stSlider > div > div > div > div { background-color: var(--neon-cyan) !important; }
    div[data-testid="metric-container"] {
        background-color: var(--card-dark); border-radius: 12px; padding: 20px; border: 1px solid var(--border-gray); border-left: 4px solid var(--neon-cyan); 
    }
    header {visibility: hidden;}
    .disclaimer-box {
        background-color: var(--card-dark); padding: 15px 20px; border-radius: 8px; border: 1px solid var(--border-gray); border-left: 4px solid var(--neon-blue); margin-bottom: 20px; color: var(--text-white);
    }
</style>
""", unsafe_allow_html=True)

def formatear_kpi(numero):
    if numero == 0: return "$0"
    if numero >= 1_000_000: return f"${numero/1_000_000:.1f}M".replace(".0M", "M")
    elif numero >= 1_000: return f"${numero/1_000:.1f}k".replace(".0k", "k")
    else: return f"${numero:,.0f}"

with st.sidebar:
    st.markdown("### ⚡ Sistema Financiero")
    menu = st.radio("Módulos:", ("📈 Simulador de Retiro", "💼 Presupuesto Mensual"))
    st.markdown("---")
    
    # Anuncio Nu (Se mantiene)
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 12px; border: 1px solid #333; text-align: center; margin-top: 20px;">
        <p style="color: #8E8E93; font-size: 10px; margin-bottom: 10px; letter-spacing: 2px;">SPONSORED</p>
        <h3 style="color: #fff; margin-top: 0;">💳 Tarjeta Nu</h3>
        <p style="color: #aaa; font-size: 13px; margin-bottom: 15px;">14% de rendimiento anual disponible 24/7.</p>
        <a href="https://nu.com.mx/" target="_blank" style="background-color: #8A05BE; color: white; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-size: 14px; font-weight: bold; display: inline-block; width: 100%;">Solicitar Ahora</a>
    </div>
    """, unsafe_allow_html=True)

if menu == "📈 Simulador de Retiro":
    st.title("📈 Motor de Retiro")
    st.markdown("<p style='color:#8E8E93;'>Proyección de interés compuesto a largo plazo.</p>", unsafe_allow_html=True)

    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            # TODO EMPIEZA EN CERO
            capital_inicial = st.number_input("Capital Inicial ($)", min_value=0, value=0, step=1000)
        with c2:
            aportacion_mensual = st.number_input("Aportación Mensual ($)", min_value=0, value=0, step=500)
        with c3:
            anos = st.slider("Años invirtiendo", min_value=1, max_value=40, value=10) # 10 por default para que no marque error la gráfica
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
            datos.append({
                "Año": mes // 12, "Capital Propio": total_aportado_acum, "Rendimientos": saldo_actual - total_aportado_acum, "Total": saldo_actual
            })
            
    df = pd.DataFrame(datos)
    st.markdown("### 📊 Performance")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Capital Aportado", formatear_kpi(df["Capital Propio"].iloc[-1] if not df.empty else 0))
    k2.metric("Rendimientos", formatear_kpi(df["Rendimientos"].iloc[-1] if not df.empty else 0))
    k3.metric("Patrimonio Final", formatear_kpi(df["Total"].iloc[-1] if not df.empty else 0))
    k4.metric("Flujo Mensual Libre", formatear_kpi(((df["Total"].iloc[-1] if not df.empty else 0) * 0.05) / 12))

    fig = px.area(df, x="Año", y=["Capital Propio", "Rendimientos"], color_discrete_sequence=["#333333", "#00FFCC"])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#FFFFFF", hovermode="x unified", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # BANNER REALISTA DE GBM+ CON LOGO OFICIAL
    st.markdown("""
    <div style="background-color: #121212; border: 1px solid #333; border-radius: 12px; padding: 25px; text-align: center; margin-top: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">
        <p style="color: #8E8E93; font-size: 11px; margin-bottom: 10px; letter-spacing: 2px;">INVERSIÓN PATROCINADA</p>
        <img src="https://gbm.com/wp-content/uploads/2023/12/logo-gbm-blanco.svg" alt="GBM+" style="width: 150px; margin-bottom: 15px;">
        <h2 style="color: #fff; font-size: 20px; margin-bottom: 10px;">Pon a trabajar tu dinero hoy mismo</h2>
        <p style="color: #aaa; font-size: 15px; margin-bottom: 25px; max-width: 600px; margin-left: auto; margin-right: auto;">Abre tu cuenta de casa de bolsa, realiza tu primer fondeo desde $100 MXN y <b>recibe tu primera acción de regalo</b> (con valor de hasta $350).</p>
        <a href="https://promos.gbm.com/" target="_blank" style="background-color: #000; border: 1px solid #fff; color: #fff; padding: 12px 35px; border-radius: 30px; text-decoration: none; font-size: 16px; font-weight: bold; display: inline-block; transition: background-color 0.3s;">Reclamar Acción Gratis</a>
    </div>
    """, unsafe_allow_html=True)

elif menu == "💼 Presupuesto Mensual":
    st.title("💼 Ingeniería de Flujo")
    # TODO EMPIEZA EN CERO
    ingreso_total = st.number_input("Ingreso Total Disponible del Mes ($)", min_value=0.0, value=0.0, step=1000.0)

    st.markdown("### 1. Costos Fijos Operativos")
    with st.expander("Desglosar estructura de costos fijos", expanded=True):
        g1, g2, g3 = st.columns(3)
        with g1:
            renta = st.number_input("🏠 Hipoteca / Renta ($)", value=0.0, step=500.0)
            servicios = st.number_input("⚡ Servicios ($)", value=0.0, step=100.0)
        with g2:
            auto = st.number_input("🚗 Autos ($)", value=0.0, step=500.0)
            supermercado = st.number_input("🛒 Supermercado ($)", value=0.0, step=500.0)
        with g3:
            seguros = st.number_input("🛡️ Seguros ($)", value=0.0, step=100.0)
            otros = st.number_input("📦 Otros ($)", value=0.0, step=100.0)

    total_fijos = renta + servicios + auto + supermercado + seguros + otros
    pct_fijos = (total_fijos / ingreso_total * 100) if ingreso_total > 0 else 0
    dinero_restante = ingreso_total - total_fijos
    pct_restante = 100.0 - pct_fijos if ingreso_total > 0 else 0

    st.markdown("### 2. Distribución de Flujo Libre")
    
    if ingreso_total == 0:
        st.info("👆 Ingresa tu sueldo y tus gastos arriba para ver la distribución.")
    elif dinero_restante < 0:
        st.error(f"⚠️ Alerta: Costos fijos (${total_fijos:,.2f}) superan tus ingresos.")
    else:
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
