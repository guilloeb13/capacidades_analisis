"""
SIEC v5.0: Sistema Integrado de Evaluación de Capacidades
==========================================================
Ingesta Real de Datos + Desambiguación Inteligente

Autor: Lead Data Scientist - OTAN Defense Analytics
Arquitectura: Lakehouse Híbrido + ETL + Weighted Scoring Algorithm
Framework: Streamlit + Pandas + Plotly + PDFPlumber
Versión: 5.0 (Real Data Ingestion + Intelligent Classification)

CHANGELOG v5.0:
- Selector de modo: Simulación vs Ingesta Real
- Función de desambiguación inteligente (clasificar_partida_inteligente)
- File uploader para Excel (eSIGEF presupuestos)
- File uploader para PDFs (reportes operativos)
- Procesamiento de Excel con normalización de columnas
- Extracción de texto de PDFs con pdfplumber
- Placeholder de conector a base de datos institucional
- Reglas de negocio para clasificación por capacidad + unidad

CHANGELOG v4.0:
- Orden de Batalla real FAE (15 unidades)
- Sistema de pesos DOTMLPF estratégicos configurables
- Algoritmo de scoring ponderado
- Controles de ajuste en sidebar
- Validación de pesos (suma 100%)
- Visualizaciones con valores ponderados
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from typing import Tuple, Dict, List
from io import BytesIO

# Importaciones para ingesta de datos v5.0
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    st.warning("⚠️ pdfplumber no disponible. Instale con: pip install pdfplumber")

try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    st.warning("⚠️ openpyxl no disponible. Instale con: pip install openpyxl")

# ============================================================================
# CONFIGURACIÓN GLOBAL Y CONSTANTES MILITARES
# ============================================================================

# ORDEN DE BATALLA REAL - FUERZA AÉREA ECUATORIANA (FAE)
MILITARY_UNITS = [
    "Ala de Combate Nro. 11",
    "Ala de Combate Nro. 21",
    "Ala de Combate Nro. 22",
    "Ala de Combate Nro. 23",
    "Ala de Transporte Nro. 11",
    "Grupo Aéreo Amazonas",
    "Grupo Aéreo Insular",
    "Escuela Superior Militar de Aviación (ESMA)",
    "Centro de Operaciones Aéreas (COA)",
    "Centro de Operaciones Sectorial 1 (COS-1)",
    "Centro de Operaciones Sectorial 2 (COS-2)",
    "Comando de Ciberdefensa (COCIBER)",
    "Dirección de Inteligencia Aérea",
    "Centro de Operaciones Espaciales (SpOC)",
    "Dirección de Planificación (DIRPLAN)"
]

# PESOS ESTRATÉGICOS DOTMLPF (Planificación Estratégica FAE)
# Basados en doctrina y prioridades institucionales
DEFAULT_DOTMLPF_WEIGHTS = {
    'M': 0.200,  # Material - 20.0%
    'F': 0.138,  # Facilities - 13.8%
    'P': 0.166,  # Personnel - 16.6%
    'T': 0.194,  # Training - 19.4%
    'D': 0.151,  # Doctrine - 15.1%
    'O': 0.151,  # Organization - 15.1%
    'L': 0.000   # Leadership - Distribuido en otros
}

# Capacidades Estratégicas del Sistema
STRATEGIC_CAPABILITIES = {
    'C2': {
        'name': 'MANDO Y CONTROL',
        'icon': '🎯',
        'description': 'Command, Control, Communications, Computers & Intelligence (C4I)',
        'status': 'operational'
    },
    'MANIOBRA': {
        'name': 'MANIOBRA AÉREA',
        'icon': '✈️',
        'description': 'Operaciones de Combate Aéreo y Proyección de Poder',
        'status': 'operational'
    },
    'CIBERDEFENSA': {
        'name': 'CIBERDEFENSA',
        'icon': '🛡️',
        'description': 'Operaciones Cibernéticas Defensivas y Ofensivas',
        'status': 'placeholder'
    },
    'LOGISTICA': {
        'name': 'LOGÍSTICA',
        'icon': '📦',
        'description': 'Sostenimiento y Cadena de Suministro Militar',
        'status': 'placeholder'
    }
}

# Taxonomía DOTMLPF (NATO Standard)
DOTMLPF_TAXONOMY = {
    'D': 'Doctrine',
    'O': 'Organization',
    'T': 'Training',
    'M': 'Material',
    'L': 'Leadership',
    'P': 'Personnel',
    'F': 'Facilities'
}

# Códigos Presupuestarios (Sistema eSIGEF Ecuatoriano)
BUDGET_CODE_MAPPING = {
    '51': 'P',  # Personal
    '53': 'T',  # Bienes/Servicios/Training
    '71': 'M',  # Inversión en Material
    '84': 'M',  # Material Estratégico
    '75': 'F',  # Infraestructura
    '57': 'O',  # Organización/Asesoría
    '58': 'D'   # Doctrina/Estudios
}

# Keywords para clasificación de CAPACIDADES
CAPABILITY_KEYWORDS = {
    'C2': [
        'comando', 'control', 'c2', 'c4i', 'bunker', 'estratégico', 'integrado',
        'radio', 'comunicaciones', 'enlace', 'radar', 'guerra electrónica',
        'jamming', 'frecuencia', 'espectro', 'criptográfico', 'software c2',
        'servidor', 'datos', 'operaciones conjuntas', 'interoperabilidad',
        'ciberdefensa', 'inteligencia', 'vigilancia', 'satelital'
    ],
    'MANIOBRA': [
        'piloto', 'vuelo', 'aeronave', 'avión', 'combate aéreo', 'misión',
        'super tucano', 'kfir', 'flota', 'tripulación', 'aerotécnica',
        'simulador', 'horas de vuelo', 'tiro real', 'munición aérea',
        'repuestos', 'rotables', 'pdm', 'mantenimiento mayor',
        'combustible aviación', 'jp1', 'hangar', 'pista', 'despegue',
        'aterrizaje', 'alerta', 'scramble', 'interceptación'
    ],
    'CIBERDEFENSA': [
        'ciber', 'hacking', 'firewall', 'soc', 'siem', 'apt', 'malware'
    ],
    'LOGISTICA': [
        'almacén', 'inventario', 'suministro', 'transporte', 'abastecimiento'
    ]
}

# Niveles operacionales por capacidad
OPERATIONAL_LEVELS = {
    'C2': ['C2 Estratégico', 'C2 Operacional', 'C2 Táctico', 'Guerra Electrónica'],
    'MANIOBRA': ['Combate Aéreo', 'Apoyo Aéreo Cercano', 'Interdicción', 'Reconocimiento Aéreo'],
    'CIBERDEFENSA': ['Nivel Estratégico', 'Nivel Operacional', 'Nivel Táctico'],
    'LOGISTICA': ['Nivel Estratégico', 'Nivel Operacional', 'Nivel Táctico']
}

# Keywords para análisis de riesgo NLP
RISK_KEYWORDS = {
    'crítico': 100,
    'falla': 80,
    'inoperativo': 90,
    'sin stock': 70,
    'sin capacitación': 75,
    'obsoleto': 85,
    'sobrecalentamiento': 65,
    'sin repuestos': 80,
    'vencido': 70,
    'sin personal': 85,
    'no disponible': 75,
    'requiere overhaul': 70,
    'grounded': 95,
    'no apto para vuelo': 100
}

POSITIVE_KEYWORDS = [
    'operando al 100%', 'excelente', 'óptimo', 'actualizado', 'disponible',
    'misión cumplida', 'ready', 'apto para vuelo', 'certificado'
]

# ============================================================================
# MÓDULO 1: GENERACIÓN DE DATOS ESTRUCTURADOS (SQL SIMULADO)
# ============================================================================

def generate_structured_data(capability: str = None) -> pd.DataFrame:
    """
    Simula la ingesta desde eSIGEF con Orden de Batalla real FAE.
    Genera partidas presupuestarias específicas por capacidad.

    Args:
        capability: 'C2', 'MANIOBRA', 'CIBERDEFENSA', 'LOGISTICA', o None (todas)

    Returns:
        DataFrame con estructura de presupuesto militar
    """

    np.random.seed(42)
    random.seed(42)

    # Partidas C2
    c2_items = [
        ('Licencias Software C2', '530801', 'T', 'C2'),
        ('Radios HF Tácticas', '840101', 'M', 'C2'),
        ('Construcción Bunker Datos', '750101', 'F', 'C2'),
        ('Curso Ciberdefensa', '530501', 'T', 'C2'),
        ('Servidor Principal C2', '710101', 'M', 'C2'),
        ('Mantenimiento Radar', '530201', 'M', 'C2'),
        ('Antenas Satelitales', '840102', 'M', 'C2'),
        ('Capacitación Operadores C2', '530502', 'T', 'C2'),
        ('Estudio Doctrina Conjunta', '580101', 'D', 'C2'),
        ('Consultoría Interoperabilidad', '570101', 'O', 'C2'),
        ('Simulador Guerra Electrónica', '710201', 'M', 'C2'),
        ('Renovación Centro Comando', '750102', 'F', 'C2'),
        ('Equipos Criptográficos', '840103', 'M', 'C2'),
        ('Personal Especializado C2', '510101', 'P', 'C2'),
        ('Generadores de Emergencia', '710301', 'F', 'C2'),
        ('Software Inteligencia Artificial', '530802', 'T', 'C2'),
        ('Fibra Óptica Redundante', '750103', 'F', 'C2'),
        ('Curso Liderazgo Táctico', '530503', 'L', 'C2'),
        ('Repuestos Sistema Radar', '530202', 'M', 'C2'),
        ('Análisis Vulnerabilidades', '580102', 'D', 'C2')
    ]

    # Partidas Maniobra
    maniobra_items = [
        ('Sueldos Pilotos Combate', '510201', 'P', 'MANIOBRA'),
        ('Bonificación Vuelo', '510202', 'P', 'MANIOBRA'),
        ('Tripulación Aerotécnica', '510203', 'P', 'MANIOBRA'),
        ('Personal Mantenimiento Aeronáutico', '510204', 'P', 'MANIOBRA'),
        ('Horas de Vuelo Entrenamiento', '530510', 'T', 'MANIOBRA'),
        ('Simulador Full Mission', '530511', 'T', 'MANIOBRA'),
        ('Curso Combate Aéreo Avanzado', '530512', 'T', 'MANIOBRA'),
        ('Entrenamiento Tiro Real', '530513', 'T', 'MANIOBRA'),
        ('Certificación Pilotos Instructores', '530514', 'T', 'MANIOBRA'),
        ('Curso Vuelo Instrumental IFR', '530515', 'T', 'MANIOBRA'),
        ('Entrenamiento Combate Aire-Tierra', '530516', 'T', 'MANIOBRA'),
        ('Repuestos Flota Super Tucano', '710401', 'M', 'MANIOBRA'),
        ('Mantenimiento PDM Aeronaves', '710402', 'M', 'MANIOBRA'),
        ('Adquisición Munición Aérea', '840201', 'M', 'MANIOBRA'),
        ('Compra Rotables Críticos', '840202', 'M', 'MANIOBRA'),
        ('Overhaul Motor Turbohélice', '710403', 'M', 'MANIOBRA'),
        ('Sistema Aviónica Modernizado', '840203', 'M', 'MANIOBRA'),
        ('Asientos Eyectables Martin Baker', '840204', 'M', 'MANIOBRA'),
        ('Tren de Aterrizaje Principal', '710404', 'M', 'MANIOBRA'),
        ('Combustible Aviación JP1', '530310', 'O', 'MANIOBRA'),
        ('Seguro Casco Aéreo', '530910', 'O', 'MANIOBRA'),
        ('Servicios Meteorológicos', '530311', 'O', 'MANIOBRA'),
        ('Mantenimiento Pista Principal', '750201', 'F', 'MANIOBRA'),
        ('Construcción Hangar Alerta', '750202', 'F', 'MANIOBRA'),
        ('Modernización Torre Control', '750203', 'F', 'MANIOBRA'),
        ('Sistema Iluminación Pista', '750204', 'F', 'MANIOBRA')
    ]

    records = []
    start_date = datetime(2024, 1, 1)

    # Determinar items según capacidad
    if capability == 'C2':
        capability_items = c2_items
        num_records = 70
    elif capability == 'MANIOBRA':
        capability_items = maniobra_items
        num_records = 70
    elif capability is None:
        capability_items = c2_items + maniobra_items
        num_records = 140
    else:
        capability_items = []
        num_records = 0

    # Generar registros
    for i in range(num_records):
        if not capability_items:
            break

        item = random.choice(capability_items)
        item_capability = item[3]
        unit = random.choice(MILITARY_UNITS)  # ORDEN DE BATALLA REAL

        monto_asignado = np.random.randint(50000, 500000)
        ejecucion_pct = np.random.beta(7, 3)
        monto_ejecutado = int(monto_asignado * ejecucion_pct)

        fecha = start_date + timedelta(days=random.randint(0, 330))

        records.append({
            'ID_Partida': f'{item_capability[:3]}-{i+1:04d}',
            'Codigo_Presupuestario': item[1],
            'Descripcion': item[0],
            'Monto_Asignado': monto_asignado,
            'Monto_Ejecutado': monto_ejecutado,
            'Fecha': fecha,
            'Unidad_Beneficiaria': unit,
            'Tipo_Recurso': 'Inversión' if item[1].startswith(('71', '84', '75')) else 'Gasto',
            'DOTMLPF_Tag': item[2],
            'Capacidad': item_capability
        })

    # Partidas genéricas
    generic_items = [
        ('Servicios Básicos', '530101', 'O'),
        ('Material Oficina', '530102', 'O'),
        ('Uniformes Personal', '530601', 'P'),
        ('Viáticos Misiones', '530701', 'O'),
        ('Alimentación Tropa', '530602', 'P'),
        ('Seguros Institucionales', '530901', 'O'),
        ('Mantenimiento Vehículos', '530301', 'M'),
        ('Comunicación Institucional', '530103', 'O'),
        ('Servicios de Limpieza', '530104', 'O'),
        ('Capacitación General', '530504', 'T')
    ]

    for i in range(10):
        item = random.choice(generic_items)
        cap = capability if capability else random.choice(['C2', 'MANIOBRA'])
        unit = random.choice(MILITARY_UNITS)

        monto_asignado = np.random.randint(10000, 100000)
        ejecucion_pct = np.random.beta(5, 3)
        monto_ejecutado = int(monto_asignado * ejecucion_pct)

        fecha = start_date + timedelta(days=random.randint(0, 330))

        records.append({
            'ID_Partida': f'GEN-{i+1:04d}',
            'Codigo_Presupuestario': item[1],
            'Descripcion': item[0],
            'Monto_Asignado': monto_asignado,
            'Monto_Ejecutado': monto_ejecutado,
            'Fecha': fecha,
            'Unidad_Beneficiaria': unit,
            'Tipo_Recurso': 'Inversión' if item[1].startswith(('71', '84', '75')) else 'Gasto',
            'DOTMLPF_Tag': item[2],
            'Capacidad': cap
        })

    df = pd.DataFrame(records)
    return df


# ============================================================================
# MÓDULO 2: GENERACIÓN DE DATOS NO ESTRUCTURADOS (NLP SIMULADO)
# ============================================================================

def generate_unstructured_data(capability: str = None) -> pd.DataFrame:
    """
    Simula reportes operativos de texto libre con unidades FAE reales.

    Args:
        capability: Capacidad a filtrar

    Returns:
        DataFrame con reportes de novedades operativas
    """

    random.seed(42)

    c2_reports = [
        "Falla crítica en servidor principal por sobrecalentamiento. Requiere intervención inmediata.",
        "Personal de radar sin curso de actualización vigente desde hace 8 meses.",
        "Sistema de comunicaciones satelitales presenta intermitencia en horas pico.",
        "Stock de repuestos para radios HF en nivel crítico (15% capacidad).",
        "Bunker de datos operando sin sistema de respaldo desde mantenimiento.",
        "Licencias de software C2 vencidas. 40% de estaciones inoperativas.",
        "Generador de emergencia con falla mecánica no reparada.",
        "Antena principal con desalineamiento detectado por personal técnico.",
        "Curso de ciberdefensa cancelado por falta de instructores certificados.",
        "Equipo criptográfico obsoleto, no compatible con estándares OTAN actuales.",
        "Personal especializado insuficiente para cubrir turnos 24/7.",
        "Sistema de refrigeración del centro de datos fuera de servicio.",
        "Enlaces de fibra óptica vulnerables, sin redundancia operativa.",
        "Simulador de guerra electrónica sin calibración desde hace 18 meses.",
        "Enlaces satelitales operando al 100% de capacidad nominal.",
        "Personal completó certificación internacional en guerra electrónica.",
        "Sistema de respaldo activado exitosamente durante simulacro.",
        "Nuevo bunker de datos inaugurado con tecnología de última generación.",
        "Software de inteligencia artificial integrado exitosamente al sistema C2.",
        "Capacitación de operadores completada con calificación excelente.",
        "Sistema de detección temprana funcionando óptimamente según pruebas.",
        "Redundancia de comunicaciones verificada en ejercicio conjunto.",
        "Equipos criptográficos actualizados a estándares NATO vigentes.",
        "Centro de operaciones conjuntas certificado para operaciones 24/7.",
        "Radar de vigilancia aérea presentando ecos fantasma en sector norte."
    ]

    maniobra_reports = [
        "Flota Super Tucano operando al 85% de disponibilidad. Dos aeronaves en PDM programado.",
        "Piloto experimentado completó 1000 horas de vuelo en combate. Certificación excelente.",
        "Stock de repuestos críticos para tren de aterrizaje en nivel rojo. Requiere reposición urgente.",
        "Simulador full mission inoperativo por falla en sistema de proyección visual.",
        "Munición aérea de entrenamiento agotada. Curso de tiro real suspendido temporalmente.",
        "Mantenimiento PDM de aeronave FAE-2301 completado exitosamente en 45 días.",
        "Combustible JP1 con inventario crítico. Solo disponible para misiones prioritarias.",
        "Hangar de alerta con sistema de iluminación averiado desde hace 15 días.",
        "Tripulación aerotécnica sin personal suficiente para turnos nocturnos.",
        "Asientos eyectables Martin Baker requieren overhaul según directiva técnica.",
        "Motor turbohélice con indicadores de performance degradada. Inspección boroscópica programada.",
        "Sistema aviónica modernizado instalado exitosamente en tres aeronaves.",
        "Pista principal con fisuras detectadas en inspección de seguridad operacional.",
        "Certificación de pilotos instructores completada con estándar NATO.",
        "Rotables críticos sin stock. Aeronave grounded hasta arribo de repuestos.",
        "Entrenamiento de combate aire-tierra ejecutado con resultados sobresalientes.",
        "Torre de control con equipos de comunicación obsoletos. Reemplazo programado Q2.",
        "Bonificación de vuelo pendiente de pago desde hace 3 meses. Personal desmotivado.",
        "Seguro de casco aéreo vencido para dos aeronaves. No aptas para vuelo operacional.",
        "Curso de vuelo instrumental IFR suspendido por condiciones meteorológicas adversas.",
        "Sistema de iluminación de pista reparado. Operaciones nocturnas restablecidas al 100%.",
        "Overhaul de motor completado antes de lo programado. Aeronave ready para misión.",
        "Personal de mantenimiento aeronáutico completó certificación en nuevos sistemas.",
        "Horas de vuelo de entrenamiento ejecutadas al 92% del plan anual.",
        "Servicios meteorológicos operando óptimamente. Pronósticos precisos para planificación."
    ]

    # Seleccionar reportes
    if capability == 'C2':
        selected_reports = c2_reports
    elif capability == 'MANIOBRA':
        selected_reports = maniobra_reports
    elif capability is None:
        selected_reports = c2_reports + maniobra_reports
    else:
        selected_reports = []

    selected_reports = selected_reports[:50]

    records = []
    for i, report_text in enumerate(selected_reports):
        report_capability = classify_capability(report_text)
        unit = random.choice(MILITARY_UNITS)  # ORDEN DE BATALLA REAL
        fecha = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 330))

        records.append({
            'Report_ID': f'RPT-{i+1:04d}',
            'Fecha': fecha,
            'Unidad': unit,
            'Texto_Reporte': report_text,
            'Categoria': 'Operacional',
            'Capacidad': report_capability
        })

    return pd.DataFrame(records)


# ============================================================================
# MÓDULO 3: CLASIFICACIÓN DE CAPACIDADES
# ============================================================================

def classify_capability(description: str) -> str:
    """Clasifica texto en capacidad estratégica."""
    desc_lower = description.lower()
    scores = {}

    for cap, keywords in CAPABILITY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in desc_lower)
        scores[cap] = score

    if max(scores.values()) > 0:
        return max(scores, key=scores.get)

    return 'C2'


def classify_operational_level(description: str, capability: str) -> str:
    """Clasifica en nivel operacional según capacidad."""
    levels = OPERATIONAL_LEVELS.get(capability, OPERATIONAL_LEVELS['C2'])
    desc_lower = description.lower()

    if capability == 'C2':
        if any(word in desc_lower for word in ['estratégico', 'nacional', 'integrado']):
            return levels[0]
        elif any(word in desc_lower for word in ['operacional', 'teatro', 'conjunto']):
            return levels[1]
        elif any(word in desc_lower for word in ['táctico', 'campo', 'móvil']):
            return levels[2]
        elif any(word in desc_lower for word in ['radar', 'guerra electrónica', 'jamming']):
            return levels[3]

    elif capability == 'MANIOBRA':
        if any(word in desc_lower for word in ['combate aéreo', 'interceptación']):
            return levels[0]
        elif any(word in desc_lower for word in ['apoyo', 'cercano', 'cas']):
            return levels[1]
        elif any(word in desc_lower for word in ['interdicción', 'strike']):
            return levels[2]
        elif any(word in desc_lower for word in ['reconocimiento', 'isr']):
            return levels[3]

    return levels[0]


# ============================================================================
# MÓDULO 3.5: INGESTA REAL DE DATOS (v5.0)
# ============================================================================

def clasificar_partida_inteligente(codigo: str, descripcion: str, unidad: str) -> Tuple[str, str]:
    """
    FUNCIÓN DE DESAMBIGUACIÓN INTELIGENTE (v5.0)

    Clasifica una partida presupuestaria en:
    1. Capacidad estratégica (C2, MANIOBRA, CIBERDEFENSA, LOGISTICA)
    2. Tag DOTMLPF (D, O, T, M, L, P, F)

    Reglas de negocio:
    - Primero intenta clasificar por keywords en descripción
    - Si hay ambigüedad, desempata por unidad beneficiaria
    - Si sigue ambiguo, usa código presupuestario como fallback

    Args:
        codigo: Código presupuestario eSIGEF (ej: '710101')
        descripcion: Descripción de la partida
        unidad: Unidad beneficiaria

    Returns:
        Tuple (capacidad, tag_dotmlpf)
    """

    desc_lower = descripcion.lower()
    unidad_lower = unidad.lower()

    # PASO 1: Clasificación de CAPACIDAD por keywords con scoring
    capability_scores = {cap: 0 for cap in CAPABILITY_KEYWORDS.keys()}

    for cap, keywords in CAPABILITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in desc_lower:
                capability_scores[cap] += 1

    # PASO 2: Desempate por unidad beneficiaria
    # Unidades de C2
    c2_units = ['coa', 'cos-1', 'cos-2', 'cociber', 'inteligencia', 'spoc', 'comando']
    # Unidades de MANIOBRA
    maniobra_units = ['ala de combate', 'ala de transporte', 'grupo aéreo', 'esma', 'escuadrón']

    if capability_scores['C2'] == capability_scores['MANIOBRA'] == 0:
        # No hay keywords, decidir por unidad
        if any(unit_key in unidad_lower for unit_key in c2_units):
            capability_scores['C2'] = 10
        elif any(unit_key in unidad_lower for unit_key in maniobra_units):
            capability_scores['MANIOBRA'] = 10

    elif capability_scores['C2'] == capability_scores['MANIOBRA'] and capability_scores['C2'] > 0:
        # Empate con keywords, usar unidad como desempate
        if any(unit_key in unidad_lower for unit_key in maniobra_units):
            capability_scores['MANIOBRA'] += 5
        elif any(unit_key in unidad_lower for unit_key in c2_units):
            capability_scores['C2'] += 5

    # Determinar capacidad ganadora
    max_score = max(capability_scores.values())
    if max_score == 0:
        capacidad = 'C2'  # Default
    else:
        capacidad = max(capability_scores, key=capability_scores.get)

    # PASO 3: Clasificación de DOTMLPF por código presupuestario
    codigo_prefix = codigo[:2] if len(codigo) >= 2 else ''
    tag_dotmlpf = BUDGET_CODE_MAPPING.get(codigo_prefix, 'O')  # Default: Organization

    # Refinamiento por keywords si es necesario
    if tag_dotmlpf == 'O':  # Si el código no fue específico, usar keywords
        if any(word in desc_lower for word in ['capacitación', 'curso', 'entrenamiento', 'simulador']):
            tag_dotmlpf = 'T'
        elif any(word in desc_lower for word in ['repuesto', 'aeronave', 'munición', 'equipo', 'material']):
            tag_dotmlpf = 'M'
        elif any(word in desc_lower for word in ['personal', 'sueldo', 'bonificación', 'tripulación']):
            tag_dotmlpf = 'P'
        elif any(word in desc_lower for word in ['infraestructura', 'construcción', 'pista', 'hangar']):
            tag_dotmlpf = 'F'
        elif any(word in desc_lower for word in ['doctrina', 'estudio', 'investigación']):
            tag_dotmlpf = 'D'

    return capacidad, tag_dotmlpf


def procesar_excel_esigef(uploaded_file) -> pd.DataFrame:
    """
    Procesa archivo Excel de eSIGEF con normalización de columnas.

    Normaliza nombres de columnas que pueden variar:
    - 'Código' / 'Codigo' / 'Cod_Presupuestario' → 'Codigo_Presupuestario'
    - 'Descripción' / 'Descripcion' / 'Detalle' → 'Descripcion'
    - 'Asignado' / 'Monto_Asignado' / 'Presupuesto' → 'Monto_Asignado'
    - 'Ejecutado' / 'Monto_Ejecutado' / 'Devengado' → 'Monto_Ejecutado'
    - 'Unidad' / 'Unidad_Beneficiaria' / 'Beneficiario' → 'Unidad_Beneficiaria'

    Args:
        uploaded_file: Archivo Excel cargado por st.file_uploader

    Returns:
        DataFrame normalizado con columnas estándar
    """

    if not OPENPYXL_AVAILABLE:
        st.error("❌ openpyxl no está instalado. No se pueden procesar archivos Excel.")
        return pd.DataFrame()

    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Mapeo de columnas posibles
        column_mapping = {
            'Codigo_Presupuestario': ['Código', 'Codigo', 'Cod_Presupuestario', 'CodPresup', 'Partida'],
            'Descripcion': ['Descripción', 'Descripcion', 'Detalle', 'Desc', 'Concepto'],
            'Monto_Asignado': ['Asignado', 'Monto_Asignado', 'Presupuesto', 'Asignacion', 'Codificado'],
            'Monto_Ejecutado': ['Ejecutado', 'Monto_Ejecutado', 'Devengado', 'Ejecucion'],
            'Unidad_Beneficiaria': ['Unidad', 'Unidad_Beneficiaria', 'Beneficiario', 'Dependencia']
        }

        # Normalizar nombres
        normalized_df = pd.DataFrame()

        for target_col, possible_names in column_mapping.items():
            for possible_name in possible_names:
                if possible_name in df.columns:
                    normalized_df[target_col] = df[possible_name]
                    break

        # Validar que se encontraron las columnas críticas
        required_cols = ['Codigo_Presupuestario', 'Descripcion', 'Monto_Asignado', 'Unidad_Beneficiaria']
        missing_cols = [col for col in required_cols if col not in normalized_df.columns]

        if missing_cols:
            st.error(f"❌ Columnas requeridas no encontradas en Excel: {', '.join(missing_cols)}")
            st.info("💡 Columnas encontradas en el archivo: " + ", ".join(df.columns))
            return pd.DataFrame()

        # Crear columna Monto_Ejecutado si no existe
        if 'Monto_Ejecutado' not in normalized_df.columns:
            normalized_df['Monto_Ejecutado'] = normalized_df['Monto_Asignado'] * 0.75  # Estimado 75%

        # Aplicar clasificación inteligente a cada fila
        clasificaciones = normalized_df.apply(
            lambda row: clasificar_partida_inteligente(
                str(row['Codigo_Presupuestario']),
                str(row['Descripcion']),
                str(row['Unidad_Beneficiaria'])
            ),
            axis=1
        )

        normalized_df['Capacidad'] = clasificaciones.apply(lambda x: x[0])
        normalized_df['DOTMLPF_Tag'] = clasificaciones.apply(lambda x: x[1])

        # Agregar campos adicionales
        normalized_df['Fecha'] = datetime.now()
        normalized_df['Tipo_Recurso'] = normalized_df['Codigo_Presupuestario'].apply(
            lambda x: 'Inversión' if str(x).startswith(('71', '84', '75')) else 'Gasto'
        )
        normalized_df['ID_Partida'] = [f"EXT-{i+1:04d}" for i in range(len(normalized_df))]

        return normalized_df

    except Exception as e:
        st.error(f"❌ Error al procesar Excel: {str(e)}")
        return pd.DataFrame()


def extraer_texto_pdf(uploaded_file) -> str:
    """
    Extrae texto de un PDF usando pdfplumber.

    Args:
        uploaded_file: Archivo PDF cargado por st.file_uploader

    Returns:
        String con el texto extraído
    """

    if not PDFPLUMBER_AVAILABLE:
        st.error("❌ pdfplumber no está instalado. No se pueden procesar PDFs.")
        return ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"❌ Error al extraer texto de PDF: {str(e)}")
        return ""


def procesar_pdfs_reportes(uploaded_files, capability: str) -> pd.DataFrame:
    """
    Procesa múltiples PDFs de reportes operativos.

    Args:
        uploaded_files: Lista de archivos PDF
        capability: Capacidad estratégica seleccionada

    Returns:
        DataFrame con reportes procesados
    """

    if not uploaded_files:
        return pd.DataFrame()

    reports = []

    for idx, pdf_file in enumerate(uploaded_files):
        texto = extraer_texto_pdf(pdf_file)

        if texto:
            # Determinar unidad del texto
            unidad = "Unidad No Especificada"
            for unit in MILITARY_UNITS:
                if unit.lower() in texto.lower():
                    unidad = unit
                    break

            reports.append({
                'Report_ID': f'PDF-{idx+1:03d}',
                'Fuente': pdf_file.name,
                'Unidad_Origen': unidad,
                'Texto_Reporte': texto[:1000],  # Primeros 1000 caracteres
                'Fecha_Reporte': datetime.now(),
                'Capacidad': capability
            })

    if reports:
        return pd.DataFrame(reports)
    else:
        return pd.DataFrame()


def conectar_base_institucional():
    """
    PLACEHOLDER: Conector a base de datos institucional.

    En producción, esta función se conectaría a la base de datos
    del sistema eSIGEF institucional usando SQLAlchemy.

    Ejemplo de implementación:

    ```python
    from sqlalchemy import create_engine
    import os

    # Configuración desde variables de entorno
    db_host = os.getenv('SIEC_DB_HOST', 'localhost')
    db_port = os.getenv('SIEC_DB_PORT', '5432')
    db_name = os.getenv('SIEC_DB_NAME', 'esigef')
    db_user = os.getenv('SIEC_DB_USER', 'readonly_user')
    db_pass = os.getenv('SIEC_DB_PASSWORD', '')

    # Crear conexión
    engine = create_engine(
        f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    )

    # Consulta SQL
    query = '''
        SELECT
            codigo_presupuestario,
            descripcion,
            monto_asignado,
            monto_ejecutado,
            unidad_beneficiaria,
            fecha_registro
        FROM partidas_presupuestarias
        WHERE ano_fiscal = 2024
            AND estado = 'ACTIVO'
    '''

    # Leer datos
    df = pd.read_sql(query, engine)

    # Aplicar clasificación inteligente
    clasificaciones = df.apply(
        lambda row: clasificar_partida_inteligente(
            row['codigo_presupuestario'],
            row['descripcion'],
            row['unidad_beneficiaria']
        ),
        axis=1
    )

    df['Capacidad'] = clasificaciones.apply(lambda x: x[0])
    df['DOTMLPF_Tag'] = clasificaciones.apply(lambda x: x[1])

    return df
    ```

    Configuración de seguridad:
    - Usar credenciales read-only
    - Conexión SSL/TLS obligatoria
    - IP whitelisting
    - Auditoría de accesos
    """

    st.info("""
        💡 **CONECTOR DE BASE DE DATOS (Placeholder)**

        Esta función está preparada para conectarse a:
        - PostgreSQL (eSIGEF institucional)
        - Oracle (Sistemas legacy)
        - SQL Server (Integración interagencias)

        Requiere configuración de:
        - Variables de entorno (DB_HOST, DB_USER, DB_PASSWORD)
        - Credenciales read-only
        - Certificados SSL/TLS
        - Whitelisting de IPs
    """)

    return None


# ============================================================================
# MÓDULO 4: MOTOR NLP
# ============================================================================

def analyze_sentiment_readiness(text: str) -> Dict[str, any]:
    """Motor NLP para análisis de riesgo operacional."""
    text_lower = text.lower()
    risk_score = 0
    detected_issues = []
    sentiment = 'neutral'

    for keyword, score in RISK_KEYWORDS.items():
        if keyword in text_lower:
            risk_score = max(risk_score, score)
            detected_issues.append(keyword)

    for pos_keyword in POSITIVE_KEYWORDS:
        if pos_keyword in text_lower:
            risk_score = max(0, risk_score - 30)
            sentiment = 'positive'
            break

    if risk_score >= 70:
        sentiment = 'critical'
    elif risk_score >= 50:
        sentiment = 'warning'
    elif risk_score > 0:
        sentiment = 'caution'
    elif 'óptim' in text_lower or 'excelente' in text_lower:
        sentiment = 'positive'

    return {
        'risk_score': risk_score,
        'sentiment': sentiment,
        'issues_detected': ', '.join(detected_issues) if detected_issues else 'Ninguno',
        'readiness_index': 100 - risk_score
    }


# ============================================================================
# MÓDULO 5: MAPEO DOTMLPF
# ============================================================================

def map_dotmlpf(codigo: str, descripcion: str) -> str:
    """Mapea código presupuestario a componente DOTMLPF."""
    codigo_base = codigo[:2]
    if codigo_base in BUDGET_CODE_MAPPING:
        return BUDGET_CODE_MAPPING[codigo_base]

    desc_lower = descripcion.lower()
    if 'doctrina' in desc_lower or 'estudio' in desc_lower:
        return 'D'
    elif 'organización' in desc_lower or 'asesoría' in desc_lower:
        return 'O'
    elif 'curso' in desc_lower or 'capacitación' in desc_lower or 'entrenamiento' in desc_lower:
        return 'T'
    elif 'equipo' in desc_lower or 'material' in desc_lower or 'repuesto' in desc_lower:
        return 'M'
    elif 'liderazgo' in desc_lower or 'comando' in desc_lower:
        return 'L'
    elif 'personal' in desc_lower or 'sueldo' in desc_lower or 'tripulación' in desc_lower:
        return 'P'
    elif 'infraestructura' in desc_lower or 'construcción' in desc_lower or 'instalación' in desc_lower:
        return 'F'
    else:
        return 'O'


# ============================================================================
# MÓDULO 6: CÁLCULO DE MÉTRICAS CON SCORING PONDERADO (v4.0)
# ============================================================================

def calculate_weighted_dotmlpf_scores(df_budget: pd.DataFrame, weights: Dict[str, float]) -> pd.DataFrame:
    """
    Calcula scores DOTMLPF ponderados por unidad.

    Args:
        df_budget: DataFrame de presupuesto
        weights: Diccionario de pesos DOTMLPF

    Returns:
        DataFrame con scores por componente
    """

    # Agrupar por unidad y componente DOTMLPF
    dotmlpf_by_unit = df_budget.groupby(['Unidad_Beneficiaria', 'DOTMLPF_Tag']).agg({
        'Monto_Asignado': 'sum',
        'Monto_Ejecutado': 'sum'
    }).reset_index()

    # Calcular % ejecución por componente
    dotmlpf_by_unit['Ejecucion_Componente'] = (
        dotmlpf_by_unit['Monto_Ejecutado'] / dotmlpf_by_unit['Monto_Asignado'] * 100
    ).fillna(0).round(2)

    return dotmlpf_by_unit


def calculate_quality_metrics(df_budget: pd.DataFrame, df_reports: pd.DataFrame,
                              weights: Dict[str, float]) -> pd.DataFrame:
    """
    Calcula KPIs con scoring ponderado estratégico (v4.0).

    Args:
        df_budget: DataFrame de presupuesto
        df_reports: DataFrame de reportes con análisis NLP
        weights: Pesos DOTMLPF estratégicos

    Returns:
        DataFrame con métricas agregadas por unidad
    """

    # KPI 1: Ejecución Presupuestaria Global
    budget_metrics = df_budget.groupby('Unidad_Beneficiaria').agg({
        'Monto_Asignado': 'sum',
        'Monto_Ejecutado': 'sum'
    }).reset_index()

    budget_metrics['Ejecucion_Pct'] = (
        budget_metrics['Monto_Ejecutado'] / budget_metrics['Monto_Asignado'] * 100
    ).round(2)

    # KPI 2: Scoring DOTMLPF Ponderado
    dotmlpf_scores = calculate_weighted_dotmlpf_scores(df_budget, weights)

    # Calcular score ponderado por unidad
    weighted_scores = []
    for unit in budget_metrics['Unidad_Beneficiaria'].unique():
        unit_data = dotmlpf_scores[dotmlpf_scores['Unidad_Beneficiaria'] == unit]

        # Calcular score ponderado
        total_weighted_score = 0
        for component in DOTMLPF_TAXONOMY.keys():
            comp_data = unit_data[unit_data['DOTMLPF_Tag'] == component]
            if len(comp_data) > 0:
                comp_score = comp_data['Ejecucion_Componente'].values[0]
            else:
                comp_score = 0

            weight = weights.get(component, 0)
            total_weighted_score += comp_score * weight

        weighted_scores.append({
            'Unidad_Beneficiaria': unit,
            'Alistamiento_Ponderado': round(total_weighted_score, 2)
        })

    weighted_df = pd.DataFrame(weighted_scores)

    # KPI 3: Alistamiento desde reportes NLP
    readiness_metrics = df_reports.groupby('Unidad').agg({
        'readiness_index': 'mean',
        'risk_score': 'mean'
    }).reset_index()

    readiness_metrics.rename(columns={'Unidad': 'Unidad_Beneficiaria'}, inplace=True)
    readiness_metrics['Alistamiento_NLP'] = readiness_metrics['readiness_index'].round(2)

    # Merge de todas las métricas
    metrics = budget_metrics.merge(weighted_df, on='Unidad_Beneficiaria', how='left')
    metrics = metrics.merge(
        readiness_metrics[['Unidad_Beneficiaria', 'Alistamiento_NLP', 'risk_score']],
        on='Unidad_Beneficiaria',
        how='left'
    )

    # Rellenar NaN
    metrics['Alistamiento_Ponderado'] = metrics['Alistamiento_Ponderado'].fillna(
        metrics['Alistamiento_Ponderado'].mean()
    )
    metrics['Alistamiento_NLP'] = metrics['Alistamiento_NLP'].fillna(
        metrics['Alistamiento_NLP'].mean()
    )
    metrics['risk_score'] = metrics['risk_score'].fillna(metrics['risk_score'].mean())

    # Alistamiento combinado (70% ponderado + 30% NLP)
    metrics['Alistamiento_Pct'] = (
        metrics['Alistamiento_Ponderado'] * 0.7 + metrics['Alistamiento_NLP'] * 0.3
    ).round(2)

    # Clasificación en cuadrantes
    def classify_quadrant(row):
        ejec = row['Ejecucion_Pct']
        alist = row['Alistamiento_Pct']

        if ejec > 80 and alist > 80:
            return 'Eficiente'
        elif ejec > 80 and alist < 50:
            return 'Ineficiente (Auditar)'
        elif ejec < 50 and alist > 80:
            return 'Sub-Ejecución'
        else:
            return 'Crítico'

    metrics['Cuadrante'] = metrics.apply(classify_quadrant, axis=1)

    return metrics


def create_dotmlpf_matrix(df_budget: pd.DataFrame, weights: Dict[str, float]) -> pd.DataFrame:
    """
    Crea matriz DOTMLPF con valores ponderados.

    Args:
        df_budget: DataFrame de presupuesto
        weights: Pesos estratégicos

    Returns:
        DataFrame pivote con valores ponderados
    """

    # Calcular monto ponderado
    df_budget_weighted = df_budget.copy()
    df_budget_weighted['Monto_Ponderado'] = df_budget_weighted.apply(
        lambda row: row['Monto_Ejecutado'] * weights.get(row['DOTMLPF_Tag'], 0),
        axis=1
    )

    matrix = df_budget_weighted.pivot_table(
        index='Operational_Level',
        columns='DOTMLPF_Tag',
        values='Monto_Ponderado',
        aggfunc='sum',
        fill_value=0
    )

    # Asegurar columnas DOTMLPF
    for letter in DOTMLPF_TAXONOMY.keys():
        if letter not in matrix.columns:
            matrix[letter] = 0

    matrix = matrix[list(DOTMLPF_TAXONOMY.keys())]

    return matrix


# ============================================================================
# MÓDULO 7: PROCESAMIENTO PRINCIPAL (ETL + ENRIQUECIMIENTO) - v5.0
# ============================================================================

def load_and_process_data(
    capability: str,
    mode: str = 'simulation',
    uploaded_excel=None,
    uploaded_pdfs=None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Pipeline principal con soporte para Simulación e Ingesta Real (v5.0).

    Args:
        capability: Capacidad estratégica seleccionada
        mode: 'simulation' o 'ingestion'
        uploaded_excel: Archivo Excel cargado (modo ingestion)
        uploaded_pdfs: Lista de PDFs cargados (modo ingestion)

    Returns:
        Tuple (df_budget, df_reports)
    """

    if mode == 'simulation':
        # MODO SIMULACIÓN (v4.0 backward compatible)
        df_budget = generate_structured_data(capability)
        df_reports = generate_unstructured_data(capability)

    else:
        # MODO INGESTA REAL (v5.0)
        if uploaded_excel is not None:
            df_budget = procesar_excel_esigef(uploaded_excel)

            # Filtrar por capacidad seleccionada
            if not df_budget.empty:
                df_budget = df_budget[df_budget['Capacidad'] == capability].copy()

            if df_budget.empty:
                st.warning(f"⚠️ No se encontraron partidas para la capacidad {capability} en el archivo Excel.")
                df_budget = generate_structured_data(capability)  # Fallback a simulación
        else:
            st.warning("⚠️ No se cargó archivo Excel. Usando datos simulados.")
            df_budget = generate_structured_data(capability)

        if uploaded_pdfs is not None and len(uploaded_pdfs) > 0:
            df_reports = procesar_pdfs_reportes(uploaded_pdfs, capability)

            if df_reports.empty:
                st.warning("⚠️ No se pudieron procesar los PDFs. Usando reportes simulados.")
                df_reports = generate_unstructured_data(capability)
        else:
            st.info("💡 No se cargaron PDFs. Usando reportes simulados.")
            df_reports = generate_unstructured_data(capability)

    # Enriquecimiento común para ambos modos
    if not df_budget.empty:
        df_budget['Operational_Level'] = df_budget.apply(
            lambda row: classify_operational_level(row['Descripcion'], row['Capacidad']),
            axis=1
        )

    if not df_reports.empty:
        nlp_results = df_reports['Texto_Reporte'].apply(analyze_sentiment_readiness)
        df_reports['risk_score'] = nlp_results.apply(lambda x: x['risk_score'])
        df_reports['sentiment'] = nlp_results.apply(lambda x: x['sentiment'])
        df_reports['issues_detected'] = nlp_results.apply(lambda x: x['issues_detected'])
        df_reports['readiness_index'] = nlp_results.apply(lambda x: x['readiness_index'])

    return df_budget, df_reports


