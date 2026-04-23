import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(
    page_title="Tabla Periódica",
    layout="wide",
    initial_sidebar_state="expanded" # Fuerza a que la barra lateral inicie abierta
)

st.markdown(
    """
    <style>
    /* Bloquea y oculta el botón de cerrar la barra lateral */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Agrega un borde distintivo a la barra lateral */
    [data-testid="stSidebar"] {
        border-right: 3px solid #4CAF50;
        background-color: #000000;
    }

    /* Borde distintivo alrededor de toda la aplicación principal */
    .main {
        border: 4px solid #4CAF50;
        border-radius: 15px;
        margin: 10px;
        padding: 20px;
        background-color: #0e1117;
    }

    /* Estilo para que el buscador (selectbox) resalte más */
    .stSelectbox label {
        color: #4CAF50 !important;
        font-weight: bold;
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- BASE DE DATOS INTEGRADA  ---
# Se incluyen los elementos fundamentales y todos los metales industriales
# --- BASE DE DATOS COMPLETA (118 Elementos) ---
datos_csv = """nombre,img_name,simbolo,numero_atomico,masa_atomica,tipo,punto_fusion,densidad,electronegatividad
Hidrógeno,hydrogen,H,1,1.008,No metal,14.01,0.00008988,2.20
Helio,helium,He,2,4.0026,Gas noble,0.95,0.0001785,0
Litio,lithium,Li,3,6.94,Metal alcalino,453.69,0.534,0.98
Berilio,beryllium,Be,4,9.0122,Metal alcalinotérreo,1560,1.85,1.57
Boro,boron,B,5,10.81,Metaloide,2349,2.34,2.04
Carbono,carbon,C,6,12.011,No metal,3800,2.267,2.55
Nitrógeno,nitrogen,N,7,14.007,No metal,63.15,0.0012506,3.04
Oxígeno,oxygen,O,8,15.999,No metal,54.36,0.001429,3.44
Flúor,fluorine,F,9,18.998,Halógeno,53.53,0.001696,3.98
Neón,neon,Ne,10,20.180,Gas noble,24.56,0.0009002,0
Sodio,sodium,Na,11,22.990,Metal alcalino,370.87,0.971,0.93
Magnesio,magnesium,Mg,12,24.305,Metal alcalinotérreo,923,1.738,1.31
Aluminio,aluminium,Al,13,26.982,Metal post-transición,933.47,2.70,1.61
Silicio,silicon,Si,14,28.085,Metaloide,1687,2.329,1.90
Fósforo,phosphorus,P,15,30.974,No metal,317.30,1.82,2.19
Azufre,sulfur,S,16,32.06,No metal,388.36,2.067,2.58
Cloro,chlorine,Cl,17,35.45,Halógeno,171.6,0.003214,3.16
Argón,argon,Ar,18,39.948,Gas noble,83.80,0.0017837,0
Potasio,potassium,K,19,39.098,Metal alcalino,336.53,0.862,0.82
Calcio,calcium,Ca,20,40.078,Metal alcalinotérreo,1115,1.54,1.00
Escandio,scandium,Sc,21,44.955,Metal de transición,1814,2.989,1.36
Titanio,titanium,Ti,22,47.867,Metal de transición,1941,4.506,1.54
Vanadio,vanadium,V,23,50.941,Metal de transición,2183,6.11,1.63
Cromo,chromium,Cr,24,51.996,Metal de transición,2180,7.15,1.66
Manganeso,manganese,Mn,25,54.938,Metal de transición,1519,7.44,1.55
Hierro,iron,Fe,26,55.845,Metal de transición,1811,7.874,1.83
Cobalto,cobalt,Co,27,58.933,Metal de transición,1768,8.86,1.88
Níquel,nickel,Ni,28,58.693,Metal de transición,1728,8.902,1.91
Cobre,copper,Cu,29,63.546,Metal de transición,1357.77,8.96,1.90
Zinc,zinc,Zn,30,65.38,Metal de transición,692.88,7.14,1.65
Galio,gallium,Ga,31,69.723,Metal post-transición,302.91,5.91,1.81
Germanio,germanium,Ge,32,72.63,Metaloide,1211.40,5.323,2.01
Arsénico,arsenic,As,33,74.921,Metaloide,1090,5.727,2.18
Selenio,selenium,Se,34,78.971,No metal,494,4.81,2.55
Bromo,bromine,Br,35,79.904,Halógeno,265.8,3.1028,2.96
Criptón,krypton,Kr,36,83.798,Gas noble,115.79,0.003733,3.00
Rubidio,rubidium,Rb,37,85.468,Metal alcalino,312.45,1.532,0.82
Estroncio,strontium,Sr,38,87.62,Metal alcalinotérreo,1050,2.63,0.95
Itrio,yttrium,Y,39,88.906,Metal de transición,1799,4.472,1.22
Circonio,zirconium,Zr,40,91.224,Metal de transición,2128,6.52,1.33
Niobio,niobium,Nb,41,92.906,Metal de transición,2750,8.57,1.6
Molibdeno,molybdenum,Mo,42,95.95,Metal de transición,2896,10.28,2.16
Tecnecio,technetium,Tc,43,98,Metal de transición,2430,11.5,1.9
Rutenio,ruthenium,Ru,44,101.07,Metal de transición,2607,12.37,2.2
Rodio,rhodium,Rh,45,102.91,Metal de transición,2237,12.45,2.28
Paladio,palladium,Pd,46,106.42,Metal de transición,1828.05,12.023,2.20
Plata,silver,Ag,47,107.87,Metal de transición,1234.93,10.501,1.93
Cadmio,cadmium,Cd,48,112.41,Metal de transición,594.22,8.69,1.69
Indio,indium,In,49,114.81,Metal post-transición,429.75,7.31,1.78
Estaño,tin,Sn,50,118.71,Metal post-transición,505.08,7.287,1.96
Antimonio,antimony,Sb,51,121.76,Metaloide,903.78,6.685,2.05
Telurio,tellurium,Te,52,127.6,Metaloide,722.66,6.24,2.1
Yodo,iodine,I,53,126.9,Halógeno,386.85,4.933,2.66
Xenón,xenon,Xe,54,131.29,Gas noble,161.4,0.005887,2.6
Cesio,caesium,Cs,55,132.91,Metal alcalino,301.7,1.93,0.79
Bario,barium,Ba,56,137.33,Metal alcalinotérreo,1000,3.51,0.89
Lantano,lanthanum,La,57,138.91,Lantánido,1193,6.15,1.1
Cerio,cerium,Ce,58,140.12,Lantánido,1068,6.77,1.12
Praseodimio,praseodymium,Pr,59,140.91,Lantánido,1208,6.77,1.13
Neodimio,neodymium,Nd,60,144.24,Lantánido,1297,7.01,1.14
Prometio,promethium,Pm,61,145,Lantánido,1315,7.26,1.13
Samario,samarium,Sm,62,150.36,Lantánido,1345,7.52,1.17
Europio,europium,Eu,63,151.96,Lantánido,1099,5.24,1.2
Gadolinio,gadolinium,Gd,64,157.25,Lantánido,1585,7.90,1.2
Terbio,terbium,Tb,65,158.93,Lantánido,1629,8.23,1.1
Disprosio,dysprosium,Dy,66,162.50,Lantánido,1680,8.55,1.22
Holmio,holmium,Ho,67,164.93,Lantánido,1734,8.80,1.23
Erbio,erbium,Er,68,167.26,Lantánido,1802,9.07,1.24
Tulio,thulium,Tm,69,168.93,Lantánido,1818,9.32,1.25
Iterbio,ytterbium,Yb,70,173.05,Lantánido,1097,6.90,1.1
Lutecio,lutetium,Lu,71,174.97,Lantánido,1925,9.84,1.27
Hafnio,hafnium,Hf,72,178.49,Metal de transición,2506,13.31,1.3
Tántalo,tantalum,Ta,73,180.95,Metal de transición,3290,16.69,1.5
Wolframio,tungsten,W,74,183.84,Metal de transición,3695,19.25,2.36
Renio,rhenium,Re,75,186.21,Metal de transición,3459,21.02,1.9
Osmio,osmium,Os,76,190.23,Metal de transición,3306,22.59,2.2
Iridio,iridium,Ir,77,192.22,Metal de transición,2719,22.56,2.2
Platino,platinum,Pt,78,195.08,Metal de transición,2041,21.45,2.28
Oro,gold,Au,79,196.97,Metal de transición,1337,19.30,2.54
Mercurio,mercury,Hg,80,200.59,Metal de transición,234,13.53,2.00
Talio,thallium,Tl,81,204.38,Metal post-transición,577,11.85,1.62
Plomo,lead,Pb,82,207.2,Metal post-transición,600,11.34,2.33
Bismuto,bismuth,Bi,83,208.98,Metal post-transición,544,9.78,2.02
Polonio,polonium,Po,84,209,Metaloide,527,9.20,2.0
Astato,astatine,At,85,210,Halógeno,575,7.00,2.2
Radón,radon,Rn,86,222,Gas noble,202,0.00973,2.2
Francio,francium,Fr,87,223,Metal alcalino,300,1.87,0.7
Radio,radium,Ra,88,226,Metal alcalinotérreo,973,5.50,0.9
Actinio,actinium,Ac,89,227,Actínido,1323,10.07,1.1
Torio,thorium,Th,90,232.04,Actínido,2023,11.72,1.3
Protactinio,protactinium,Pa,91,231.04,Actínido,1841,15.37,1.5
Uranio,uranium,U,92,238.03,Actínido,1405,18.95,1.38
Neptunio,neptunium,Np,93,237,Actínido,917,20.45,1.36
Plutonio,plutonium,Pu,94,244,Actínido,912,19.82,1.28
Americio,americium,Am,95,243,Actínido,1449,13.67,1.13
Curio,curium,Cm,96,247,Actínido,1613,13.51,1.28
Berkelio,berkelium,Bk,97,247,Actínido,1259,14.78,1.3
Californio,californium,Cf,98,251,Actínido,1173,15.10,1.3
Einstenio,einsteinium,Es,99,252,Actínido,1133,8.84,1.3
Fermio,fermium,Fm,100,257,Actínido,1800,0,1.3
Mendelevio,mendelevium,Md,101,258,Actínido,1100,0,1.3
Nobelio,nobelium,No,102,259,Actínido,1100,0,1.3
Lawrencio,lawrencium,Lr,103,266,Actínido,1900,0,1.3
Rutherfordio,rutherfordium,Rf,104,267,Metal de transición,2400,23.2,0
Dubnio,dubnium,Db,105,268,Metal de transición,0,29.3,0
Seaborgio,seaborgium,Sg,106,269,Metal de transición,0,35.0,0
Bohrio,bohrium,Bh,107,270,Metal de transición,0,37.1,0
Hassio,hassium,Hs,108,269,Metal de transición,0,41.0,0
Meitnerio,meitnerium,Mt,109,278,Metal de transición,0,37.4,0
Darmstadtio,darmstadtium,Ds,110,281,Metal de transición,0,34.8,0
Roentgenio,roentgenium,Rg,111,282,Metal de transición,0,28.7,0
Copernicio,copernicium,Cn,112,285,Metal de transición,0,23.7,0
Nihonio,nihonium,Nh,113,286,Metal post-transición,0,16.0,0
Flerovio,flerovium,Fl,114,289,Metal post-transición,0,14.0,0
Moscovio,moscovium,Mc,115,290,Metal post-transición,0,13.5,0
Livermorio,livermorium,Lv,116,293,Metal post-transición,0,12.9,0
Teneso,tennessine,Ts,117,294,Halógeno,0,7.2,0
Oganesón,oganesson,Og,118,294,Gas noble,0,5.0,0"""

@st.cache_data
def cargar_datos():
    # Convertimos el string a un DataFrame de pandas automáticamente
    return pd.read_csv(io.StringIO(datos_csv))

df = cargar_datos()

# --- Interfaz Principal ---
# --- Interfaz Principal ---
st.title("🧪 Dashboard de Ingeniería: Materiales y Elementos")
st.markdown("---")

# ==============================================================================
# --- BARRA LATERAL (Búsqueda y Exportación) ---
# ==============================================================================
st.sidebar.header("🔍 Búsqueda y Control")
nombre_seleccionado = st.sidebar.selectbox("Selecciona un material:", df['nombre'].tolist())
datos_e = df[df['nombre'] == nombre_seleccionado].iloc[0]

st.sidebar.markdown("---")
st.sidebar.subheader("📄 Exportación de Datos")

# Plantilla del reporte técnico (generado automáticamente)
reporte_texto = f"""==================================================
FICHA TÉCNICA DE MATERIAL: {nombre_seleccionado.upper()}
==================================================
Símbolo: {datos_e['simbolo']}
Número Atómico (Z): {datos_e['numero_atomico']}
Familia/Tipo: {datos_e['tipo']}

[ PROPIEDADES FUNDAMENTALES ]
> Masa Atómica:       {datos_e['masa_atomica']} u
> Punto de Fusión:    {datos_e['punto_fusion']} K
> Densidad:           {datos_e['densidad']} g/cm³
> Electronegatividad: {datos_e['electronegatividad'] if datos_e['electronegatividad'] > 0 else 'N/A'}

==================================================
* Documento generado por el Sistema de Análisis *
"""

# Botón de descarga
st.sidebar.download_button(
    label=f"⬇️ Descargar Ficha del {nombre_seleccionado}",
    data=reporte_texto,
    file_name=f"Ficha_Tecnica_{nombre_seleccionado}.txt",
    mime="text/plain"
)
# ==============================================================================

# --- Sección Superior: Foto y Tarjeta ---
col_foto, col_info = st.columns([1, 1.5])

with col_foto:
    st.subheader("Muestra Real")
    # Usamos el nombre en inglés (oculto en los datos) para asegurar que la imagen siempre cargue
    url_img = f"https://images-of-elements.com/s/{datos_e['img_name']}.jpg"
    st.image(url_img, caption=f"Elemento: {nombre_seleccionado}", use_container_width=True)
    
    st.markdown(f"""
    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 5px solid #4CAF50; text-align: center;">
        <h1 style="color: #4CAF50; font-size: 70px; margin: 0;">{datos_e['simbolo']}</h1>
        <p style="font-size: 20px; color: white; margin: 0;">Z = {datos_e['numero_atomico']}</p>
    </div>
    """, unsafe_allow_html=True)

with col_info:
    st.subheader("Especificaciones Técnicas")
    m1, m2 = st.columns(2)
    m1.metric("Masa Atómica", f"{datos_e['masa_atomica']} u")
    m2.metric("Punto de Fusión", f"{datos_e['punto_fusion']} K")
    
    m3, m4 = st.columns(2)
    m3.metric("Densidad", f"{datos_e['densidad']} g/cm³")
    m4.metric("Electronegatividad", f"{datos_e['electronegatividad'] if datos_e['electronegatividad'] > 0 else 'N/A'}")

    st.info(f"**Categoría Química:** {datos_e['tipo']}")

st.markdown("---")

# --- Gráficas de Tendencia ---
st.header("📊 Comparativa de Propiedades Mecánicas y Químicas")
propiedad = st.selectbox("Variable a graficar:", ["densidad", "punto_fusion", "masa_atomica", "electronegatividad"])

# Gráfica interactiva
fig = px.line(df, x="numero_atomico", y=propiedad, 
              title=f"Evolución de la {propiedad.replace('_', ' ').title()}",
              labels={"numero_atomico": "Número Atómico (Z)"},
              markers=True, color_discrete_sequence=['#4CAF50'])

# Resaltar el elemento seleccionado con un punto rojo gigante
fig.add_scatter(x=[datos_e['numero_atomico']], y=[datos_e[propiedad]], 
                mode="markers", marker=dict(size=18, color="red"), name=nombre_seleccionado)

st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# --- MÓDULO DE CÁLCULOS Y SELECCIÓN DE MATERIALES ---
# ==============================================================================
st.markdown("---")
st.header("🧮 Modulo de Calculos y Seleccion de Materiales")

# Agregamos una tercera pestaña a nuestra lista
tab_masa, tab_termica, tab_comparador = st.tabs([
    "⚖️ Masa/Volumen", 
    "🔥 Dilatación Térmica", 
    "⚔️ Comparador de Materiales"
])

# --- PESTAÑA 1: MASA Y VOLUMEN ---
with tab_masa:
    st.subheader("Estimación de Peso para Piezas CAD")
    if datos_e['densidad'] > 0:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            volumen_cm3 = st.number_input("Volumen de la pieza (cm³):", min_value=0.1, value=100.0, step=10.0)
        with col_m2:
            masa_g = datos_e['densidad'] * volumen_cm3
            masa_kg = masa_g / 1000
            st.success(f"Peso estimado: **{masa_kg:,.3f} kg** ({masa_g:,.2f} g)")
    else:
        st.warning("No hay datos de densidad disponibles para este elemento.")

# --- PESTAÑA 2: DILATACIÓN TÉRMICA ---
with tab_termica:
    st.subheader("Análisis de Expansión por Temperatura")
    coeficientes_alfa = {
        "Aluminio": 23.1, "Cobre": 16.7, "Hierro": 11.8, "Titanio": 8.6, 
        "Oro": 14.2, "Plata": 18.9, "Silicio": 2.6, "Níquel": 13.0, "Plomo": 28.9
    }
    
    if nombre_seleccionado in coeficientes_alfa:
        alfa = coeficientes_alfa[nombre_seleccionado]
        st.write(f"Coeficiente ($\\alpha$) del {nombre_seleccionado}: **{alfa} $\\times 10^{-6} / ^\\circ C$**")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            l_inicial = st.number_input("Longitud (m):", min_value=0.01, value=1.0, step=0.1)
        with c2:
            t_inicial = st.number_input("T. inicial (°C):", value=20.0, step=5.0)
        with c3:
            t_final = st.number_input("T. final (°C):", value=80.0, step=5.0)
            
        delta_l = (alfa * 1e-6) * l_inicial * (t_final - t_inicial)
        st.metric("Expansión Total (ΔL)", f"{delta_l * 1000:.4f} mm")
    else:
        st.warning(f"Coeficiente de dilatación no registrado para {nombre_seleccionado}.")

# --- PESTAÑA 3: COMPARADOR FRENTE A FRENTE ---
with tab_comparador:
    st.subheader("Análisis Competitivo de Materiales")
    st.write("Selecciona un segundo material para evaluar sus diferencias críticas de diseño.")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        # El Material A es el que ya tenías seleccionado arriba
        st.markdown(f"**Material A (Referencia):** {nombre_seleccionado}")
        datos_m1 = datos_e
        
    with col_sel2:
        # Buscamos un Material B (por defecto ponemos Aluminio para que no sea el mismo)
        mat2 = st.selectbox("Material B (A evaluar):", df['nombre'].tolist(), index=12) 
        datos_m2 = df[df['nombre'] == mat2].iloc[0]

    st.markdown("---")
    
    # Columnas de comparación de métricas
    c_comp1, c_comp2 = st.columns(2)
    
    with c_comp1:
        st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>{datos_m1['simbolo']}</h2>", unsafe_allow_html=True)
        st.metric("Punto de Fusión", f"{datos_m1['punto_fusion']} K")
        st.metric("Densidad", f"{datos_m1['densidad']} g/cm³")
        st.metric("Masa Atómica", f"{datos_m1['masa_atomica']} u")
        
    with c_comp2:
        st.markdown(f"<h2 style='text-align: center; color: #2196F3;'>{datos_m2['simbolo']}</h2>", unsafe_allow_html=True)
        
        # Calculamos los deltas (diferencias) para que el usuario vea exactamente cuánto cambia
        dif_fusion = datos_m2['punto_fusion'] - datos_m1['punto_fusion']
        dif_densidad = datos_m2['densidad'] - datos_m1['densidad']
        dif_masa = datos_m2['masa_atomica'] - datos_m1['masa_atomica']
        
        # El parámetro delta_color="inverse" en densidad pone en verde si es más ligero (útil en diseño)
        st.metric("Punto de Fusión", f"{datos_m2['punto_fusion']} K", delta=f"{dif_fusion:.2f} K")
        st.metric("Densidad", f"{datos_m2['densidad']} g/cm³", delta=f"{dif_densidad:.3f} g/cm³", delta_color="inverse")
        st.metric("Masa Atómica", f"{datos_m2['masa_atomica']} u", delta=f"{dif_masa:.3f} u", delta_color="off")

    # Conclusión automática generada por los datos
    if dif_densidad != 0 or dif_fusion != 0:
        st.info(f"💡 **Veredicto Técnico:** El **{mat2}** es **{'más ligero' if dif_densidad < 0 else 'más pesado'}** que el {nombre_seleccionado}, y requiere **{'menos' if dif_fusion < 0 else 'más'}** temperatura para fundirse.")
