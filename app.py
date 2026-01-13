"""
SIEC v3.0: Sistema Integrado de Evaluación de Capacidades
==========================================================
Arquitectura Modular Multicapacidad - POC Funcional End-to-End

Autor: Lead Data Scientist - OTAN Defense Analytics
Arquitectura: Lakehouse Híbrido + Navegación Multicapacidad
Framework: Streamlit + Pandas + Plotly
Versión: 3.0 (Multi-Capability)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from typing import Tuple, Dict, List

# ============================================================================
# CONFIGURACIÓN GLOBAL Y CONSTANTES MILITARES
# ============================================================================

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

# Unidades Militares
MILITARY_UNITS = {
    'C2': [
        'Comando Aéreo de Combate',
        'Centro de Operaciones Conjuntas',
        'Grupo de Guerra Electrónica',
        'Escuadrón de Defensa Aérea',
        'Comando de Ciberdefensa'
    ],
    'MANIOBRA': [
        'Ala de Combate 21 (Taura)',
        'Ala de Combate 22 (Guayaquil)',
        'Ala de Combate 23 (Manta)',
        'Escuadrón de Combate 2111',
        'Escuadrón de Combate 2112',
        'Escuadrón Logístico 21'
    ],
    'CIBERDEFENSA': ['Comando de Ciberdefensa'],
    'LOGISTICA': ['Comando Logístico']
}

# ============================================================================
# MÓDULO 1: GENERACIÓN DE DATOS ESTRUCTURADOS (SQL SIMULADO)
# ============================================================================

def generate_structured_data(capability: str = None) -> pd.DataFrame:
    """
    Simula la ingesta desde eSIGEF (Sistema Financiero Gubernamental).
    Genera partidas presupuestarias específicas por capacidad.

    Args:
        capability: 'C2', 'MANIOBRA', 'CIBERDEFENSA', 'LOGISTICA', o None (todas)

    Returns:
        DataFrame con estructura de presupuesto militar
    """

    np.random.seed(42)
    random.seed(42)

    # ========================================================================
    # PARTIDAS ESPECÍFICAS DE MANDO Y CONTROL (C2)
    # ========================================================================
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

    # ========================================================================
    # PARTIDAS ESPECÍFICAS DE MANIOBRA AÉREA
    # ========================================================================
    maniobra_items = [
        # Personal (P)
        ('Sueldos Pilotos Combate', '510201', 'P', 'MANIOBRA'),
        ('Bonificación Vuelo', '510202', 'P', 'MANIOBRA'),
        ('Tripulación Aerotécnica', '510203', 'P', 'MANIOBRA'),
        ('Personal Mantenimiento Aeronáutico', '510204', 'P', 'MANIOBRA'),

        # Training (T)
        ('Horas de Vuelo Entrenamiento', '530510', 'T', 'MANIOBRA'),
        ('Simulador Full Mission', '530511', 'T', 'MANIOBRA'),
        ('Curso Combate Aéreo Avanzado', '530512', 'T', 'MANIOBRA'),
        ('Entrenamiento Tiro Real', '530513', 'T', 'MANIOBRA'),
        ('Certificación Pilotos Instructores', '530514', 'T', 'MANIOBRA'),
        ('Curso Vuelo Instrumental IFR', '530515', 'T', 'MANIOBRA'),
        ('Entrenamiento Combate Aire-Tierra', '530516', 'T', 'MANIOBRA'),

        # Material (M)
        ('Repuestos Flota Super Tucano', '710401', 'M', 'MANIOBRA'),
        ('Mantenimiento PDM Aeronaves', '710402', 'M', 'MANIOBRA'),
        ('Adquisición Munición Aérea', '840201', 'M', 'MANIOBRA'),
        ('Compra Rotables Críticos', '840202', 'M', 'MANIOBRA'),
        ('Overhaul Motor Turbohélice', '710403', 'M', 'MANIOBRA'),
        ('Sistema Aviónica Modernizado', '840203', 'M', 'MANIOBRA'),
        ('Asientos Eyectables Martin Baker', '840204', 'M', 'MANIOBRA'),
        ('Tren de Aterrizaje Principal', '710404', 'M', 'MANIOBRA'),

        # Operaciones (O)
        ('Combustible Aviación JP1', '530310', 'O', 'MANIOBRA'),
        ('Seguro Casco Aéreo', '530910', 'O', 'MANIOBRA'),
        ('Servicios Meteorológicos', '530311', 'O', 'MANIOBRA'),

        # Infraestructura (F)
        ('Mantenimiento Pista Principal', '750201', 'F', 'MANIOBRA'),
        ('Construcción Hangar Alerta', '750202', 'F', 'MANIOBRA'),
        ('Modernización Torre Control', '750203', 'F', 'MANIOBRA'),
        ('Sistema Iluminación Pista', '750204', 'F', 'MANIOBRA')
    ]

    # ========================================================================
    # CONSOLIDACIÓN Y GENERACIÓN DE REGISTROS
    # ========================================================================

    records = []
    start_date = datetime(2024, 1, 1)

    # Determinar qué items usar según la capacidad
    if capability == 'C2':
        capability_items = c2_items
        num_records = 70
    elif capability == 'MANIOBRA':
        capability_items = maniobra_items
        num_records = 70
    elif capability is None:
        # Todas las capacidades
        capability_items = c2_items + maniobra_items
        num_records = 140
    else:
        # Placeholder para otras capacidades
        capability_items = []
        num_records = 0

    # Generar registros específicos de capacidad
    for i in range(num_records):
        if not capability_items:
            break

        item = random.choice(capability_items)
        item_capability = item[3]
        units_list = MILITARY_UNITS.get(item_capability, MILITARY_UNITS['C2'])
        unit = random.choice(units_list)

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

    # Generar partidas genéricas (10 registros adicionales)
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
        units_list = MILITARY_UNITS.get(cap, MILITARY_UNITS['C2'])
        unit = random.choice(units_list)

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
    Simula reportes operativos de texto libre extraídos de PDFs.
    Representa el componente no estructurado del Lakehouse.

    Args:
        capability: 'C2', 'MANIOBRA', etc., o None (todas)

    Returns:
        DataFrame con reportes de novedades operativas
    """

    random.seed(42)

    # ========================================================================
    # REPORTES DE MANDO Y CONTROL (C2)
    # ========================================================================
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

    # ========================================================================
    # REPORTES DE MANIOBRA AÉREA
    # ========================================================================
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

    # Seleccionar reportes según capacidad
    if capability == 'C2':
        selected_reports = c2_reports
    elif capability == 'MANIOBRA':
        selected_reports = maniobra_reports
    elif capability is None:
        selected_reports = c2_reports + maniobra_reports
    else:
        selected_reports = []

    # Limitar a 50 reportes
    selected_reports = selected_reports[:50]

    records = []
    for i, report_text in enumerate(selected_reports):
        # Determinar capacidad del reporte
        report_capability = classify_capability(report_text)

        units_list = MILITARY_UNITS.get(report_capability, MILITARY_UNITS['C2'])
        unit = random.choice(units_list)
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
    """
    Clasifica una partida o reporte en su capacidad estratégica.

    Args:
        description: Texto a clasificar

    Returns:
        Capacidad ('C2', 'MANIOBRA', etc.)
    """

    desc_lower = description.lower()

    # Scoring por keywords
    scores = {}
    for cap, keywords in CAPABILITY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in desc_lower)
        scores[cap] = score

    # Retornar la capacidad con mayor score
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)

    return 'C2'  # Default


