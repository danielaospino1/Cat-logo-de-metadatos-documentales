"""
╔══════════════════════════════════════════════════════════════════╗
║   ARCHIVO DETECTIVE 🗂️                                          ║
║   Actividad interactiva de limpieza de metadatos documentales   ║
║   Bootcamp IA: Memoria y Preservación Digital — AHB 2026        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import os

# ─────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Archivo Detective 🗂️",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────
# ESTILOS CSS
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

  /* Fondo principal — azul oscuro del bootcamp */
  .stApp { background-color: #05101f; color: #e2ecf8; }

  /* Sidebar */
  section[data-testid="stSidebar"] { background-color: #081a30; border-right: 1px solid #0d3a6e; }
  section[data-testid="stSidebar"] * { color: #c7ddf5 !important; }

  /* Tarjetas métricas */
  .metric-card {
    background: linear-gradient(135deg, #0a1f38 0%, #0d2d52 100%);
    border: 1px solid #1a4a7a;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 10px;
    text-align: center;
  }
  .metric-card .val  { font-size: 2.2rem; font-weight: 800; }
  .metric-card .lbl  { font-size: 0.82rem; color: #6fa3d4; margin-top: 3px; letter-spacing: 0.04em; }

  /* Tarjeta de problema */
  .problema-card {
    background: #0a1f38;
    border-left: 4px solid #f5a623;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 8px 0;
  }
  .problema-card.ok { border-left-color: #00c896; }

  /* Badge */
  .badge {
    display: inline-block;
    background: #0062cc;
    color: white;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 700;
    margin-left: 8px;
  }

  /* Barra de progreso */
  .prog-wrap {
    background: #0d2d52;
    border-radius: 8px;
    height: 18px;
    margin: 6px 0 14px 0;
    overflow: hidden;
  }
  .prog-bar { height: 100%; border-radius: 8px; transition: width 0.4s ease; }

  /* Título de sección */
  .section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #e8f2ff;
    border-bottom: 2px solid #0062cc;
    padding-bottom: 6px;
    margin: 24px 0 16px 0;
  }

  /* Hero band */
  .hero-band {
    background: linear-gradient(90deg, #0a2a50 0%, #0d4080 50%, #0a2a50 100%);
    border: 1px solid #1a5599;
    border-radius: 16px;
    padding: 32px 40px;
    text-align: center;
    margin-bottom: 28px;
  }

  /* Ocultar menú */
  #MainMenu, footer { visibility: hidden; }

  /* Botones */
  .stButton > button {
    background: linear-gradient(135deg, #0062cc 0%, #0047a3 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    font-family: 'Space Grotesk', sans-serif;
    padding: 9px 22px;
    letter-spacing: 0.02em;
  }
  .stButton > button:hover { background: linear-gradient(135deg, #0047a3 0%, #003380 100%); }

  /* Tablas */
  .stDataFrame { border-radius: 10px; overflow: hidden; }

  /* Headers */
  h1, h2, h3 { color: #e8f2ff !important; font-family: 'Space Grotesk', sans-serif !important; }

  /* Alertas */
  .stAlert { border-radius: 8px; }

  /* Code */
  code, .stCode { font-family: 'JetBrains Mono', monospace !important; }

  /* Concept pill */
  .concept-pill {
    display: inline-block;
    background: #0a2a50;
    border: 1px solid #1a5599;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.8rem;
    color: #7ec8ff;
    margin: 3px 2px;
  }

  /* Info box */
  .info-box {
    background: #04192e;
    border: 1px solid #0d3a6e;
    border-left: 4px solid #0062cc;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 0.92rem;
    color: #b0cde8;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────
PUNTOS = {
    "explorar_vista":              5,
    "explorar_nulos":             10,
    "explorar_duplicados":        10,
    "explorar_inconsistencias":   10,
    "limpiar_col_vacia":          15,
    "limpiar_duplicados":         20,
    "limpiar_nulos_titulo":       15,
    "limpiar_nulos_dependencia":  15,
    "limpiar_nulos_calidad":      15,
    "limpiar_nulos_formato":      15,
    "limpiar_outliers_peso":      25,
    "limpiar_outliers_paginas":   25,
    "limpiar_fechas_logicas":     20,
    "limpiar_dependencia_inconsistente": 20,
    "limpiar_tipo_documental":    20,
}
PUNTOS_MAX = sum(PUNTOS.values())

DEPENDENCIAS_VALIDAS = [
    "Secretaría General", "Hacienda", "Planeación",
    "Jurídica", "Archivo Histórico"
]
DEPENDENCIAS_MAP = {
    "Sec. General": "Secretaría General",
    "secretaria general": "Secretaría General",
    "SEC GEN": "Secretaría General",
    "HACIENDA": "Hacienda",
    "Hacienda Dist.": "Hacienda",
    "hacienda": "Hacienda",
    "Planeacion": "Planeación",
    "PLANEACIÓN": "Planeación",
    "juridica": "Jurídica",
    "Jurídica": "Jurídica",
    "arch. historico": "Archivo Histórico",
    "Archivo Hist.": "Archivo Histórico",
}
TIPOS_VALIDOS = [
    "Acta", "Resolución", "Contrato", "Circular", "Informe",
    "Memorando", "Decreto", "Certificado", "Solicitud", "Oficio"
]
TIPOS_MAP = {
    "acta": "Acta", "RESOLUCIÓN": "Resolución", "contrato ": "Contrato",
    "Informe ": "Informe", "CIRCULAR": "Circular", "memorando": "Memorando",
    "DECRETO": "Decreto", "Certificado.": "Certificado",
    "solicitud": "Solicitud", "OFICIO": "Oficio",
}


# ─────────────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────────────
def init_state():
    defaults = {
        "df_trabajo": None,
        "df_original": None,
        "puntos": 0,
        "logros": [],
        "fase": "inicio",
        "acciones_realizadas": set(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def sumar_puntos(clave: str):
    if clave not in st.session_state.acciones_realizadas:
        pts = PUNTOS.get(clave, 0)
        st.session_state.puntos += pts
        st.session_state.acciones_realizadas.add(clave)
        return pts
    return 0


def barra_progreso(valor, maximo, color="#0062cc"):
    pct = min(int(valor / maximo * 100), 100)
    st.markdown(f"""
    <div class="prog-wrap">
      <div class="prog-bar" style="width:{pct}%; background:{color};"></div>
    </div>
    <p style="color:#6fa3d4;font-size:0.8rem;margin-top:-10px;">{valor}/{maximo} puntos ({pct}%)</p>
    """, unsafe_allow_html=True)


def medalla(pts):
    if pts >= PUNTOS_MAX * 0.9:
        return "🥇 Archivista Experto en IA", "#f5c518"
    elif pts >= PUNTOS_MAX * 0.7:
        return "🥈 Gestor Documental Avanzado", "#94a3b8"
    elif pts >= PUNTOS_MAX * 0.5:
        return "🥉 Técnico en Metadatos", "#b45309"
    else:
        return "📄 Aprendiz de Archivo", "#4a6fa5"


def cargar_dataset():
    ruta = os.path.join(os.path.dirname(__file__), "metadatos_sucios.csv")
    df = pd.read_csv(ruta, parse_dates=["fecha_creacion", "fecha_digitalizacion"])
    return df


# ─────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:12px 0;">
          <div style="font-size:2.5rem;">🗂️</div>
          <div style="font-weight:800;font-size:1.1rem;color:#7ec8ff;">Archivo Detective</div>
          <div style="font-size:0.72rem;color:#4a7aaa;margin-top:2px;">
            Bootcamp IA · AHB 2026
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        pts = st.session_state.puntos
        st.markdown("### 🏆 Puntuación")
        barra_progreso(pts, PUNTOS_MAX,
                       "#00c896" if pts >= PUNTOS_MAX * 0.7 else "#0062cc")

        nombre_medalla, color_medalla = medalla(pts)
        st.markdown(
            f'<div style="background:{color_medalla}22;border:1px solid {color_medalla};'
            f'border-radius:8px;padding:8px;text-align:center;margin:8px 0;">'
            f'<span style="color:{color_medalla};font-weight:700;font-size:0.9rem;">'
            f'{nombre_medalla}</span></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📋 Fases")
        fases = [
            ("🚀", "inicio",   "Inicio"),
            ("🔍", "explorar", "Explorar Metadatos"),
            ("🧹", "limpiar",  "Normalizar Datos"),
            ("🏆", "resultado","Resultado Final"),
        ]
        for emoji, clave, nombre in fases:
            activa = st.session_state.fase == clave
            bloqueada = (clave == "limpiar" and
                         "explorar_vista" not in st.session_state.acciones_realizadas)
            bloqueada2 = (clave == "resultado" and
                          len(st.session_state.acciones_realizadas) < 5)

            if bloqueada or bloqueada2:
                st.markdown(
                    f'<div style="color:#2a4a6a;padding:6px 0;">🔒 {nombre}</div>',
                    unsafe_allow_html=True)
            elif activa:
                st.markdown(
                    f'<div style="background:#0062cc33;border-left:3px solid #0062cc;'
                    f'padding:6px 10px;border-radius:4px;font-weight:700;">'
                    f'{emoji} {nombre}</div>', unsafe_allow_html=True)
            else:
                if st.button(f"{emoji} {nombre}", key=f"nav_{clave}",
                             use_container_width=True):
                    st.session_state.fase = clave
                    st.rerun()

        st.markdown("---")
        if st.session_state.df_trabajo is not None:
            df = st.session_state.df_trabajo
            st.markdown("### 📊 Estado actual")
            st.markdown(f"- **Registros:** {len(df)}")
            st.markdown(f"- **Campos:** {df.shape[1]}")
            nulos = df.isnull().sum().sum()
            dupes = df.duplicated().sum()
            col_a = "🔴" if nulos > 0 else "🟢"
            col_b = "🔴" if dupes > 0 else "🟢"
            st.markdown(f"- {col_a} **Nulos:** {nulos}")
            st.markdown(f"- {col_b} **Duplicados:** {dupes}")

        st.markdown("---")
        st.caption("Taller IA en Gestión de la Información · 11:30am")


# ─────────────────────────────────────────────────────
# FASE 0: INICIO
# ─────────────────────────────────────────────────────
def fase_inicio():
    st.markdown("""
    <div class="hero-band">
      <div style="font-size:4rem;margin-bottom:8px;">🗂️</div>
      <h1 style="font-size:2.4rem;margin:6px 0;color:#7ec8ff !important;">Archivo Detective</h1>
      <p style="color:#6fa3d4;font-size:1.05rem;max-width:620px;margin:0 auto;">
        Un dataset de metadatos documentales llegó al sistema con errores críticos.<br>
        Tu misión: detectarlos, corregirlos y garantizar la <strong style="color:#7ec8ff;">autenticidad, 
        integridad y trazabilidad</strong> del patrimonio digital.
      </p>
      <div style="margin-top:16px;">
        <span class="concept-pill">📋 Metadatos RiC-CM</span>
        <span class="concept-pill">🔗 Cadena de custodia</span>
        <span class="concept-pill">🤖 IA aplicada a archivos</span>
        <span class="concept-pill">🛡️ Preservación digital</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    tarjetas = [
        ("🔍", "Explora", "Analiza el catálogo documental y detecta los problemas de metadatos ocultos.", "#3b82f6"),
        ("🧹", "Normaliza", "Aplica técnicas reales de limpieza: imputación, deduplicación, estandarización.", "#8b5cf6"),
        ("🏆", "Certifica", "Cada corrección suma puntos. ¿Llegarás a Archivista Experto en IA?", "#f5a623"),
    ]
    for col, (icon, titulo, desc, color) in zip([col1, col2, col3], tarjetas):
        with col:
            st.markdown(f"""
            <div style="background:#0a1f38;border:1px solid {color}44;border-top:3px solid {color};
                        border-radius:12px;padding:24px;text-align:center;height:190px;">
              <div style="font-size:2.2rem;">{icon}</div>
              <h3 style="color:{color};margin:8px 0;">{titulo}</h3>
              <p style="color:#6fa3d4;font-size:0.88rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📁 Tu misión</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown("""
        <div class="info-box">
        Eres parte del equipo de digitalización del <strong>Archivo Histórico de Barranquilla</strong>. 
        El sistema recibió una exportación masiva de metadatos documentales de cinco dependencias 
        distritales, pero el proceso falló: hay registros incompletos, duplicados por importación doble, 
        fechas imposibles, campos con valores anómalos y dependencias escritas de mil formas distintas.
        <br><br>
        Antes de que estos metadatos entren al repositorio oficial (AtoM) y se usen para modelos de 
        <strong>IA (RAG)</strong>, debes garantizar su calidad. Un metadato malo destruye la 
        trazabilidad y el valor probatorio del documento.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **¿Por qué importa la calidad de metadatos?**

        - Sin metadatos limpios, la IA genera recuperación de información incorrecta
        - Los duplicados distorsionan estadísticas de patrimonio documental
        - Fechas incoherentes rompen la cadena de custodia digital
        - Dependencias inconsistentes impiden la interoperabilidad entre sistemas
        """)
    with col_b:
        st.markdown("""
        <div class="metric-card">
          <div class="val" style="color:#0062cc;">315</div>
          <div class="lbl">Registros documentales</div>
        </div>
        <div class="metric-card">
          <div class="val" style="color:#f5a623;">16</div>
          <div class="lbl">Campos de metadatos</div>
        </div>
        <div class="metric-card">
          <div class="val" style="color:#ef4444;">8+</div>
          <div class="lbl">Tipos de problemas</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn, _, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("🚀 ¡Comenzar auditoría!", use_container_width=True):
            df = cargar_dataset()
            st.session_state.df_original = df.copy()
            st.session_state.df_trabajo  = df.copy()
            st.session_state.fase = "explorar"
            st.rerun()


# ─────────────────────────────────────────────────────
# FASE 1: EXPLORAR
# ─────────────────────────────────────────────────────
def fase_explorar():
    df = st.session_state.df_trabajo
    sumar_puntos("explorar_vista")

    st.markdown("# 🔍 Fase 1 — Auditoría de Metadatos")
    st.markdown(
        "Antes de normalizar, necesitas **entender el estado del catálogo**. "
        "Explora cada pestaña y detecta dónde están los problemas de calidad.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Catálogo general", "🕳️ Metadatos faltantes",
        "👯 Registros duplicados", "📈 Anomalías y distribuciones"
    ])

    # ── TAB 1: VISTA GENERAL ──
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        metricas = [
            (len(df), "Total registros", "#0062cc"),
            (df.shape[1], "Campos de metadatos", "#8b5cf6"),
            (int(df.isnull().sum().sum()), "Valores faltantes", "#ef4444"),
            (int(df.duplicated().sum()), "Duplicados", "#f5a623"),
        ]
        for col, (val, lbl, color) in zip([col1, col2, col3, col4], metricas):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                  <div class="val" style="color:{color};">{val}</div>
                  <div class="lbl">{lbl}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("#### Primeros 10 registros del catálogo")
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown("#### Estadísticas descriptivas")
        st.dataframe(df.describe(include="all").round(2), use_container_width=True)

    # ── TAB 2: NULOS ──
    with tab2:
        sumar_puntos("explorar_nulos")
        nulos = df.isnull().sum().reset_index()
        nulos.columns = ["Campo", "Faltantes"]
        nulos = nulos[nulos["Faltantes"] > 0].sort_values("Faltantes", ascending=False)
        nulos["% del total"] = (nulos["Faltantes"] / len(df) * 100).round(1)

        if nulos.empty:
            st.success("✅ No hay metadatos faltantes.")
        else:
            st.warning(f"⚠️ **{nulos['Faltantes'].sum()} metadatos faltantes** en {len(nulos)} campos críticos.")
            st.dataframe(nulos, use_container_width=True)

            fig, ax = plt.subplots(figsize=(8, 3), facecolor="#05101f")
            ax.set_facecolor("#0a1f38")
            bars = ax.barh(nulos["Campo"], nulos["Faltantes"], color="#ef4444", alpha=0.85)
            ax.set_xlabel("Cantidad de faltantes", color="#6fa3d4")
            ax.tick_params(colors="#94a3b8")
            ax.spines[["top","right","left","bottom"]].set_color("#1a4a7a")
            ax.set_title("Metadatos faltantes por campo", color="#e8f2ff", pad=10)
            for bar, val in zip(bars, nulos["Faltantes"]):
                ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                        str(val), va="center", color="#e8f2ff", fontsize=9)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            st.markdown("""
            <div class="info-box">
            💡 <strong>Concepto RiC-CM:</strong> En el estándar Records in Contexts (ICA), campos como 
            <em>titulo</em>, <em>dependencia</em> y <em>formato</em> son metadatos obligatorios de 
            identidad. Su ausencia invalida la descripción archivística y puede romper la cadena de custodia.
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 3: DUPLICADOS ──
    with tab3:
        sumar_puntos("explorar_duplicados")
        n_dupes = df.duplicated().sum()
        if n_dupes == 0:
            st.success("✅ No se detectaron registros duplicados.")
        else:
            st.error(f"🚨 **{n_dupes} registros duplicados exactos detectados.**")
            st.markdown("""
            <div class="info-box">
            💡 Los duplicados en un catálogo archivístico son un problema grave: inflan el recuento 
            de documentos del patrimonio, distorsionan métricas de gestión y pueden causar inconsistencias 
            en el repositorio AtoM. Típicamente ocurren por doble importación o errores de migración.
            </div>
            """, unsafe_allow_html=True)
            st.markdown("#### Ejemplos de registros duplicados:")
            dupes_df = df[df.duplicated(keep=False)].sort_values("id_documento")
            st.dataframe(dupes_df.head(10), use_container_width=True)

    # ── TAB 4: ANOMALÍAS ──
    with tab4:
        sumar_puntos("explorar_inconsistencias")

        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown("#### Distribución de `peso_kb`")
            fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#05101f")
            ax.set_facecolor("#0a1f38")
            ax.hist(df["peso_kb"].dropna(), bins=60, color="#0062cc", alpha=0.8, edgecolor="none")
            ax.set_xlabel("Peso (KB)", color="#6fa3d4")
            ax.tick_params(colors="#94a3b8")
            ax.spines[["top","right","left","bottom"]].set_color("#1a4a7a")
            ax.set_title("Peso de archivos — hay outliers extremos", color="#e8f2ff")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            outliers_peso = int((df["peso_kb"] > 100_000).sum())
            st.markdown(f"🚨 **{outliers_peso} archivos con peso > 100 MB** (valores imposibles)")

        with col_r:
            st.markdown("#### Distribución de `num_paginas`")
            fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#05101f")
            ax.set_facecolor("#0a1f38")
            ax.hist(df["num_paginas"].dropna(), bins=60, color="#8b5cf6", alpha=0.8, edgecolor="none")
            ax.set_xlabel("Número de páginas", color="#6fa3d4")
            ax.tick_params(colors="#94a3b8")
            ax.spines[["top","right","left","bottom"]].set_color("#1a4a7a")
            ax.set_title("Páginas por documento — hay valores anómalos", color="#e8f2ff")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            outliers_pag = int((df["num_paginas"] > 500).sum())
            st.markdown(f"🚨 **{outliers_pag} documentos con +500 páginas** (error de ingreso)")

        st.markdown("#### Valores únicos en `dependencia` (inconsistencias ortográficas)")
        vals_dep = df["dependencia"].dropna().unique()
        st.write(sorted(vals_dep))

        st.markdown("#### Valores únicos en `tipo_documental` (variantes no normalizadas)")
        vals_tipo = df["tipo_documental"].dropna().unique()
        st.write(sorted(vals_tipo))

        # Fechas incoherentes
        df_temp = df.copy()
        df_temp["fecha_creacion"] = pd.to_datetime(df_temp["fecha_creacion"], errors="coerce")
        df_temp["fecha_digitalizacion"] = pd.to_datetime(df_temp["fecha_digitalizacion"], errors="coerce")
        fechas_malas = int((df_temp["fecha_digitalizacion"] < df_temp["fecha_creacion"]).sum())
        st.markdown(f"#### ⏰ Inconsistencias temporales")
        st.error(f"🚨 **{fechas_malas} registros** donde la fecha de digitalización es **anterior** a la fecha de creación del documento. Imposible y viola la cadena de custodia.")

    # Botón para avanzar
    st.markdown("---")
    if "explorar_vista" in st.session_state.acciones_realizadas:
        if st.button("🧹 Ir a Normalizar Metadatos", use_container_width=False):
            st.session_state.fase = "limpiar"
            st.rerun()


# ─────────────────────────────────────────────────────
# FASE 2: LIMPIAR
# ─────────────────────────────────────────────────────
def fase_limpiar():
    df = st.session_state.df_trabajo

    st.markdown("# 🧹 Fase 2 — Normalización de Metadatos")
    st.markdown(
        "Aplica las técnicas de calidad de datos para que este catálogo pueda "
        "entrar de forma confiable al repositorio AtoM y alimentar modelos de IA.")

    st.markdown('<div class="section-title">📊 Estado actual del catálogo</div>',
                unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    metricas = [
        (len(df), "Registros", "#0062cc"),
        (int(df.isnull().sum().sum()), "Metadatos faltantes", "#ef4444"),
        (int(df.duplicated().sum()), "Duplicados", "#f5a623"),
        (st.session_state.puntos, "Puntos acumulados", "#00c896"),
    ]
    for col, (val, lbl, color) in zip([col1, col2, col3, col4], metricas):
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="val" style="color:{color};">{val}</div>
              <div class="lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── PROBLEMAS ──
    problemas = [
        {
            "id": "limpiar_col_vacia",
            "titulo": "🗑️ Campo completamente vacío: 'observaciones'",
            "descripcion": "La columna 'observaciones' tiene el 100% de valores nulos. Se creó en la exportación pero nunca se llenó.",
            "pistas": "Usa `df.dropna(axis=1, how='all', inplace=True)` para eliminar campos totalmente vacíos del catálogo.",
            "concepto": "En archivística, mantener campos vacíos sin valor genera ruido en los sistemas de descripción. RiC-CM establece que solo deben documentarse metadatos con valor real.",
            "puntos": PUNTOS["limpiar_col_vacia"],
        },
        {
            "id": "limpiar_duplicados",
            "titulo": "👯 Registros duplicados (doble importación)",
            "descripcion": f"Hay {int(st.session_state.df_original.duplicated().sum())} registros exactamente repetidos por un error de importación doble.",
            "pistas": "Usa `df.drop_duplicates(inplace=True)` para conservar solo la primera ocurrencia de cada registro.",
            "concepto": "Los duplicados en un catálogo archivístico son un problema de integridad: inflan el patrimonio documental y pueden generar descripciones contradictorias en AtoM.",
            "puntos": PUNTOS["limpiar_duplicados"],
        },
        {
            "id": "limpiar_nulos_titulo",
            "titulo": "🕳️ Títulos de documento faltantes",
            "descripcion": "Hay documentos sin título registrado. El título es metadato obligatorio según RiC-CM.",
            "pistas": "Imputar con un valor genérico: `df['titulo'].fillna('[Sin título registrado]', inplace=True)`",
            "concepto": "El título es el principal metadato de identidad de un documento. Sin él, la búsqueda y recuperación son imposibles, y el documento pierde valor probatorio.",
            "puntos": PUNTOS["limpiar_nulos_titulo"],
        },
        {
            "id": "limpiar_nulos_dependencia",
            "titulo": "🕳️ Dependencia productora faltante",
            "descripcion": "Algunos documentos no tienen dependencia asignada, lo que rompe la procedencia archivística.",
            "pistas": "Imputar con la moda: `df['dependencia'].fillna(df['dependencia'].mode()[0], inplace=True)`",
            "concepto": "La procedencia (fonds) es el principio fundamental de la archivística. Sin dependencia productora, el documento pierde contexto y autenticidad.",
            "puntos": PUNTOS["limpiar_nulos_dependencia"],
        },
        {
            "id": "limpiar_nulos_calidad",
            "titulo": "🕳️ Calidad de imagen sin registrar",
            "descripcion": "Variable numérica (1-5) con valores nulos. Indica la calidad del proceso de digitalización.",
            "pistas": "Imputar con la mediana: `df['calidad_imagen'].fillna(df['calidad_imagen'].median(), inplace=True)`",
            "concepto": "La calidad de imagen es un metadato técnico de preservación. Sin él, no se puede priorizar la re-digitalización de documentos deteriorados.",
            "puntos": PUNTOS["limpiar_nulos_calidad"],
        },
        {
            "id": "limpiar_nulos_formato",
            "titulo": "🕳️ Formato de archivo faltante",
            "descripcion": "Documentos sin formato registrado no pueden ser gestionados por el repositorio OAIS.",
            "pistas": "Imputar con 'Desconocido': `df['formato'].fillna('Desconocido', inplace=True)`",
            "concepto": "El formato es metadato técnico crítico para la preservación a largo plazo. El modelo OAIS (ISO 14721) lo requiere para garantizar la renderización futura del documento.",
            "puntos": PUNTOS["limpiar_nulos_formato"],
        },
        {
            "id": "limpiar_outliers_peso",
            "titulo": "📈 Pesos de archivo absurdos (outliers)",
            "descripcion": "Algunos registros muestran archivos con pesos de cientos de GB — error de ingreso de datos.",
            "pistas": "Calcula IQR: `limite = Q3 + 1.5*IQR` y filtra: `df = df[df['peso_kb'] <= limite]`",
            "concepto": "Un metadato técnico erróneo como el peso puede causar que el sistema de repositorio rechace o mal-clasifique el documento en la gestión del almacenamiento.",
            "puntos": PUNTOS["limpiar_outliers_peso"],
        },
        {
            "id": "limpiar_outliers_paginas",
            "titulo": "📈 Número de páginas imposible (outliers)",
            "descripcion": "Documentos administrativos con 5.000-9.999 páginas son errores de digitación.",
            "pistas": "Filtra: `df = df[df['num_paginas'] <= 500]`",
            "concepto": "Los metadatos de extensión (páginas, peso) permiten estimar recursos de digitalización y almacenamiento. Valores erróneos distorsionan la planificación presupuestal.",
            "puntos": PUNTOS["limpiar_outliers_paginas"],
        },
        {
            "id": "limpiar_fechas_logicas",
            "titulo": "⏰ Fechas de digitalización anteriores a la creación",
            "descripcion": "Hay documentos donde la fecha de digitalización es anterior a la fecha de creación — lógicamente imposible.",
            "pistas": "Filtra: `df = df[df['fecha_digitalizacion'] >= df['fecha_creacion']]`",
            "concepto": "Las inconsistencias temporales rompen la cadena de custodia digital. Un documento no puede digitalizarse antes de existir. Esto viola el principio de autenticidad documental.",
            "puntos": PUNTOS["limpiar_fechas_logicas"],
        },
        {
            "id": "limpiar_dependencia_inconsistente",
            "titulo": "🔀 Dependencias con formatos inconsistentes",
            "descripcion": "La columna 'dependencia' tiene abreviaciones y variantes: 'Sec. General', 'HACIENDA', 'juridica'...",
            "pistas": "Usa un diccionario de mapeo y `.replace()` para estandarizar a los 5 valores canónicos.",
            "concepto": "La normalización de entidades (dependencias, personas, lugares) es clave para la interoperabilidad. En AtoM, una dependencia mal escrita crea entidades duplicadas y fragmenta la descripción archivística.",
            "puntos": PUNTOS["limpiar_dependencia_inconsistente"],
        },
        {
            "id": "limpiar_tipo_documental",
            "titulo": "📄 Tipos documentales no normalizados",
            "descripcion": "Hay valores como 'acta', 'RESOLUCIÓN', 'contrato ' con espacios y mayúsculas inconsistentes.",
            "pistas": "Usa `TIPOS_MAP` y `.replace()`: `df['tipo_documental'] = df['tipo_documental'].replace(tipos_map)`",
            "concepto": "La taxonomía documental es la base de la clasificación archivística. Tipos inconsistentes impiden la agrupación en series y subseries, y confunden a los modelos de IA clasificadora.",
            "puntos": PUNTOS["limpiar_tipo_documental"],
        },
    ]

    for prob in problemas:
        ya_resuelto = prob["id"] in st.session_state.acciones_realizadas
        clase = "problema-card ok" if ya_resuelto else "problema-card"
        estado_icon = "✅" if ya_resuelto else "⚠️"

        st.markdown(f"""
        <div class="{clase}">
          <strong>{estado_icon} {prob['titulo']}</strong>
          <span class="badge">+{prob['puntos']} pts</span>
          <p style="color:#6fa3d4;margin:6px 0 0 0;font-size:0.9rem;">{prob['descripcion']}</p>
        </div>
        """, unsafe_allow_html=True)

        if not ya_resuelto:
            with st.expander(f"🔧 Resolver: {prob['titulo']}"):
                st.markdown(f"**💡 Técnica:** {prob['pistas']}")
                st.markdown(f"""
                <div class="info-box" style="margin-top:8px;">
                📚 <strong>¿Por qué importa?</strong> {prob['concepto']}
                </div>
                """, unsafe_allow_html=True)
                _render_accion(prob["id"], df)

    st.markdown("---")
    completados = len([p for p in problemas
                       if p["id"] in st.session_state.acciones_realizadas])
    st.info(f"📊 **{completados}/{len(problemas)} problemas resueltos**")

    if completados >= 5:
        if st.button("🏆 Ver mi certificado de auditoría", use_container_width=False):
            st.session_state.fase = "resultado"
            st.rerun()
    else:
        st.warning("Resuelve al menos 5 problemas para ver tu resultado final.")


def _render_accion(prob_id: str, df: pd.DataFrame):
    """Renderiza el botón de acción para cada problema."""

    if prob_id == "limpiar_col_vacia":
        cols_vacias = [c for c in df.columns if df[c].isnull().all()]
        if cols_vacias:
            st.code(f"# Campos completamente vacíos: {cols_vacias}\ndf.dropna(axis=1, how='all', inplace=True)")
            if st.button("Eliminar campos vacíos", key=prob_id):
                st.session_state.df_trabajo.dropna(axis=1, how="all", inplace=True)
                pts = sumar_puntos(prob_id)
                st.success(f"✅ Campo(s) {cols_vacias} eliminado(s). +{pts} puntos 🎉")
                st.rerun()
        else:
            st.success("No hay campos completamente vacíos.")

    elif prob_id == "limpiar_duplicados":
        n = df.duplicated().sum()
        st.code(f"# Duplicados actuales: {n}\ndf.drop_duplicates(inplace=True)\ndf.reset_index(drop=True, inplace=True)")
        if st.button("Eliminar registros duplicados", key=prob_id):
            st.session_state.df_trabajo.drop_duplicates(inplace=True)
            st.session_state.df_trabajo.reset_index(drop=True, inplace=True)
            pts = sumar_puntos(prob_id)
            st.success(f"✅ {n} duplicados eliminados. +{pts} puntos 🎉")
            st.rerun()

    elif prob_id == "limpiar_nulos_titulo":
        n = df["titulo"].isnull().sum() if "titulo" in df.columns else 0
        st.code(f"# Títulos faltantes: {n}\ndf['titulo'].fillna('[Sin título registrado]', inplace=True)")
        if st.button("Imputar títulos faltantes", key=prob_id):
            st.session_state.df_trabajo["titulo"] = \
                st.session_state.df_trabajo["titulo"].fillna("[Sin título registrado]")
            pts = sumar_puntos(prob_id)
            st.success(f"✅ {n} títulos imputados. +{pts} puntos 🎉")
            st.rerun()

    elif prob_id == "limpiar_nulos_dependencia":
        n = df["dependencia"].isnull().sum() if "dependencia" in df.columns else 0
        moda = df["dependencia"].mode()[0] if "dependencia" in df.columns and not df["dependencia"].mode().empty else "Secretaría General"
        st.code(f"# Dependencias faltantes: {n}\n# Moda: '{moda}'\ndf['dependencia'].fillna(df['dependencia'].mode()[0], inplace=True)")
        if st.button("Imputar dependencia con moda", key=prob_id):
            st.session_state.df_trabajo["dependencia"] = \
                st.session_state.df_trabajo["dependencia"].fillna(moda)
            pts = sumar_puntos(prob_id)
            st.success(f"✅ {n} dependencias imputadas con '{moda}'. +{pts} puntos 🎉")
            st.rerun()

    elif prob_id == "limpiar_nulos_calidad":
        n = df["calidad_imagen"].isnull().sum()
        mediana = df["calidad_imagen"].median()
        st.code(f"# Calidad de imagen faltante: {n}\n# Mediana: {mediana}\ndf['calidad_imagen'].fillna(df['calidad_imagen'].median(), inplace=True)")
        if st.button("Imputar calidad con mediana", key=prob_id):
            st.session_state.df_trabajo["calidad_imagen"] = \
                st.session_state.df_trabajo["calidad_imagen"].fillna(mediana)
            pts = sumar_puntos(prob_id)
            st.success(f"✅ {n} valores imputados con mediana={mediana}. +{pts} puntos 🎉")
            st.rerun()

    elif prob_id == "limpiar_nulos_formato":
        n = df["formato"].isnull().sum() if "formato" in df.columns else 0
        st.code(f"# Formatos faltantes: {n}\ndf['formato'].fillna('Desconocido', inplace=True)")
        if st.button("Imputar formato desconocido", key=prob_id):
            st.session_state.df_trabajo["formato"] = \
                st.session_state.df_trabajo["formato"].fillna("Desconocido")
            pts = sumar_puntos(prob_id)
            st.success(f"✅ {n} formatos imputados con 'Desconocido'. +{pts} puntos 🎉")
            st.rerun()

    elif prob_id == "limpiar_outliers_peso":
        col = "peso_kb"
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        limite = q3 + 1.5 * iqr
        n_out = int((df[col] > limite).sum())
        st.code(f"# Outliers en peso_kb: {n_out}\n# Límite IQR: {limite:.2f} KB\ndf = df[df['peso_kb'] <= {limite:.2f}]")
        if st.button("Eliminar pesos anómalos", key=prob_id):
            st.session_state.df_trabajo = \
                st.session_state.df_trabajo[
                    st.session_state.df_trabajo[col] <= limite
                ].reset_index(drop=True)
            pts = sumar_puntos(prob_id)
            st.success(f"✅ {n_out} registros con peso anómalo eliminados. +{pts} puntos 🎉")
            st.rerun()

    elif prob_id == "limpiar_outliers_paginas":
        col = "num_paginas"
        limite = 500
        n_out = int((df[col] > limite).sum())
        st.code(f"# Páginas anómalas (> {limite}): {n_out}\ndf = df[df['num_paginas'] <= {limite}]")
        if st.button("Filtrar páginas imposibles", key=prob_id):
            st.session_state.df_trabajo = \
                st.session_state.df_trabajo[
                    st.session_state.df_trabajo[col] <= limite
                ].reset_index(drop=True)
            pts = sumar_puntos(prob_id)
            st.success(f"✅ {n_out} registros con páginas imposibles eliminados. +{pts} puntos 🎉")
            st.rerun()

    elif prob_id == "limpiar_fechas_logicas":
        df_temp = df.copy()
        df_temp["fecha_creacion"] = pd.to_datetime(df_temp["fecha_creacion"], errors="coerce")
        df_temp["fecha_digitalizacion"] = pd.to_datetime(df_temp["fecha_digitalizacion"], errors="coerce")
        n_bad = int((df_temp["fecha_digitalizacion"] < df_temp["fecha_creacion"]).sum())
        st.code(f"# Inconsistencias temporales: {n_bad}\n# Digitalización anterior a creación\ndf = df[df['fecha_digitalizacion'] >= df['fecha_creacion']]")
        if st.button("Eliminar inconsistencias temporales", key=prob_id):
            df_w = st.session_state.df_trabajo.copy()
            df_w["fecha_creacion"] = pd.to_datetime(df_w["fecha_creacion"], errors="coerce")
            df_w["fecha_digitalizacion"] = pd.to_datetime(df_w["fecha_digitalizacion"], errors="coerce")
            st.session_state.df_trabajo = \
                df_w[df_w["fecha_digitalizacion"] >= df_w["fecha_creacion"]].reset_index(drop=True)
            pts = sumar_puntos(prob_id)
            st.success(f"✅ {n_bad} registros con fechas incoherentes eliminados. +{pts} puntos 🎉")
            st.rerun()

    elif prob_id == "limpiar_dependencia_inconsistente":
        dep_map = DEPENDENCIAS_MAP
        deps_raras = [d for d in df["dependencia"].dropna().unique()
                      if d not in DEPENDENCIAS_VALIDAS]
        n_afectadas = df["dependencia"].isin(deps_raras).sum()
        st.code(f"# Dependencias no estándar: {deps_raras}\n"
                f"# Registros afectados: {n_afectadas}\n"
                f"df['dependencia'] = df['dependencia'].replace(dep_map)")
        if st.button("Estandarizar dependencias", key=prob_id):
            st.session_state.df_trabajo["dependencia"] = \
                st.session_state.df_trabajo["dependencia"].replace(dep_map)
            pts = sumar_puntos(prob_id)
            st.success(f"✅ {n_afectadas} dependencias estandarizadas. +{pts} puntos 🎉")
            st.rerun()

    elif prob_id == "limpiar_tipo_documental":
        tipos_raros = [t for t in df["tipo_documental"].dropna().unique()
                       if t not in TIPOS_VALIDOS]
        n_afectadas = df["tipo_documental"].isin(tipos_raros).sum()
        st.code(f"# Tipos no normalizados: {tipos_raros}\n"
                f"# Registros afectados: {n_afectadas}\n"
                f"df['tipo_documental'] = df['tipo_documental'].replace(tipos_map)")
        if st.button("Normalizar tipos documentales", key=prob_id):
            st.session_state.df_trabajo["tipo_documental"] = \
                st.session_state.df_trabajo["tipo_documental"].replace(TIPOS_MAP)
            pts = sumar_puntos(prob_id)
            st.success(f"✅ {n_afectadas} tipos documentales normalizados. +{pts} puntos 🎉")
            st.rerun()


# ─────────────────────────────────────────────────────
# FASE 3: RESULTADO
# ─────────────────────────────────────────────────────
def fase_resultado():
    df_original = st.session_state.df_original
    df_limpio   = st.session_state.df_trabajo
    puntos_total = st.session_state.puntos
    nombre_medalla, color_medalla = medalla(puntos_total)

    st.markdown(f"""
    <div style="text-align:center;padding:36px 0 20px;">
      <div style="font-size:4rem;">{nombre_medalla.split()[0]}</div>
      <h1 style="font-size:2.3rem;color:{color_medalla} !important;">{nombre_medalla}</h1>
      <div style="font-size:3rem;font-weight:800;color:{color_medalla};">
        {puntos_total} / {PUNTOS_MAX} pts
      </div>
      <p style="color:#6fa3d4;margin-top:8px;">
        Catálogo documental auditado · Bootcamp IA: Memoria y Preservación Digital · AHB 2026
      </p>
    </div>
    """, unsafe_allow_html=True)

    barra_progreso(puntos_total, PUNTOS_MAX, color_medalla)
    st.markdown("---")

    # ── COMPARATIVA ──
    st.markdown('<div class="section-title">📊 Catálogo: Antes vs Después de la normalización</div>',
                unsafe_allow_html=True)

    metricas_comp = [
        ("Total registros",     len(df_original), len(df_limpio),   False),
        ("Campos activos",      df_original.shape[1], df_limpio.shape[1], False),
        ("Metadatos faltantes", int(df_original.isnull().sum().sum()),
                                int(df_limpio.isnull().sum().sum()), True),
        ("Duplicados",          int(df_original.duplicated().sum()),
                                int(df_limpio.duplicated().sum()), True),
    ]

    cols = st.columns(len(metricas_comp))
    for col, (label, antes, despues, menor_es_mejor) in zip(cols, metricas_comp):
        with col:
            delta = despues - antes
            if menor_es_mejor:
                color = "#00c896" if delta < 0 else ("#ef4444" if delta > 0 else "#94a3b8")
                signo = "▼" if delta < 0 else ("▲" if delta > 0 else "=")
            else:
                color = "#94a3b8"; signo = ""
            st.markdown(f"""
            <div class="metric-card">
              <div style="font-size:0.72rem;color:#4a7aaa;text-transform:uppercase;letter-spacing:0.05em;">{label}</div>
              <div style="display:flex;justify-content:center;gap:14px;margin:8px 0;">
                <div>
                  <div style="font-size:1.4rem;font-weight:700;color:#ef4444;">{antes}</div>
                  <div style="font-size:0.7rem;color:#6fa3d4;">Antes</div>
                </div>
                <div style="font-size:1.4rem;color:#2a4a6a;align-self:center;">→</div>
                <div>
                  <div style="font-size:1.4rem;font-weight:700;color:#00c896;">{despues}</div>
                  <div style="font-size:0.7rem;color:#6fa3d4;">Después</div>
                </div>
              </div>
              <div style="color:{color};font-weight:700;font-size:0.9rem;">{signo} {abs(delta)}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── GRÁFICA ──
    st.markdown("#### Distribución de `peso_kb`: Antes vs Después")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), facecolor="#05101f")
    for ax in axes:
        ax.set_facecolor("#0a1f38")
        ax.tick_params(colors="#94a3b8")
        ax.spines[["top","right","left","bottom"]].set_color("#1a4a7a")

    axes[0].hist(df_original["peso_kb"].dropna(), bins=50,
                 color="#ef4444", alpha=0.8, edgecolor="none")
    axes[0].set_title("ANTES (con outliers)", color="#e8f2ff", pad=10)
    axes[0].set_xlabel("Peso KB", color="#6fa3d4")

    axes[1].hist(df_limpio["peso_kb"].dropna(), bins=50,
                 color="#00c896", alpha=0.8, edgecolor="none")
    axes[1].set_title("DESPUÉS (normalizado)", color="#e8f2ff", pad=10)
    axes[1].set_xlabel("Peso KB", color="#6fa3d4")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # ── ACCIONES ──
    st.markdown('<div class="section-title">✅ Problemas resueltos</div>',
                unsafe_allow_html=True)
    acciones_limpiar = [k for k in st.session_state.acciones_realizadas
                        if k.startswith("limpiar_")]
    todas = [k for k in PUNTOS if k.startswith("limpiar_")]

    col_a, col_b = st.columns(2)
    for i, k in enumerate(todas):
        hecho = k in acciones_limpiar
        nombre_legible = k.replace("limpiar_", "").replace("_", " ").title()
        icon = "✅" if hecho else "❌"
        pts = PUNTOS[k]
        target = col_a if i % 2 == 0 else col_b
        with target:
            st.markdown(
                f'<div style="background:#0a1f38;border-radius:8px;padding:10px 14px;'
                f'margin:4px 0;border-left:3px solid {"#00c896" if hecho else "#1a4a7a"};">'
                f'{icon} <strong>{nombre_legible}</strong> '
                f'<span style="color:{"#00c896" if hecho else "#2a4a6a"};">+{pts if hecho else 0} pts</span>'
                f'</div>', unsafe_allow_html=True)

    # ── REFLEXIÓN ──
    st.markdown("---")
    st.markdown('<div class="section-title">🤖 Conexión con IA y preservación digital</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    Los problemas que acabas de resolver en este catálogo son exactamente los que enfrenta 
    cualquier sistema de <strong>IA aplicada a archivos</strong>:
    <br><br>
    • <strong>Metadatos faltantes</strong> → los modelos de clasificación no pueden operar sin campos completos<br>
    • <strong>Duplicados</strong> → sesgan los modelos de RAG y generan respuestas redundantes<br>
    • <strong>Inconsistencias ortográficas</strong> → fragmentan la búsqueda semántica en AtoM<br>
    • <strong>Outliers</strong> → distorsionan los embeddings vectoriales de los documentos<br>
    • <strong>Fechas incoherentes</strong> → rompen la cadena de custodia digital (OAIS)<br>
    <br>
    <strong>La calidad del dato es el primer paso de cualquier estrategia de IA en archivos.</strong>
    </div>
    """, unsafe_allow_html=True)

    # ── DESCARGA ──
    st.markdown('<div class="section-title">📥 Descargar catálogo normalizado</div>',
                unsafe_allow_html=True)
    csv_buffer = io.StringIO()
    df_limpio.to_csv(csv_buffer, index=False)

    col_dl, _, _ = st.columns([1, 2, 1])
    with col_dl:
        st.download_button(
            label="⬇️ Descargar metadatos_limpios.csv",
            data=csv_buffer.getvalue(),
            file_name="metadatos_limpios.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("---")
    if st.button("🔄 Nueva auditoría", use_container_width=False):
        for key in ["df_trabajo", "df_original", "puntos",
                    "logros", "fase", "acciones_realizadas"]:
            del st.session_state[key]
        st.rerun()


# ─────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────
def main():
    init_state()
    render_sidebar()

    fase = st.session_state.fase
    if fase == "inicio":
        fase_inicio()
    elif fase == "explorar":
        fase_explorar()
    elif fase == "limpiar":
        fase_limpiar()
    elif fase == "resultado":
        fase_resultado()


if __name__ == "__main__":
    main()