# ============================================================================
# MÓDULO 8: VISUALIZACIONES CON VALORES PONDERADOS (v4.0)
# ============================================================================

def render_dotmlpf_heatmap(df_budget: pd.DataFrame, weights: Dict[str, float]):
    """Heatmap con valores ponderados estratégicos."""

    matrix = create_dotmlpf_matrix(df_budget, weights)

    # Crear anotaciones
    annotations = []
    for i, row_label in enumerate(matrix.index):
        for j, col_label in enumerate(matrix.columns):
            value = matrix.iloc[i, j]
            weight = weights.get(col_label, 0)

            if value > 0:
                text = f'${value/1000:.0f}K<br>W:{weight*100:.1f}%'
                color = 'white'
            else:
                text = 'GAP'
                color = 'red'

            annotations.append(
                dict(
                    x=f"{col_label} - {DOTMLPF_TAXONOMY[col_label]}",
                    y=row_label,
                    text=text,
                    showarrow=False,
                    font=dict(color=color, size=9)
                )
            )

    fig = go.Figure(data=go.Heatmap(
        z=matrix.values,
        x=[f"{k} - {v}" for k, v in DOTMLPF_TAXONOMY.items()],
        y=matrix.index,
        colorscale='Viridis',
        colorbar=dict(title="USD Ponderado", tickprefix="$", tickformat=",.0f")
    ))

    fig.update_layout(
        title='MATRIZ DOTMLPF PONDERADA<br><sub>Inversión Ponderada por Pesos Estratégicos (USD)</sub>',
        xaxis_title="Componentes DOTMLPF (con pesos aplicados)",
        yaxis_title="Niveles Operacionales",
        template='plotly_dark',
        height=500,
        annotations=annotations
    )

    st.plotly_chart(fig, use_container_width=True)


