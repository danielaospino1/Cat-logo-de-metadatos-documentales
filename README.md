# 🗂️ Archivo Detective

Actividad interactiva de calidad de metadatos documentales.
**Bootcamp IA: Memoria y Preservación Digital — Archivo Histórico de Barranquilla 2026**

Taller: *Aplicación de IA en la Gestión de la Información* · 11:30am

## 📁 Archivos

```
bootcamp_archivo/
├── app.py                  # Aplicación principal Streamlit
├── generate_dataset.py     # Generador del catálogo sucio
├── metadatos_sucios.csv    # Dataset ya generado (listo para usar)
├── requirements.txt        # Dependencias Python
└── README.md               # Este archivo
```

## 🧩 Dinámica

Los participantes asumen el rol de **auditores de calidad de metadatos** del Archivo Histórico.
Reciben un catálogo documental exportado con 8 tipos de errores reales:

| # | Problema | Concepto archivístico |
|---|----------|-----------------------|
| 1 | Campo completamente vacío | Economía descriptiva (RiC-CM) |
| 2 | Registros duplicados | Integridad del fondo documental |
| 3 | Títulos faltantes | Metadato de identidad obligatorio |
| 4 | Dependencia productora faltante | Principio de procedencia |
| 5 | Calidad de imagen sin registrar | Metadato técnico de preservación |
| 6 | Formato de archivo desconocido | Requerimiento OAIS (ISO 14721) |
| 7 | Pesos de archivo absurdos | Metadato técnico — error de ingreso |
| 8 | Páginas imposibles | Metadato de extensión |
| 9 | Fecha digitalización < creación | Cadena de custodia digital |
| 10 | Dependencias inconsistentes | Interoperabilidad (AtoM) |
| 11 | Tipos documentales no normalizados | Taxonomía y clasificación archivística |

---

## 🚀 Opción 1: Desplegar en Streamlit Cloud

1. Crear repositorio en GitHub (público)
2. Subir los 4 archivos: `app.py`, `metadatos_sucios.csv`, `requirements.txt`, `README.md`
3. Ir a [share.streamlit.io](https://share.streamlit.io)
4. Conectar GitHub → seleccionar repo → seleccionar `app.py` → **Deploy**

URL resultante:
```
https://tu-usuario-archivo-detective.streamlit.app
```

## 💻 Opción 2: Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abre en `http://localhost:8501`