def classify_operational_level(description: str, capability: str) -> str:
    """
    Clasifica en nivel operacional según capacidad.

    Args:
        description: Texto a clasificar
        capability: Capacidad estratégica

    Returns:
        Nivel operacional
    """

    levels = OPERATIONAL_LEVELS.get(capability, OPERATIONAL_LEVELS['C2'])

    # Análisis simple por keywords
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

    return levels[0]  # Default


# ============================================================================
# MÓDULO 4: MOTOR NLP - ANÁLISIS DE SENTIMIENTO Y RIESGO
# ============================================================================

def analyze_sentiment_readiness(text: str) -> Dict[str, any]:
    """
    Motor NLP simplificado para analizar riesgo operacional.

    Args:
        text: Texto del reporte operativo

    Returns:
        Dict con risk_score, sentiment, y keywords detectadas
    """

    text_lower = text.lower()
    risk_score = 0
    detected_issues = []
    sentiment = 'neutral'

    # Análisis de keywords negativas
    for keyword, score in RISK_KEYWORDS.items():
        if keyword in text_lower:
            risk_score = max(risk_score, score)
            detected_issues.append(keyword)

    # Análisis de keywords positivas
    for pos_keyword in POSITIVE_KEYWORDS:
        if pos_keyword in text_lower:
            risk_score = max(0, risk_score - 30)
            sentiment = 'positive'
            break

    # Clasificación final
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
    """
    Mapea código presupuestario y descripción a componente DOTMLPF.

    Args:
        codigo: Código presupuestario
        descripcion: Descripción de la partida

    Returns:
        Letra DOTMLPF
    """

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
# MÓDULO 6: CÁLCULO DE MÉTRICAS Y CALIDAD DEL GASTO
# ============================================================================