def render_radar_chart(df_budget: pd.DataFrame, weights: Dict[str, float]):
    """Radar Chart con líneas de referencia de pesos."""

    dotmlpf_totals = df_budget.groupby('DOTMLPF_Tag')['Monto_Ejecutado'].sum()
    dotmlpf_normalized = (dotmlpf_totals / dotmlpf_totals.max() * 100).round(2)

    categories = [f"{k} - {DOTMLPF_TAXONOMY[k]}" for k in DOTMLPF_TAXONOMY.keys()]
    values = [dotmlpf_normalized.get(k, 0) for k in DOTMLPF_TAXONOMY.keys()]

    # Valores de pesos estratégicos (normalizados a 100)
    weight_values = [weights.get(k, 0) * 100 for k in DOTMLPF_TAXONOMY.keys()]

    fig = go.Figure()

    # Inversión real
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Inversión Real',
        line=dict(color='cyan', width=2),
        fillcolor='rgba(0,255,255,0.3)'
    ))

    # Pesos estratégicos (referencia)
    fig.add_trace(go.Scatterpolar(
        r=weight_values,
        theta=categories,
        fill='toself',
        name='Pesos Estratégicos',
        line=dict(color='yellow', width=2, dash='dash'),
        fillcolor='rgba(255,255,0,0.1)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], ticksuffix='%'),
            bgcolor='rgba(20,20,20,0.5)'
        ),
        title='BALANCE DOTMLPF CON PESOS ESTRATÉGICOS<br><sub>Inversión Real vs Pesos Planificados</sub>',
        template='plotly_dark',
        height=500,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)


