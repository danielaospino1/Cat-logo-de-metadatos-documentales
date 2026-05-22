"""
Genera el dataset de metadatos documentales "sucios" para la actividad
Archivo Detective — Bootcamp IA: Memoria y Preservación Digital.
Ejecutar una sola vez: python generate_dataset.py
"""
import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

N = 300

# ── CATÁLOGOS ─────────────────────────────────────────────────────────────────
tipos_doc = [
    "Acta", "Resolución", "Contrato", "Circular", "Informe",
    "Memorando", "Decreto", "Certificado", "Solicitud", "Oficio"
]
series = {
    "Acta":        "Actas de Reunión",
    "Resolución":  "Resoluciones Administrativas",
    "Contrato":    "Contratos y Convenios",
    "Circular":    "Circulares",
    "Informe":     "Informes de Gestión",
    "Memorando":   "Memorandos",
    "Decreto":     "Decretos",
    "Certificado": "Certificados y Constancias",
    "Solicitud":   "Solicitudes Ciudadanas",
    "Oficio":      "Oficios",
}
dependencias = [
    "Secretaría General", "Hacienda", "Planeación",
    "Jurídica", "Archivo Histórico"
]
formatos = ["PDF", "TIFF", "JPEG", "DOCX", "PNG"]
idiomas = ["es"]
estados = ["Activo", "Inactivo", "Transferido", "Eliminado"]
clasificaciones = ["Público", "Reservado", "Confidencial"]

# ── DATOS LIMPIOS BASE ────────────────────────────────────────────────────────
fechas_creacion = pd.date_range("2018-01-01", "2024-12-31", periods=N)
fechas_creacion = sorted([f + pd.Timedelta(hours=random.randint(7, 17)) for f in fechas_creacion])

tipos = [random.choice(tipos_doc) for _ in range(N)]
peso_kb = [round(random.uniform(50, 8000), 1) for _ in range(N)]

df = pd.DataFrame({
    "id_documento":    [f"AHB-{2018 + i//50:04d}-{1000+i:04d}" for i in range(N)],
    "titulo":          [f"{t} #{random.randint(1,999):03d}" for t in tipos],
    "tipo_documental": tipos,
    "serie":           [series[t] for t in tipos],
    "dependencia":     [random.choice(dependencias) for _ in range(N)],
    "fecha_creacion":  fechas_creacion,
    "fecha_digitalizacion": [
        f + pd.Timedelta(days=random.randint(1, 730)) for f in fechas_creacion
    ],
    "formato":         [random.choice(formatos) for _ in range(N)],
    "peso_kb":         peso_kb,
    "num_paginas":     [random.randint(1, 80) for _ in range(N)],
    "idioma":          [random.choice(idiomas) for _ in range(N)],
    "estado":          [random.choice(estados) for _ in range(N)],
    "clasificacion":   [random.choice(clasificaciones) for _ in range(N)],
    "digitalizador":   [random.choice(["Ana García", "Carlos López", "María Rodríguez",
                                        "Juan Martínez", "Laura Sánchez"]) for _ in range(N)],
    "calidad_imagen":  [random.randint(1, 5) for _ in range(N)],
})

# ── INTRODUCIR PROBLEMAS ──────────────────────────────────────────────────────

# 1. Valores nulos (~10% en columnas críticas)
for col, pct in [("titulo", 0.07), ("dependencia", 0.09),
                  ("calidad_imagen", 0.12), ("formato", 0.06)]:
    idx = df.sample(frac=pct, random_state=42).index
    df.loc[idx, col] = np.nan

# 2. Duplicados exactos (15 registros repetidos — típico de importaciones dobles)
dupes = df.sample(15, random_state=7)
df = pd.concat([df, dupes], ignore_index=True)

# 3. Outliers en peso_kb (archivos con tamaño absurdo)
bad_peso_idx = df.sample(8, random_state=13).index
df.loc[bad_peso_idx, "peso_kb"] = df.loc[bad_peso_idx, "peso_kb"] * random.uniform(200, 500)

# 4. Outliers en num_paginas (imposibles)
bad_pag_idx = df.sample(5, random_state=21).index
df.loc[bad_pag_idx, "num_paginas"] = [5000, 9999, 7500, 6000, 8500]

# 5. Fechas de digitalización ANTERIORES a la fecha de creación (error lógico)
bad_fecha_idx = df.sample(6, random_state=33).index
df.loc[bad_fecha_idx, "fecha_digitalizacion"] = (
    df.loc[bad_fecha_idx, "fecha_creacion"] - pd.Timedelta(days=365)
)

# 6. Inconsistencias en dependencia (abreviaciones y variantes)
bad_dep_idx = df.sample(12, random_state=55).index
replacements = [
    "Sec. General", "HACIENDA", "Planeacion", "juridica", "arch. historico",
    "secretaria general", "PLANEACIÓN", "Hacienda Dist.", "Jurídica",
    "Archivo Hist.", "SEC GEN", "hacienda"
]
for i, idx in enumerate(bad_dep_idx):
    df.loc[idx, "dependencia"] = replacements[i % len(replacements)]

# 7. Columna de observaciones completamente vacía (campo que nunca se llenó)
df["observaciones"] = np.nan

# 8. Tipos documentales con variantes ortográficas
bad_tipo_idx = df.sample(10, random_state=77).index
tipo_map_dirty = {0:"acta", 1:"RESOLUCIÓN", 2:"contrato ", 3:"Informe ",
                   4:"CIRCULAR", 5:"memorando", 6:"DECRETO", 7:"Certificado.",
                   8:"solicitud", 9:"OFICIO"}
for i, idx in enumerate(bad_tipo_idx):
    df.loc[idx, "tipo_documental"] = tipo_map_dirty[i % 10]

# Mezclar
df = df.sample(frac=1, random_state=99).reset_index(drop=True)

df.to_csv("metadatos_sucios.csv", index=False)
print(f"✅ Dataset generado: {len(df)} filas, {df.shape[1]} columnas")
print(f"   Nulos por columna:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"   Duplicados: {df.duplicated().sum()}")