def calculate_quality_metrics(df_budget: pd.DataFrame, df_reports: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula KPIs de eficiencia presupuestaria y alistamiento operativo.

    Args:
        df_budget: DataFrame de presupuesto
        df_reports: DataFrame de reportes con análisis NLP

    Returns:
        DataFrame con métricas agregadas por unidad
    """

    # KPI 1: Ejecución Presupuestaria
    budget_metrics = df_budget.groupby('Unidad_Beneficiaria').agg({
        'Monto_Asignado': 'sum',
        'Monto_Ejecutado': 'sum'
    }).reset_index()

    budget_metrics['Ejecucion_Pct'] = (
        budget_metrics['Monto_Ejecutado'] / budget_metrics['Monto_Asignado'] * 100
    ).round(2)

    # KPI 2: Alistamiento Operativo
    readiness_metrics = df_reports.groupby('Unidad').agg({
        'readiness_index': 'mean',
        'risk_score': 'mean'
    }).reset_index()

    readiness_metrics.rename(columns={'Unidad': 'Unidad_Beneficiaria'}, inplace=True)
    readiness_metrics['Alistamiento_Pct'] = readiness_metrics['readiness_index'].round(2)

    # Merge
    metrics = budget_metrics.merge(
        readiness_metrics[['Unidad_Beneficiaria', 'Alistamiento_Pct', 'risk_score']],
        on='Unidad_Beneficiaria',
        how='left'
    )

    # Rellenar NaN
    metrics['Alistamiento_Pct'] = metrics['Alistamiento_Pct'].fillna(metrics['Alistamiento_Pct'].mean())
    metrics['risk_score'] = metrics['risk_score'].fillna(metrics['risk_score'].mean())

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


def create_dotmlpf_matrix(df_budget: pd.DataFrame) -> pd.DataFrame:
    """
    Crea matriz cruzada Nivel Operacional x DOTMLPF.

    Args:
        df_budget: DataFrame de presupuesto con clasificaciones

    Returns:
        DataFrame pivote para heatmap
    """

    matrix = df_budget.pivot_table(
        index='Operational_Level',
        columns='DOTMLPF_Tag',
        values='Monto_Ejecutado',
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
# MÓDULO 7: PROCESAMIENTO PRINCIPAL (ETL + ENRIQUECIMIENTO)
# ============================================================================

@st.cache_data
def load_and_process_data(capability: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Pipeline principal: Genera, procesa y enriquece datos por capacidad.

    Args:
        capability: Capacidad estratégica a procesar

    Returns:
        Tupla (df_budget_enriched, df_reports_analyzed, df_metrics)
    """

    # STAGE 1: Generación
    df_budget = generate_structured_data(capability)
    df_reports = generate_unstructured_data(capability)

    # STAGE 2: Clasificación
    df_budget['Operational_Level'] = df_budget.apply(
        lambda row: classify_operational_level(row['Descripcion'], row['Capacidad']),
        axis=1
    )

    # STAGE 3: Análisis NLP
    nlp_results = df_reports['Texto_Reporte'].apply(analyze_sentiment_readiness)
    df_reports['risk_score'] = nlp_results.apply(lambda x: x['risk_score'])
    df_reports['sentiment'] = nlp_results.apply(lambda x: x['sentiment'])
    df_reports['issues_detected'] = nlp_results.apply(lambda x: x['issues_detected'])
    df_reports['readiness_index'] = nlp_results.apply(lambda x: x['readiness_index'])

    # STAGE 4: Métricas
    df_metrics = calculate_quality_metrics(df_budget, df_reports)

    return df_budget, df_reports, df_metrics


# ============================================================================
# MÓDULO 8: VISUALIZACIONES
# ============================================================================

def render_dotmlpf_heatmap(df_budget: pd.DataFrame):
    """Matriz de Calor DOTMLPF."""

    matrix = create_dotmlpf_matrix(df_budget)

    fig = go.Figure(data=go.Heatmap(
        z=matrix.values,
        x=[f"{k} - {v}" for k, v in DOTMLPF_TAXONOMY.items()],
        y=matrix.index,
        colorscale='Viridis',
        colorbar=dict(title="USD", tickprefix="$", tickformat=",.0f")
    ))

    fig.update_layout(
        title='MATRIZ DOTMLPF x NIVEL OPERACIONAL<br><sub>Inversión Ejecutada (USD)</sub>',
        xaxis_title="Componentes DOTMLPF",
        yaxis_title="Niveles Operacionales",
        template='plotly_dark',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


def render_radar_chart(df_budget: pd.DataFrame):
    """Radar Chart de balance DOTMLPF."""

    dotmlpf_totals = df_budget.groupby('DOTMLPF_Tag')['Monto_Ejecutado'].sum()
    dotmlpf_normalized = (dotmlpf_totals / dotmlpf_totals.max() * 100).round(2)

    categories = [f"{k} - {DOTMLPF_TAXONOMY[k]}" for k in DOTMLPF_TAXONOMY.keys()]
    values = [dotmlpf_normalized.get(k, 0) for k in DOTMLPF_TAXONOMY.keys()]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Inversión Actual',
        line=dict(color='cyan', width=2)
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title='BALANCE DOTMLPF<br><sub>Equilibrio de Capacidades</sub>',
        template='plotly_dark',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


def render_efficiency_matrix(df_metrics: pd.DataFrame):
    """Scatter Plot de Calidad del Gasto."""

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
        color_discrete_map=color_map,
        template='plotly_dark'
    )

    fig.add_hline(y=80, line_dash="dash", line_color="yellow", opacity=0.5)
    fig.add_hline(y=50, line_dash="dash", line_color="orange", opacity=0.5)
    fig.add_vline(x=80, line_dash="dash", line_color="yellow", opacity=0.5)
    fig.add_vline(x=50, line_dash="dash", line_color="orange", opacity=0.5)

    fig.update_layout(
        title='MATRIZ DE CALIDAD DEL GASTO',
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# MÓDULO 9: LANDING PAGE (SELECTOR DE CAPACIDADES)
# ============================================================================

def render_landing_page():
    """
    Pantalla inicial de selección de capacidad estratégica.
    """

    st.markdown("""
        <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #000428 0%, #004e92 100%); border-radius: 15px; margin-bottom: 40px;'>
            <h1 style='margin: 0; font-size: 56px; color: #00D9FF;'>⚔️ SIEC v3.0</h1>
            <p style='color: #FFD700; font-size: 24px; margin: 15px 0;'>
                Sistema Integrado de Evaluación de Capacidades
            </p>
            <p style='color: #AAAAAA; font-size: 14px; margin: 5px 0;'>
                Arquitectura Modular Multicapacidad | Defense Analytics Engine
            </p>
            <p style='color: #00D9FF; font-size: 12px; margin: 10px 0;'>
                NATO DOTMLPF Framework | Lakehouse Hybrid Architecture | NLP Intelligence
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #FFD700;'>📊 SELECCIONE CAPACIDAD ESTRATÉGICA</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Grid de capacidades
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

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 11px; padding: 20px; border-top: 1px solid #333;'>
            <b>SIEC Defense Analytics Platform v3.0</b> | Multi-Capability Architecture<br>
            Powered by Streamlit + Pandas + Plotly | NATO UNCLASSIFIED<br>
            <i>Sistema de Evaluación Estratégica de Capacidades Militares</i>
        </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MÓDULO 10: DASHBOARD PRINCIPAL (POR CAPACIDAD)
# ============================================================================

def render_dashboard(capability: str):
    """
    Dashboard analítico específico por capacidad.

    Args:
        capability: Capacidad estratégica seleccionada
    """

    cap_info = STRATEGIC_CAPABILITIES[capability]

    # Configuración de página
    st.set_page_config(
        page_title=f"SIEC | {cap_info['name']}",
        page_icon=cap_info['icon'],
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS Custom
    st.markdown("""
        <style>
        .main {background-color: #0E1117;}
        h1 {color: #00D9FF; font-family: 'Arial Black', sans-serif;}
        h2 {color: #FFD700; border-bottom: 2px solid #FFD700; padding-bottom: 10px;}
        h3 {color: #00FF00;}
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #000428 0%, #004e92 100%); border-radius: 10px;'>
            <h1 style='margin: 0; font-size: 42px;'>{cap_info['icon']} {cap_info['name']}</h1>
            <p style='color: #00D9FF; font-size: 16px; margin: 10px 0;'>
                {cap_info['description']}
            </p>
            <p style='color: #FFD700; font-size: 11px; margin: 5px 0;'>
                SIEC v3.0 | NATO DOTMLPF Analysis Framework
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Cargar datos
    with st.spinner(f'🔄 Procesando datos de {cap_info["name"]}...'):
        df_budget, df_reports, df_metrics = load_and_process_data(capability)

    # Sidebar
    with st.sidebar:
        st.markdown(f"## {cap_info['icon']} {cap_info['name']}")
        st.markdown("---")

        # Botón volver
        if st.button("⬅️ VOLVER AL INICIO", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.selected_capability = None
            st.rerun()

        st.markdown("---")
        st.markdown("### 📊 MÉTRICAS EJECUTIVAS")

        total_asignado = df_budget['Monto_Asignado'].sum()
        total_ejecutado = df_budget['Monto_Ejecutado'].sum()
        ejecucion_global = (total_ejecutado / total_asignado * 100)
        alistamiento_promedio = df_metrics['Alistamiento_Pct'].mean()

        st.metric("Presupuesto Asignado", f"${total_asignado:,.0f}")
        st.metric("Presupuesto Ejecutado", f"${total_ejecutado:,.0f}", delta=f"{ejecucion_global:.1f}%")
        st.metric("Alistamiento Promedio", f"{alistamiento_promedio:.1f}%")

        st.markdown("---")
        st.markdown("### 🔍 FILTROS")

        selected_units = st.multiselect(
            "Unidades",
            options=df_budget['Unidad_Beneficiaria'].unique(),
            default=df_budget['Unidad_Beneficiaria'].unique()
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
        st.markdown("## 🎯 ANÁLISIS DOTMLPF")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Partidas Analizadas", len(df_budget_filtered))
        with col2:
            st.metric("Inversión Total", f"${df_budget_filtered['Monto_Ejecutado'].sum():,.0f}")
        with col3:
            gaps = (create_dotmlpf_matrix(df_budget_filtered) == 0).sum().sum()
            st.metric("Gaps Detectados", gaps, delta="Requieren atención", delta_color="inverse")

        st.markdown("---")

        render_dotmlpf_heatmap(df_budget_filtered)

        st.markdown("---")

        col_radar, col_table = st.columns(2)

        with col_radar:
            render_radar_chart(df_budget_filtered)

        with col_table:
            st.markdown("### 📋 TOP 10 PARTIDAS")
            top_partidas = df_budget_filtered.nlargest(10, 'Monto_Ejecutado')[
                ['Descripcion', 'Monto_Ejecutado', 'DOTMLPF_Tag']
            ]
            st.dataframe(
                top_partidas.style.format({'Monto_Ejecutado': '${:,.0f}'}),
                use_container_width=True,
                height=400
            )

    # TAB 2
    with tab2:
        st.markdown("## 💰 GOBERNANZA FINANCIERA")

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
    """
    Orquestador principal con navegación por session_state.
    """

    # Inicializar session state
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    if 'selected_capability' not in st.session_state:
        st.session_state.selected_capability = None

    # Routing
    if st.session_state.page == 'landing':
        render_landing_page()
    elif st.session_state.page == 'dashboard' and st.session_state.selected_capability:
        render_dashboard(st.session_state.selected_capability)
    else:
        # Fallback
        st.session_state.page = 'landing'
        st.rerun()


if __name__ == "__main__":
    main()