def render_efficiency_matrix(df_metrics: pd.DataFrame):
    """Scatter Plot de Calidad del Gasto con scoring ponderado."""

    color_map = {
        'Eficiente': 'green',
        'Ineficiente (Auditar)': 'red',
        'Sub-Ejecución': 'gray',
        'Crítico': 'darkred'
    }

    fig = px.scatter(
        df_metrics,
        x='Ejecucion_Pct',
        y='Alistamiento_Pct',
        size='Monto_Ejecutado',
        color='Cuadrante',
        hover_name='Unidad_Beneficiaria',
        hover_data={
            'Monto_Ejecutado': ':$,.0f',
            'Ejecucion_Pct': ':.1f%',
            'Alistamiento_Pct': ':.1f% (Ponderado)',
            'Alistamiento_Ponderado': ':.1f%',
            'Alistamiento_NLP': ':.1f%'
        },
        color_discrete_map=color_map,
        template='plotly_dark'
    )

    fig.add_hline(y=80, line_dash="dash", line_color="yellow", opacity=0.5)
    fig.add_hline(y=50, line_dash="dash", line_color="orange", opacity=0.5)
    fig.add_vline(x=80, line_dash="dash", line_color="yellow", opacity=0.5)
    fig.add_vline(x=50, line_dash="dash", line_color="orange", opacity=0.5)

    fig.update_layout(
        title='MATRIZ DE CALIDAD DEL GASTO (Scoring Ponderado v4.0)',
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# MÓDULO 9: LANDING PAGE
# ============================================================================

def render_landing_page():
    """Pantalla inicial de selección de capacidad estratégica."""

    st.markdown("""
        <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #000428 0%, #004e92 100%); border-radius: 15px; margin-bottom: 40px;'>
            <h1 style='margin: 0; font-size: 56px; color: #00D9FF;'>⚔️ SIEC v4.0</h1>
            <p style='color: #FFD700; font-size: 24px; margin: 15px 0;'>
                Sistema Integrado de Evaluación de Capacidades
            </p>
            <p style='color: #AAAAAA; font-size: 14px; margin: 5px 0;'>
                Arquitectura Modular Multicapacidad | Weighted Strategic Scoring
            </p>
            <p style='color: #00D9FF; font-size: 12px; margin: 10px 0;'>
                NATO DOTMLPF Framework | Real OOB FAE | NLP Intelligence
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #FFD700;'>📊 SELECCIONE CAPACIDAD ESTRATÉGICA</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(2)

    for idx, (cap_key, cap_info) in enumerate(STRATEGIC_CAPABILITIES.items()):
        with cols[idx % 2]:
            is_operational = cap_info['status'] == 'operational'

            if is_operational:
                button_style = "background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: white; padding: 30px; border-radius: 10px; border: 2px solid #00D9FF; cursor: pointer;"
            else:
                button_style = "background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); color: #666; padding: 30px; border-radius: 10px; border: 2px solid #444; cursor: not-allowed;"

            st.markdown(f"""
                <div style='{button_style} text-align: center; margin-bottom: 20px;'>
                    <div style='font-size: 48px; margin-bottom: 10px;'>{cap_info['icon']}</div>
                    <h3 style='margin: 10px 0;'>{cap_info['name']}</h3>
                    <p style='font-size: 12px; margin: 10px 0;'>{cap_info['description']}</p>
                    <p style='font-size: 10px; margin-top: 15px; opacity: 0.7;'>
                        {'✅ OPERACIONAL' if is_operational else '🚧 EN DESARROLLO'}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            if is_operational:
                if st.button(f"🎯 ANALIZAR {cap_info['name']}", key=f"btn_{cap_key}", use_container_width=True):
                    st.session_state.page = 'dashboard'
                    st.session_state.selected_capability = cap_key
                    st.rerun()
            else:
                st.button(f"🔒 {cap_info['name']} (Próximamente)", key=f"btn_{cap_key}", disabled=True, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 11px; padding: 20px; border-top: 1px solid #333;'>
            <b>SIEC Defense Analytics Platform v5.0</b> | Real Data Ingestion + Intelligent Classification<br>
            Real OOB FAE (15 Units) | Excel ETL + PDF Processing | NATO UNCLASSIFIED<br>
            <i>Sistema de Evaluación Estratégica con Ingesta Real de Datos Institucionales</i>
        </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MÓDULO 10: DASHBOARD CON CONTROLES DE PESOS (v4.0)
# ============================================================================

def render_dashboard(capability: str):
    """Dashboard con controles de pesos DOTMLPF estratégicos."""

    cap_info = STRATEGIC_CAPABILITIES[capability]

    st.set_page_config(
        page_title=f"SIEC v5.0 | {cap_info['name']}",
        page_icon=cap_info['icon'],
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        .main {background-color: #0E1117;}
        h1 {color: #00D9FF; font-family: 'Arial Black', sans-serif;}
        h2 {color: #FFD700; border-bottom: 2px solid #FFD700; padding-bottom: 10px;}
        h3 {color: #00FF00;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #000428 0%, #004e92 100%); border-radius: 10px;'>
            <h1 style='margin: 0; font-size: 42px;'>{cap_info['icon']} {cap_info['name']}</h1>
            <p style='color: #00D9FF; font-size: 16px; margin: 10px 0;'>
                {cap_info['description']}
            </p>
            <p style='color: #FFD700; font-size: 11px; margin: 5px 0;'>
                SIEC v5.0 | Real Data Ingestion + Weighted DOTMLPF Analysis | OOB FAE Real
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sidebar con controles de modo y pesos (v5.0)
    with st.sidebar:
        st.markdown(f"## {cap_info['icon']} {cap_info['name']}")
        st.markdown("---")

        # SELECTOR DE MODO (v5.0)
        st.markdown("### 🔧 MODO DE OPERACIÓN")
        mode = st.radio(
            "Seleccione modo de datos:",
            options=['🛠️ MODO SIMULACIÓN (Demo)', '📂 MODO INGESTA DE DATOS (Real)'],
            index=0,
            key='mode_selector',
            help="Simulación: datos generados automáticamente. Ingesta: cargar archivos Excel y PDF."
        )

        mode_value = 'simulation' if '🛠️' in mode else 'ingestion'

        st.markdown("---")

        # FILE UPLOADERS (v5.0) - Solo en modo ingesta
        uploaded_excel = None
        uploaded_pdfs = None

        if mode_value == 'ingestion':
            st.markdown("### 📂 CARGA DE ARCHIVOS")

            st.markdown("**1. Presupuesto (Excel eSIGEF)**")
            uploaded_excel = st.file_uploader(
                "Archivo Excel con partidas presupuestarias",
                type=['xlsx', 'xls'],
                key='excel_uploader',
                help="Columnas esperadas: Código, Descripción, Asignado, Ejecutado, Unidad"
            )

            if uploaded_excel:
                st.success(f"✅ {uploaded_excel.name}")

            st.markdown("**2. Reportes (PDFs Operativos)**")
            uploaded_pdfs = st.file_uploader(
                "Reportes operativos en PDF (múltiples)",
                type=['pdf'],
                accept_multiple_files=True,
                key='pdf_uploader',
                help="Pueden ser novedades, informes de mantenimiento, reportes de novedades, etc."
            )

            if uploaded_pdfs:
                st.success(f"✅ {len(uploaded_pdfs)} archivo(s) cargado(s)")
                for pdf in uploaded_pdfs:
                    st.text(f"  • {pdf.name}")

            # Información del conector DB (placeholder)
            with st.expander("💾 CONECTOR BD (Configuración Avanzada)"):
                if st.button("ℹ️ Ver Info Conector BD", key="db_info"):
                    conectar_base_institucional()

            st.markdown("---")

        if st.button("⬅️ VOLVER AL INICIO", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.selected_capability = None
            st.rerun()

        st.markdown("---")

    # Cargar datos según modo seleccionado (v5.0)
    with st.spinner(f'🔄 Procesando datos de {cap_info["name"]} ({mode_value.upper()})...'):
        df_budget, df_reports = load_and_process_data(
            capability,
            mode=mode_value,
            uploaded_excel=uploaded_excel,
            uploaded_pdfs=uploaded_pdfs
        )

    # Continuar con sidebar - controles de pesos
    with st.sidebar:

        # CONTROLES DE PESOS ESTRATÉGICOS (v4.0)
        with st.expander("⚙️ CONFIGURACIÓN ESTRATÉGICA (PESOS DOTMLPF)", expanded=False):
            st.markdown("**Ajuste de Pesos por Componente:**")
            st.markdown("<small>Modifique los pesos según prioridades estratégicas</small>", unsafe_allow_html=True)

            weights = {}
            weight_sum = 0

            for component, full_name in DOTMLPF_TAXONOMY.items():
                default_weight = DEFAULT_DOTMLPF_WEIGHTS.get(component, 0.0)

                weight_pct = st.slider(
                    f"{component} - {full_name}",
                    min_value=0.0,
                    max_value=100.0,
                    value=default_weight * 100,
                    step=0.1,
                    key=f"weight_{component}",
                    help=f"Peso estratégico para {full_name}"
                )

                weights[component] = weight_pct / 100
                weight_sum += weight_pct

            # Validación de pesos
            if abs(weight_sum - 100.0) > 0.1:
                st.warning(f"⚠️ La suma de pesos es {weight_sum:.1f}%. Debe ser 100%.")
                st.markdown(f"**Diferencia:** {weight_sum - 100:.1f}%")
            else:
                st.success(f"✅ Pesos válidos: {weight_sum:.1f}%")

            if st.button("🔄 Restaurar Pesos Default", use_container_width=True):
                st.rerun()

        st.markdown("---")
        st.markdown("### 📊 MÉTRICAS EJECUTIVAS")

        # Calcular métricas con pesos actuales
        df_metrics = calculate_quality_metrics(df_budget, df_reports, weights)

        total_asignado = df_budget['Monto_Asignado'].sum()
        total_ejecutado = df_budget['Monto_Ejecutado'].sum()
        ejecucion_global = (total_ejecutado / total_asignado * 100)
        alistamiento_promedio = df_metrics['Alistamiento_Pct'].mean()

        st.metric("Presupuesto Asignado", f"${total_asignado:,.0f}")
        st.metric("Presupuesto Ejecutado", f"${total_ejecutado:,.0f}", delta=f"{ejecucion_global:.1f}%")
        st.metric("Alistamiento Ponderado", f"{alistamiento_promedio:.1f}%",
                 help="Calculado con pesos DOTMLPF estratégicos")

        st.markdown("---")
        st.markdown("### 🔍 FILTROS")

        selected_units = st.multiselect(
            "Unidades FAE",
            options=df_budget['Unidad_Beneficiaria'].unique(),
            default=df_budget['Unidad_Beneficiaria'].unique(),
            help="Orden de Batalla real FAE"
        )

    # Aplicar filtros
    df_budget_filtered = df_budget[df_budget['Unidad_Beneficiaria'].isin(selected_units)]
    df_metrics_filtered = df_metrics[df_metrics['Unidad_Beneficiaria'].isin(selected_units)]

    # TABS
    tab1, tab2, tab3 = st.tabs([
        "🎯 SITUATIONAL AWARENESS",
        "💰 GOBERNANZA & CALIDAD",
        "🧠 DATA INTELLIGENCE"
    ])

    # TAB 1
    with tab1:
        st.markdown("## 🎯 ANÁLISIS DOTMLPF PONDERADO")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Partidas Analizadas", len(df_budget_filtered))
        with col2:
            st.metric("Inversión Total", f"${df_budget_filtered['Monto_Ejecutado'].sum():,.0f}")
        with col3:
            matrix = create_dotmlpf_matrix(df_budget_filtered, weights)
            gaps = (matrix == 0).sum().sum()
            st.metric("Gaps Detectados", gaps, delta="Requieren atención", delta_color="inverse")

        st.markdown("---")

        render_dotmlpf_heatmap(df_budget_filtered, weights)

        st.markdown("---")

        col_radar, col_table = st.columns(2)

        with col_radar:
            render_radar_chart(df_budget_filtered, weights)

        with col_table:
            st.markdown("### 📋 TOP 10 PARTIDAS")
            top_partidas = df_budget_filtered.nlargest(10, 'Monto_Ejecutado')[
                ['Descripcion', 'Unidad_Beneficiaria', 'Monto_Ejecutado', 'DOTMLPF_Tag']
            ]
            st.dataframe(
                top_partidas.style.format({'Monto_Ejecutado': '${:,.0f}'}),
                use_container_width=True,
                height=400
            )

    # TAB 2
    with tab2:
        st.markdown("## 💰 GOBERNANZA FINANCIERA (Scoring Ponderado)")

        cuadrante_counts = df_metrics_filtered['Cuadrante'].value_counts()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Eficientes", cuadrante_counts.get('Eficiente', 0))
        with col2:
            st.metric("Auditar", cuadrante_counts.get('Ineficiente (Auditar)', 0))
        with col3:
            st.metric("Sub-Ejecución", cuadrante_counts.get('Sub-Ejecución', 0))
        with col4:
            st.metric("Críticos", cuadrante_counts.get('Crítico', 0))

        st.markdown("---")

        render_efficiency_matrix(df_metrics_filtered)

        st.markdown("---")

        st.markdown("### 📊 DETALLE DE SCORING PONDERADO")
        st.dataframe(
            df_metrics_filtered[[
                'Unidad_Beneficiaria', 'Ejecucion_Pct', 'Alistamiento_Ponderado',
                'Alistamiento_NLP', 'Alistamiento_Pct', 'Cuadrante'
            ]].style.format({
                'Ejecucion_Pct': '{:.1f}%',
                'Alistamiento_Ponderado': '{:.1f}%',
                'Alistamiento_NLP': '{:.1f}%',
                'Alistamiento_Pct': '{:.1f}%'
            }).background_gradient(subset=['Alistamiento_Pct'], cmap='RdYlGn'),
            use_container_width=True,
            height=400
        )

    # TAB 3
    with tab3:
        st.markdown("## 🧠 INTELIGENCIA DE DATOS (NLP)")

        col1, col2, col3 = st.columns(3)
        critical_reports = len(df_reports[df_reports['sentiment'] == 'critical'])
        positive_reports = len(df_reports[df_reports['sentiment'] == 'positive'])

        with col1:
            st.metric("Reportes Analizados", len(df_reports))
        with col2:
            st.metric("Reportes Críticos", critical_reports, delta="Atención inmediata", delta_color="inverse")
        with col3:
            st.metric("Reportes Positivos", positive_reports)

        st.markdown("---")

        search_term = st.text_input("🔍 Buscar en reportes", placeholder="Ej: repuestos, falla, vuelo...")

        df_reports_display = df_reports.copy()
        if search_term:
            df_reports_display = df_reports_display[
                df_reports_display['Texto_Reporte'].str.contains(search_term, case=False, na=False)
            ]

        st.dataframe(
            df_reports_display[['Report_ID', 'Fecha', 'Unidad', 'Texto_Reporte', 'sentiment', 'risk_score']],
            use_container_width=True,
            height=500
        )


# ============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# ============================================================================

def main():
    """Orquestador principal con navegación por session_state."""

    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    if 'selected_capability' not in st.session_state:
        st.session_state.selected_capability = None

    if st.session_state.page == 'landing':
        render_landing_page()
    elif st.session_state.page == 'dashboard' and st.session_state.selected_capability:
        render_dashboard(st.session_state.selected_capability)
    else:
        st.session_state.page = 'landing'
        st.rerun()


if __name__ == "__main__":
    main()
