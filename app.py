"""
SIEC-C2: Sistema Integrado de Evaluación de Capacidades de Mando y Control
============================================================================
POC Funcional End-to-End para Análisis Estratégico de Defensa

Autor: Lead Data Scientist - OTAN Defense Analytics
Arquitectura: Lakehouse Híbrido (Datos Estructurados + NLP No Estructurado)
Framework: Streamlit + Pandas + Plotly
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

# Niveles de Comando y Control (Joint Publication 3-0)
C2_LEVELS = ['C2 Estratégico', 'C2 Operacional', 'C2 Táctico', 'Guerra Electrónica']

# Keywords para clasificación automática
C2_KEYWORDS = {
    'C2 Estratégico': ['bunker', 'comando', 'estratégico', 'integrado', 'nacional'],
    'C2 Operacional': ['operacional', 'teatro', 'coordinación', 'enlace', 'interoperabilidad'],
    'C2 Táctico': ['táctico', 'radio', 'comunicaciones', 'móvil', 'campo'],
    'Guerra Electrónica': ['radar', 'guerra electrónica', 'jamming', 'frecuencia', 'espectro']
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
    'sin personal': 85
}

POSITIVE_KEYWORDS = ['operando al 100%', 'excelente', 'óptimo', 'actualizado', 'disponible']

# Unidades Militares Ficticias
MILITARY_UNITS = [
    'Ala de Combate 21 (Taura)',
    'Ala de Combate 22 (Guayaquil)',
    'Ala de Combate 23 (Manta)',
    'Comando Aéreo de Combate',
    'Grupo de Guerra Electrónica',
    'Escuadrón de Defensa Aérea',
    'Centro de Operaciones Conjuntas',
    'Comando de Ciberdefensa'
]

# ============================================================================
# MÓDULO 1: GENERACIÓN DE DATOS ESTRUCTURADOS (SQL SIMULADO)
# ============================================================================

def generate_structured_data() -> pd.DataFrame:
    """
    Simula la ingesta desde eSIGEF (Sistema Financiero Gubernamental).
    Genera 150 registros de partidas presupuestarias con enfoque en C2.

    Returns:
        DataFrame con estructura de presupuesto militar
    """

    np.random.seed(42)
    random.seed(42)

    # Partidas Presupuestarias Específicas para C2
    c2_items = [
        ('Licencias Software C2', '530801', 'T'),
        ('Radios HF Tácticas', '840101', 'M'),
        ('Construcción Bunker Datos', '750101', 'F'),
        ('Curso Ciberdefensa', '530501', 'T'),
        ('Servidor Principal C2', '710101', 'M'),
        ('Mantenimiento Radar', '530201', 'M'),
        ('Antenas Satelitales', '840102', 'M'),
        ('Capacitación Operadores', '530502', 'T'),
        ('Estudio Doctrina Conjunta', '580101', 'D'),
        ('Consultoría Interoperabilidad', '570101', 'O'),
        ('Simulador Guerra Electrónica', '710201', 'M'),
        ('Renovación Centro Comando', '750102', 'F'),
        ('Equipos Criptográficos', '840103', 'M'),
        ('Personal Especializado C2', '510101', 'P'),
        ('Generadores de Emergencia', '710301', 'F'),
        ('Software Inteligencia Artificial', '530802', 'T'),
        ('Fibra Óptica Redundante', '750103', 'F'),
        ('Curso Liderazgo Táctico', '530503', 'L'),
        ('Repuestos Sistema Radar', '530202', 'M'),
        ('Análisis Vulnerabilidades', '580102', 'D')
    ]

    # Partidas genéricas (completar hasta 150)
    generic_items = [
        ('Combustible Aeronáutico', '530301'),
        ('Munición de Entrenamiento', '530302'),
        ('Vehículos Administrativos', '710401'),
        ('Uniformes Personal', '530601'),
        ('Viáticos Misiones', '530701'),
        ('Servicios Básicos', '530101'),
        ('Alimentación Tropa', '530602'),
        ('Material Oficina', '530102'),
        ('Seguros Aeronaves', '530901'),
        ('Mantenimiento Infraestructura', '750201')
    ]

    records = []
    start_date = datetime(2024, 1, 1)

    # Generar registros C2 (70 registros)
    for i in range(70):
        item = random.choice(c2_items)
        unit = random.choice(MILITARY_UNITS)

        monto_asignado = np.random.randint(50000, 500000)
        # Variabilidad realista en ejecución
        ejecucion_pct = np.random.beta(7, 3)  # Distribución sesgada hacia alta ejecución
        monto_ejecutado = int(monto_asignado * ejecucion_pct)

        fecha = start_date + timedelta(days=random.randint(0, 330))

        records.append({
            'ID_Partida': f'C2-{i+1:04d}',
            'Codigo_Presupuestario': item[1],
            'Descripcion': item[0],
            'Monto_Asignado': monto_asignado,
            'Monto_Ejecutado': monto_ejecutado,
            'Fecha': fecha,
            'Unidad_Beneficiaria': unit,
            'Tipo_Recurso': 'Inversión' if item[1].startswith(('71', '84', '75')) else 'Gasto',
            'DOTMLPF_Tag': item[2] if len(item) > 2 else None
        })

    # Generar registros genéricos (80 registros)
    for i in range(80):
        item = random.choice(generic_items)
        unit = random.choice(MILITARY_UNITS)

        monto_asignado = np.random.randint(10000, 200000)
        ejecucion_pct = np.random.beta(5, 3)
        monto_ejecutado = int(monto_asignado * ejecucion_pct)

        fecha = start_date + timedelta(days=random.randint(0, 330))

        # Mapear código a DOTMLPF
        codigo_base = item[1][:2]
        dotmlpf = BUDGET_CODE_MAPPING.get(codigo_base, 'O')

        records.append({
            'ID_Partida': f'GEN-{i+1:04d}',
            'Codigo_Presupuestario': item[1],
            'Descripcion': item[0],
            'Monto_Asignado': monto_asignado,
            'Monto_Ejecutado': monto_ejecutado,
            'Fecha': fecha,
            'Unidad_Beneficiaria': unit,
            'Tipo_Recurso': 'Inversión' if item[1].startswith(('71', '84', '75')) else 'Gasto',
            'DOTMLPF_Tag': dotmlpf
        })

    df = pd.DataFrame(records)
    return df


# ============================================================================
# MÓDULO 2: GENERACIÓN DE DATOS NO ESTRUCTURADOS (NLP SIMULADO)
# ============================================================================

def generate_unstructured_data() -> pd.DataFrame:
    """
    Simula reportes operativos de texto libre extraídos de PDFs.
    Representa el componente no estructurado del Lakehouse.

    Returns:
        DataFrame con reportes de novedades operativas
    """

    random.seed(42)

    # Templates realistas de reportes militares
    report_templates = [
        # Reportes negativos (indicadores de riesgo)
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
        "Falta de repuestos críticos para sistema integrado de defensa aérea.",

        # Reportes neutros/informativos
        "Mantenimiento preventivo programado para próxima semana en radar secundario.",
        "Rotación de personal completada según cronograma establecido.",
        "Auditoría de seguridad informática en proceso, resultados pendientes.",
        "Nuevo personal incorporado requiere certificación en sistemas C2.",
        "Inventario de equipos realizado, discrepancias menores detectadas.",
        "Pruebas de interoperabilidad con unidades navales programadas para Q2.",
        "Migración de sistemas legacy en fase de planificación.",
        "Consumo energético dentro de parámetros normales este trimestre.",

        # Reportes positivos
        "Enlaces satelitales operando al 100% de capacidad nominal.",
        "Personal completó certificación internacional en guerra electrónica.",
        "Sistema de respaldo activado exitosamente durante simulacro.",
        "Nuevo bunker de datos inaugurado con tecnología de última generación.",
        "Software de inteligencia artificial integrado exitosamente al sistema C2.",
        "Capacitación de operadores completada con calificación excelente.",
        "Sistema de detección temprana funcionando óptimamente según pruebas.",
        "Redundancia de comunicaciones verificada en ejercicio conjunto.",
        "Equipos criptográficos actualizados a estándares NATO vigentes.",
        "Centro de operaciones conjuntas certificado para operaciones 24/7."
    ]

    # Ampliar templates para llegar a 50 reportes únicos
    extended_templates = [
        "Radar de vigilancia aérea presentando ecos fantasma en sector norte.",
        "Sistema de mando táctico requiere actualización de bases de datos geográficas.",
        "Disponibilidad de ancho de banda satelital reducida al 60% por condiciones meteorológicas.",
        "Protocolo de encriptación implementado exitosamente en todas las estaciones.",
        "Personal técnico requiere entrenamiento en nuevos sistemas de guerra electrónica.",
        "Centro de análisis de inteligencia reporta procesamiento óptimo de datos.",
        "Sistema de alarma temprana con falsos positivos recurrentes.",
        "Coordinación con fuerzas terrestres mejorada tras ejercicio UNITAS.",
        "Plataforma de comando móvil completamente operativa tras mantenimiento.",
        "Vulnerabilidad detectada en firewall perimetral, mitigación en curso.",
        "Sistema de posicionamiento GPS con deriva detectada en calibración.",
        "Nueva doctrina de operaciones conjuntas en proceso de implementación.",
        "Equipos de comunicación táctica terrestre operando sin novedades.",
        "Análisis de espectro radioeléctrico revela interferencias no identificadas.",
        "Personal de liderazgo táctico completó curso avanzado en EE.UU.",
        "Sistema de gestión de crisis activado durante emergencia simulada.",
        "Infraestructura de red reforzada con fibra óptica redundante.",
        "Estudio de amenazas cibernéticas completado, recomendaciones en revisión.",
        "Simulador de combate aéreo integrado al sistema de entrenamiento.",
        "Generadores diésel operando dentro de parámetros de mantenimiento preventivo."
    ]

    all_templates = report_templates + extended_templates

    records = []
    for i in range(50):
        report_text = all_templates[i] if i < len(all_templates) else random.choice(all_templates)
        unit = random.choice(MILITARY_UNITS)
        fecha = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 330))

        records.append({
            'Report_ID': f'RPT-{i+1:04d}',
            'Fecha': fecha,
            'Unidad': unit,
            'Texto_Reporte': report_text,
            'Categoria': 'Operacional'  # Placeholder para clasificación posterior
        })

    return pd.DataFrame(records)


# ============================================================================
# MÓDULO 3: MOTOR NLP - ANÁLISIS DE SENTIMIENTO Y RIESGO
# ============================================================================

def analyze_sentiment_readiness(text: str) -> Dict[str, any]:
    """
    Motor NLP simplificado para analizar riesgo operacional.
    En producción: BERT multilingual + clasificador fine-tuned.

    Args:
        text: Texto del reporte operativo

    Returns:
        Dict con risk_score, sentiment, y keywords detectadas
    """

    text_lower = text.lower()
    risk_score = 0
    detected_issues = []
    sentiment = 'neutral'

    # Análisis de keywords negativas (indicadores de riesgo)
    for keyword, score in RISK_KEYWORDS.items():
        if keyword in text_lower:
            risk_score = max(risk_score, score)
            detected_issues.append(keyword)

    # Análisis de keywords positivas (reducen riesgo)
    for pos_keyword in POSITIVE_KEYWORDS:
        if pos_keyword in text_lower:
            risk_score = max(0, risk_score - 30)
            sentiment = 'positive'
            break

    # Clasificación de sentimiento final
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
        'readiness_index': 100 - risk_score  # Alistamiento inverso al riesgo
    }


# ============================================================================
# MÓDULO 4: CLASIFICADOR MULTIDIMENSIONAL DOTMLPF x C2
# ============================================================================

def classify_c2_level(description: str) -> str:
    """
    Clasifica una partida o reporte en nivel C2 usando keywords.

    Args:
        description: Texto a clasificar

    Returns:
        Nivel C2 ('C2 Estratégico', 'C2 Operacional', etc.)
    """

    desc_lower = description.lower()

    for level, keywords in C2_KEYWORDS.items():
        if any(keyword in desc_lower for keyword in keywords):
            return level

    return 'C2 Operacional'  # Default


def map_dotmlpf(codigo: str, descripcion: str) -> str:
    """
    Mapea código presupuestario y descripción a componente DOTMLPF.

    Args:
        codigo: Código presupuestario (ej. '710101')
        descripcion: Descripción de la partida

    Returns:
        Letra DOTMLPF ('D', 'O', 'T', 'M', 'L', 'P', 'F')
    """

    # Primero intentar mapeo por código
    codigo_base = codigo[:2]
    if codigo_base in BUDGET_CODE_MAPPING:
        return BUDGET_CODE_MAPPING[codigo_base]

    # Si no, usar análisis de texto
    desc_lower = descripcion.lower()
    if 'doctrina' in desc_lower or 'estudio' in desc_lower:
        return 'D'
    elif 'organización' in desc_lower or 'asesoría' in desc_lower:
        return 'O'
    elif 'curso' in desc_lower or 'capacitación' in desc_lower or 'entrenamiento' in desc_lower:
        return 'T'
    elif 'equipo' in desc_lower or 'material' in desc_lower or 'hardware' in desc_lower:
        return 'M'
    elif 'liderazgo' in desc_lower or 'comando' in desc_lower:
        return 'L'
    elif 'personal' in desc_lower or 'salario' in desc_lower:
        return 'P'
    elif 'infraestructura' in desc_lower or 'construcción' in desc_lower or 'instalación' in desc_lower:
        return 'F'
    else:
        return 'O'  # Default


# ============================================================================
# MÓDULO 5: ALGORITMO DE CALIDAD DEL GASTO Y MÉTRICAS
# ============================================================================

def calculate_quality_metrics(df_budget: pd.DataFrame, df_reports: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula KPIs de eficiencia presupuestaria y alistamiento operativo.
    Implementa la Matriz de Salud del Sistema C2.

    Args:
        df_budget: DataFrame de presupuesto
        df_reports: DataFrame de reportes con análisis NLP

    Returns:
        DataFrame con métricas agregadas por unidad
    """

    # KPI 1: Ejecución Presupuestaria por Unidad
    budget_metrics = df_budget.groupby('Unidad_Beneficiaria').agg({
        'Monto_Asignado': 'sum',
        'Monto_Ejecutado': 'sum'
    }).reset_index()

    budget_metrics['Ejecucion_Pct'] = (
        budget_metrics['Monto_Ejecutado'] / budget_metrics['Monto_Asignado'] * 100
    ).round(2)

    # KPI 2: Índice de Alistamiento Operativo (derivado de reportes NLP)
    readiness_metrics = df_reports.groupby('Unidad').agg({
        'readiness_index': 'mean',
        'risk_score': 'mean'
    }).reset_index()

    readiness_metrics.rename(columns={'Unidad': 'Unidad_Beneficiaria'}, inplace=True)
    readiness_metrics['Alistamiento_Pct'] = readiness_metrics['readiness_index'].round(2)

    # Merge de ambos KPIs
    metrics = budget_metrics.merge(
        readiness_metrics[['Unidad_Beneficiaria', 'Alistamiento_Pct', 'risk_score']],
        on='Unidad_Beneficiaria',
        how='left'
    )

    # Rellenar unidades sin reportes con alistamiento promedio
    metrics['Alistamiento_Pct'] = metrics['Alistamiento_Pct'].fillna(metrics['Alistamiento_Pct'].mean())
    metrics['risk_score'] = metrics['risk_score'].fillna(metrics['risk_score'].mean())

    # Clasificación en Cuadrantes (Matriz de Eficiencia)
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
    Crea matriz cruzada C2 Level x DOTMLPF con montos invertidos.

    Args:
        df_budget: DataFrame de presupuesto con clasificaciones

    Returns:
        DataFrame pivote para heatmap
    """

    matrix = df_budget.pivot_table(
        index='C2_Level',
        columns='DOTMLPF_Tag',
        values='Monto_Ejecutado',
        aggfunc='sum',
        fill_value=0
    )

    # Asegurar que todas las columnas DOTMLPF existan
    for letter in DOTMLPF_TAXONOMY.keys():
        if letter not in matrix.columns:
            matrix[letter] = 0

    # Ordenar columnas según DOTMLPF
    matrix = matrix[list(DOTMLPF_TAXONOMY.keys())]

    return matrix


# ============================================================================
# MÓDULO 6: PROCESAMIENTO PRINCIPAL (ETL + ENRIQUECIMIENTO)
# ============================================================================

@st.cache_data
def load_and_process_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Pipeline principal: Genera, procesa y enriquece todos los datos.
    Cachea resultados para performance óptimo en Streamlit.

    Returns:
        Tupla (df_budget_enriched, df_reports_analyzed, df_metrics)
    """

    # STAGE 1: Generación de Datos Raw
    df_budget = generate_structured_data()
    df_reports = generate_unstructured_data()

    # STAGE 2: Enriquecimiento de Datos Estructurados
    df_budget['C2_Level'] = df_budget['Descripcion'].apply(classify_c2_level)

    # Asegurar que DOTMLPF_Tag esté presente
    if 'DOTMLPF_Tag' not in df_budget.columns or df_budget['DOTMLPF_Tag'].isna().any():
        df_budget['DOTMLPF_Tag'] = df_budget.apply(
            lambda row: map_dotmlpf(row['Codigo_Presupuestario'], row['Descripcion']),
            axis=1
        )

    # STAGE 3: Análisis NLP de Reportes No Estructurados
    nlp_results = df_reports['Texto_Reporte'].apply(analyze_sentiment_readiness)
    df_reports['risk_score'] = nlp_results.apply(lambda x: x['risk_score'])
    df_reports['sentiment'] = nlp_results.apply(lambda x: x['sentiment'])
    df_reports['issues_detected'] = nlp_results.apply(lambda x: x['issues_detected'])
    df_reports['readiness_index'] = nlp_results.apply(lambda x: x['readiness_index'])

    # STAGE 4: Cálculo de Métricas Agregadas
    df_metrics = calculate_quality_metrics(df_budget, df_reports)

    return df_budget, df_reports, df_metrics


# ============================================================================
# MÓDULO 7: VISUALIZACIONES TÁCTICAS (PLOTLY)
# ============================================================================

def render_dotmlpf_heatmap(df_budget: pd.DataFrame):
    """
    Matriz de Calor: Inversión por Nivel C2 x Componente DOTMLPF.
    Resalta gaps de capacidad en ROJO.
    """

    matrix = create_dotmlpf_matrix(df_budget)

    # Crear anotaciones de texto para cada celda
    annotations = []
    for i, row_label in enumerate(matrix.index):
        for j, col_label in enumerate(matrix.columns):
            value = matrix.iloc[i, j]
            text = f'${value/1000:.0f}K' if value > 0 else 'GAP'
            color = 'white' if value > 0 else 'red'
            annotations.append(
                dict(
                    x=col_label,
                    y=row_label,
                    text=text,
                    showarrow=False,
                    font=dict(color=color, size=11, family='Courier New, monospace')
                )
            )

    fig = go.Figure(data=go.Heatmap(
        z=matrix.values,
        x=[f"{k} - {v}" for k, v in DOTMLPF_TAXONOMY.items()],
        y=matrix.index,
        colorscale='Viridis',
        text=matrix.values,
        texttemplate='%{text:.0f}',
        textfont={"size": 10},
        colorbar=dict(title="USD Ejecutado", tickprefix="$", tickformat=",.0f")
    ))

    fig.update_layout(
        title=dict(
            text='MATRIZ DOTMLPF x NIVEL C2<br><sub>Inversión Ejecutada (USD) - Gaps en ROJO</sub>',
            font=dict(size=18, family='Arial Black')
        ),
        xaxis_title="Componentes DOTMLPF (NATO Taxonomy)",
        yaxis_title="Niveles de Comando y Control",
        template='plotly_dark',
        height=500,
        annotations=annotations
    )

    st.plotly_chart(fig, use_container_width=True)


def render_radar_chart(df_budget: pd.DataFrame):
    """
    Radar Chart: Balance de inversión entre componentes DOTMLPF.
    Detecta desequilibrios (mucho M, poco T).
    """

    dotmlpf_totals = df_budget.groupby('DOTMLPF_Tag')['Monto_Ejecutado'].sum()

    # Normalizar a escala 0-100 para visualización
    dotmlpf_normalized = (dotmlpf_totals / dotmlpf_totals.max() * 100).round(2)

    categories = [f"{k} - {DOTMLPF_TAXONOMY[k]}" for k in DOTMLPF_TAXONOMY.keys()]
    values = [dotmlpf_normalized.get(k, 0) for k in DOTMLPF_TAXONOMY.keys()]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Inversión Actual',
        line=dict(color='cyan', width=2),
        fillcolor='rgba(0,255,255,0.3)'
    ))

    # Línea de referencia (equilibrio ideal)
    ideal_balance = [70] * len(categories)  # 70% como target balanced
    fig.add_trace(go.Scatterpolar(
        r=ideal_balance,
        theta=categories,
        fill='toself',
        name='Target Equilibrado',
        line=dict(color='yellow', width=1, dash='dash'),
        fillcolor='rgba(255,255,0,0.1)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], ticksuffix='%'),
            bgcolor='rgba(20,20,20,0.5)'
        ),
        title=dict(
            text='BALANCE DOTMLPF<br><sub>Equilibrio de Capacidades (Normalizado)</sub>',
            font=dict(size=18, family='Arial Black')
        ),
        template='plotly_dark',
        height=500,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)


def render_efficiency_matrix(df_metrics: pd.DataFrame):
    """
    Scatter Plot: Matriz de Salud (Ejecución vs Alistamiento).
    Clasificación en cuadrantes con tooltips informativos.
    """

    # Configuración de colores por cuadrante
    color_map = {
        'Eficiente': 'green',
        'Ineficiente (Auditar)': 'red',
        'Sub-Ejecución': 'gray',
        'Crítico': 'darkred'
    }

    df_metrics['Color'] = df_metrics['Cuadrante'].map(color_map)

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
            'Alistamiento_Pct': ':.1f%',
            'risk_score': ':.0f',
            'Color': False
        },
        color_discrete_map=color_map,
        template='plotly_dark',
        labels={
            'Ejecucion_Pct': 'Ejecución Presupuestaria (%)',
            'Alistamiento_Pct': 'Índice de Alistamiento Operativo (%)'
        }
    )

    # Añadir líneas de referencia para cuadrantes
    fig.add_hline(y=80, line_dash="dash", line_color="yellow", opacity=0.5)
    fig.add_hline(y=50, line_dash="dash", line_color="orange", opacity=0.5)
    fig.add_vline(x=80, line_dash="dash", line_color="yellow", opacity=0.5)
    fig.add_vline(x=50, line_dash="dash", line_color="orange", opacity=0.5)

    # Anotaciones de cuadrantes
    annotations = [
        dict(x=90, y=90, text="EFICIENTE", showarrow=False, font=dict(size=14, color='lime')),
        dict(x=90, y=30, text="AUDITAR", showarrow=False, font=dict(size=14, color='red')),
        dict(x=30, y=90, text="SUB-EJECUCIÓN", showarrow=False, font=dict(size=14, color='gray')),
        dict(x=30, y=30, text="CRÍTICO", showarrow=False, font=dict(size=14, color='darkred'))
    ]

    fig.update_layout(
        title=dict(
            text='MATRIZ DE CALIDAD DEL GASTO<br><sub>Ejecución Presupuestaria vs Alistamiento Operativo</sub>',
            font=dict(size=18, family='Arial Black')
        ),
        annotations=annotations,
        height=600,
        xaxis=dict(range=[0, 105]),
        yaxis=dict(range=[0, 105])
    )

    st.plotly_chart(fig, use_container_width=True)


def render_timeline_execution(df_budget: pd.DataFrame):
    """
    Gráfico de línea temporal de ejecución presupuestaria acumulada.
    """

    df_timeline = df_budget.copy()
    df_timeline = df_timeline.sort_values('Fecha')
    df_timeline['Ejecutado_Acumulado'] = df_timeline['Monto_Ejecutado'].cumsum()
    df_timeline['Asignado_Acumulado'] = df_timeline['Monto_Asignado'].cumsum()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_timeline['Fecha'],
        y=df_timeline['Asignado_Acumulado'],
        mode='lines',
        name='Presupuesto Asignado',
        line=dict(color='yellow', width=3, dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=df_timeline['Fecha'],
        y=df_timeline['Ejecutado_Acumulado'],
        mode='lines',
        name='Presupuesto Ejecutado',
        line=dict(color='cyan', width=3),
        fill='tonexty',
        fillcolor='rgba(0,255,255,0.2)'
    ))

    fig.update_layout(
        title='EJECUCIÓN PRESUPUESTARIA ACUMULADA 2024',
        xaxis_title='Fecha',
        yaxis_title='Monto USD',
        template='plotly_dark',
        height=400,
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# MÓDULO 8: DASHBOARD PRINCIPAL (STREAMLIT UI)
# ============================================================================

def render_dashboard():
    """
    Orquestador principal del dashboard interactivo.
    """

    # Configuración de página
    st.set_page_config(
        page_title="SIEC-C2 | Defense Analytics",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS Custom para Dark Mode Profesional
    st.markdown("""
        <style>
        .main {background-color: #0E1117;}
        .stTabs [data-baseweb="tab-list"] {gap: 8px;}
        .stTabs [data-baseweb="tab"] {
            background-color: #1E1E1E;
            border-radius: 4px;
            padding: 10px 20px;
            color: #FFFFFF;
            font-weight: bold;
        }
        .stTabs [aria-selected="true"] {
            background-color: #00D9FF;
            color: #000000;
        }
        h1 {color: #00D9FF; font-family: 'Arial Black', sans-serif;}
        h2 {color: #FFD700; border-bottom: 2px solid #FFD700; padding-bottom: 10px;}
        h3 {color: #00FF00;}
        .metric-card {
            background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #00D9FF;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #000428 0%, #004e92 100%); border-radius: 10px;'>
            <h1 style='margin: 0; font-size: 48px;'>🎯 SIEC-C2</h1>
            <p style='color: #00D9FF; font-size: 18px; margin: 10px 0 0 0;'>
                Sistema Integrado de Evaluación de Capacidades | Comando y Control
            </p>
            <p style='color: #FFD700; font-size: 12px; margin: 5px 0 0 0;'>
                Defense Analytics Engine v2.5 | NATO DOTMLPF Framework
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Cargar datos
    with st.spinner('🔄 Iniciando arquitectura Lakehouse... Procesando datos estructurados y no estructurados...'):
        df_budget, df_reports, df_metrics = load_and_process_data()

    # Sidebar: Métricas Ejecutivas
    with st.sidebar:
        st.markdown("## 📊 EXECUTIVE DASHBOARD")
        st.markdown("---")

        total_asignado = df_budget['Monto_Asignado'].sum()
        total_ejecutado = df_budget['Monto_Ejecutado'].sum()
        ejecucion_global = (total_ejecutado / total_asignado * 100)
        alistamiento_promedio = df_metrics['Alistamiento_Pct'].mean()

        st.metric(
            "Presupuesto Total Asignado",
            f"${total_asignado:,.0f}",
            delta=None
        )

        st.metric(
            "Presupuesto Ejecutado",
            f"${total_ejecutado:,.0f}",
            delta=f"{ejecucion_global:.1f}% ejecutado"
        )

        st.metric(
            "Índice de Alistamiento",
            f"{alistamiento_promedio:.1f}%",
            delta="Promedio Nacional"
        )

        st.markdown("---")
        st.markdown("### 🔍 FILTROS ANALÍTICOS")

        selected_units = st.multiselect(
            "Unidades Militares",
            options=df_budget['Unidad_Beneficiaria'].unique(),
            default=df_budget['Unidad_Beneficiaria'].unique()
        )

        selected_dotmlpf = st.multiselect(
            "Componentes DOTMLPF",
            options=list(DOTMLPF_TAXONOMY.keys()),
            default=list(DOTMLPF_TAXONOMY.keys()),
            format_func=lambda x: f"{x} - {DOTMLPF_TAXONOMY[x]}"
        )

        st.markdown("---")
        st.markdown("""
            <div style='font-size: 10px; color: #888;'>
            <b>Clasificación de Seguridad:</b><br>
            NATO UNCLASSIFIED<br>
            <b>Última actualización:</b><br>
            2024-12-30 14:35 UTC
            </div>
        """, unsafe_allow_html=True)

    # Aplicar filtros
    df_budget_filtered = df_budget[
        (df_budget['Unidad_Beneficiaria'].isin(selected_units)) &
        (df_budget['DOTMLPF_Tag'].isin(selected_dotmlpf))
    ]

    df_metrics_filtered = df_metrics[df_metrics['Unidad_Beneficiaria'].isin(selected_units)]

    # TABS PRINCIPALES
    tab1, tab2, tab3 = st.tabs([
        "🎯 SITUATIONAL AWARENESS",
        "💰 GOBERNANZA & CALIDAD",
        "🧠 DATA INTELLIGENCE (NLP)"
    ])

    # ========================================================================
    # TAB 1: SITUATIONAL AWARENESS (DOTMLPF)
    # ========================================================================
    with tab1:
        st.markdown("## 🎯 EVALUACIÓN DOTMLPF - CAPACIDADES C2")

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.metric("Total Partidas Analizadas", len(df_budget_filtered))
        with col2:
            partidas_c2 = len(df_budget_filtered[df_budget_filtered['ID_Partida'].str.startswith('C2')])
            st.metric("Partidas C2 Específicas", partidas_c2)
        with col3:
            gaps = (create_dotmlpf_matrix(df_budget_filtered) == 0).sum().sum()
            st.metric("Gaps Detectados", gaps, delta="Requieren atención", delta_color="inverse")

        st.markdown("---")

        # Heatmap DOTMLPF x C2
        st.markdown("### 🔥 Matriz de Inversión Estratégica")
        render_dotmlpf_heatmap(df_budget_filtered)

        st.markdown("---")

        col_radar, col_timeline = st.columns(2)

        with col_radar:
            st.markdown("### 📡 Balance de Capacidades")
            render_radar_chart(df_budget_filtered)

        with col_timeline:
            st.markdown("### 📈 Ejecución Temporal")
            render_timeline_execution(df_budget_filtered)

        # Tabla detallada
        st.markdown("---")
        st.markdown("### 📋 DETALLE DE PARTIDAS PRESUPUESTARIAS")

        df_display = df_budget_filtered[[
            'ID_Partida', 'Descripcion', 'Unidad_Beneficiaria',
            'DOTMLPF_Tag', 'C2_Level', 'Monto_Asignado', 'Monto_Ejecutado'
        ]].copy()

        df_display['Ejecución %'] = (
            df_display['Monto_Ejecutado'] / df_display['Monto_Asignado'] * 100
        ).round(1)

        st.dataframe(
            df_display.style.format({
                'Monto_Asignado': '${:,.0f}',
                'Monto_Ejecutado': '${:,.0f}',
                'Ejecución %': '{:.1f}%'
            }).background_gradient(subset=['Ejecución %'], cmap='RdYlGn'),
            use_container_width=True,
            height=400
        )

    # ========================================================================
    # TAB 2: GOBERNANZA & CALIDAD DEL GASTO
    # ========================================================================
    with tab2:
        st.markdown("## 💰 GOBERNANZA FINANCIERA Y CALIDAD DEL GASTO")

        # Métricas por cuadrante
        col1, col2, col3, col4 = st.columns(4)

        cuadrante_counts = df_metrics_filtered['Cuadrante'].value_counts()

        with col1:
            eficientes = cuadrante_counts.get('Eficiente', 0)
            st.markdown(f"""
                <div class='metric-card' style='border-left-color: green;'>
                    <h3 style='color: #00FF00; margin: 0;'>{eficientes}</h3>
                    <p style='color: #AAA; margin: 5px 0 0 0;'>Unidades Eficientes</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            ineficientes = cuadrante_counts.get('Ineficiente (Auditar)', 0)
            st.markdown(f"""
                <div class='metric-card' style='border-left-color: red;'>
                    <h3 style='color: #FF0000; margin: 0;'>{ineficientes}</h3>
                    <p style='color: #AAA; margin: 5px 0 0 0;'>Requieren Auditoría</p>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            subejecucion = cuadrante_counts.get('Sub-Ejecución', 0)
            st.markdown(f"""
                <div class='metric-card' style='border-left-color: gray;'>
                    <h3 style='color: #AAAAAA; margin: 0;'>{subejecucion}</h3>
                    <p style='color: #AAA; margin: 5px 0 0 0;'>Sub-Ejecución</p>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            criticos = cuadrante_counts.get('Crítico', 0)
            st.markdown(f"""
                <div class='metric-card' style='border-left-color: darkred;'>
                    <h3 style='color: #8B0000; margin: 0;'>{criticos}</h3>
                    <p style='color: #AAA; margin: 5px 0 0 0;'>Estado Crítico</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Matriz de Eficiencia (Scatter Plot)
        st.markdown("### 🎯 MATRIZ DE SALUD DEL SISTEMA C2")
        render_efficiency_matrix(df_metrics_filtered)

        st.markdown("---")

        # Análisis detallado por cuadrante
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("### ⚠️ UNIDADES QUE REQUIEREN ATENCIÓN")
            unidades_atencion = df_metrics_filtered[
                df_metrics_filtered['Cuadrante'].isin(['Ineficiente (Auditar)', 'Crítico'])
            ].sort_values('risk_score', ascending=False)

            if len(unidades_atencion) > 0:
                for _, row in unidades_atencion.iterrows():
                    st.markdown(f"""
                        <div style='background-color: #2D1E1E; padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid red;'>
                            <b style='color: #FF6666;'>{row['Unidad_Beneficiaria']}</b><br>
                            <span style='color: #AAA;'>Ejecución: {row['Ejecucion_Pct']:.1f}% | Alistamiento: {row['Alistamiento_Pct']:.1f}%</span><br>
                            <span style='color: #FF9999; font-size: 12px;'>Risk Score: {row['risk_score']:.0f} | Cuadrante: {row['Cuadrante']}</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No hay unidades en estado crítico.")

        with col_right:
            st.markdown("### ✅ UNIDADES DE EXCELENCIA")
            unidades_excelencia = df_metrics_filtered[
                df_metrics_filtered['Cuadrante'] == 'Eficiente'
            ].sort_values('Alistamiento_Pct', ascending=False)

            if len(unidades_excelencia) > 0:
                for _, row in unidades_excelencia.iterrows():
                    st.markdown(f"""
                        <div style='background-color: #1E2D1E; padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid green;'>
                            <b style='color: #66FF66;'>{row['Unidad_Beneficiaria']}</b><br>
                            <span style='color: #AAA;'>Ejecución: {row['Ejecucion_Pct']:.1f}% | Alistamiento: {row['Alistamiento_Pct']:.1f}%</span><br>
                            <span style='color: #99FF99; font-size: 12px;'>Monto Ejecutado: ${row['Monto_Ejecutado']:,.0f}</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ No hay unidades en cuadrante eficiente actualmente.")

        st.markdown("---")

        # Tabla de métricas completa
        st.markdown("### 📊 TABLA DE MÉTRICAS POR UNIDAD")
        st.dataframe(
            df_metrics_filtered.style.format({
                'Monto_Asignado': '${:,.0f}',
                'Monto_Ejecutado': '${:,.0f}',
                'Ejecucion_Pct': '{:.1f}%',
                'Alistamiento_Pct': '{:.1f}%',
                'risk_score': '{:.0f}'
            }).background_gradient(subset=['Ejecucion_Pct', 'Alistamiento_Pct'], cmap='RdYlGn'),
            use_container_width=True,
            height=400
        )

    # ========================================================================
    # TAB 3: DATA INTELLIGENCE (NLP)
    # ========================================================================
    with tab3:
        st.markdown("## 🧠 INTELIGENCIA DE DATOS - ANÁLISIS NLP")

        # Métricas NLP
        col1, col2, col3, col4 = st.columns(4)

        critical_reports = len(df_reports[df_reports['sentiment'] == 'critical'])
        warning_reports = len(df_reports[df_reports['sentiment'] == 'warning'])
        positive_reports = len(df_reports[df_reports['sentiment'] == 'positive'])
        avg_risk = df_reports['risk_score'].mean()

        with col1:
            st.metric("Reportes Analizados", len(df_reports))
        with col2:
            st.metric("Reportes Críticos", critical_reports, delta="Requieren acción inmediata", delta_color="inverse")
        with col3:
            st.metric("Reportes Positivos", positive_reports, delta="Indicadores saludables")
        with col4:
            st.metric("Risk Score Promedio", f"{avg_risk:.0f}", delta=f"{100-avg_risk:.0f}% alistamiento")

        st.markdown("---")

        # Filtro de búsqueda
        st.markdown("### 🔍 BÚSQUEDA EN REPORTES OPERATIVOS")
        search_term = st.text_input(
            "Filtrar por palabra clave (ej: 'radar', 'falla', 'curso')",
            placeholder="Ingrese término de búsqueda..."
        )

        df_reports_display = df_reports.copy()
        if search_term:
            df_reports_display = df_reports_display[
                df_reports_display['Texto_Reporte'].str.contains(search_term, case=False, na=False)
            ]

        # Distribución de sentimientos
        col_sentiment, col_risk = st.columns(2)

        with col_sentiment:
            st.markdown("### 📊 Distribución de Sentimientos")
            sentiment_counts = df_reports['sentiment'].value_counts()

            sentiment_colors = {
                'critical': '#8B0000',
                'warning': '#FF8C00',
                'caution': '#FFD700',
                'neutral': '#808080',
                'positive': '#00FF00'
            }

            fig_sentiment = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                color=sentiment_counts.index,
                color_discrete_map=sentiment_colors,
                template='plotly_dark'
            )

            fig_sentiment.update_traces(textposition='inside', textinfo='percent+label')
            fig_sentiment.update_layout(height=400)
            st.plotly_chart(fig_sentiment, use_container_width=True)

        with col_risk:
            st.markdown("### 📈 Distribución de Risk Scores")
            fig_risk = px.histogram(
                df_reports,
                x='risk_score',
                nbins=20,
                color_discrete_sequence=['cyan'],
                template='plotly_dark'
            )

            fig_risk.update_layout(
                xaxis_title="Risk Score",
                yaxis_title="Cantidad de Reportes",
                height=400
            )
            st.plotly_chart(fig_risk, use_container_width=True)

        st.markdown("---")

        # Tabla de reportes con clasificación
        st.markdown("### 📋 REPORTES OPERATIVOS PROCESADOS")

        df_reports_table = df_reports_display[[
            'Report_ID', 'Fecha', 'Unidad', 'Texto_Reporte',
            'sentiment', 'risk_score', 'issues_detected'
        ]].copy()

        df_reports_table.columns = [
            'ID', 'Fecha', 'Unidad', 'Reporte',
            'Sentimiento', 'Risk Score', 'Issues Detectados'
        ]

        # Formateo condicional
        def highlight_risk(row):
            if row['Risk Score'] >= 70:
                return ['background-color: #2D1E1E'] * len(row)
            elif row['Risk Score'] >= 50:
                return ['background-color: #2D2A1E'] * len(row)
            elif row['Sentimiento'] == 'positive':
                return ['background-color: #1E2D1E'] * len(row)
            else:
                return [''] * len(row)

        st.dataframe(
            df_reports_table.style.apply(highlight_risk, axis=1).format({
                'Risk Score': '{:.0f}',
                'Fecha': lambda x: x.strftime('%Y-%m-%d')
            }),
            use_container_width=True,
            height=500
        )

        st.markdown("---")

        # Top Issues detectados
        st.markdown("### ⚠️ TOP ISSUES DETECTADOS")

        all_issues = df_reports['issues_detected'].str.split(', ').explode()
        issue_counts = all_issues[all_issues != 'Ninguno'].value_counts().head(10)

        if len(issue_counts) > 0:
            fig_issues = px.bar(
                x=issue_counts.values,
                y=issue_counts.index,
                orientation='h',
                template='plotly_dark',
                color=issue_counts.values,
                color_continuous_scale='Reds'
            )

            fig_issues.update_layout(
                xaxis_title="Frecuencia",
                yaxis_title="Tipo de Issue",
                height=400,
                showlegend=False
            )

            st.plotly_chart(fig_issues, use_container_width=True)
        else:
            st.success("✅ No se detectaron issues críticos en los reportes analizados.")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 12px; padding: 20px;'>
            <b>SIEC-C2 Defense Analytics Platform</b> | Powered by Streamlit + Plotly + Pandas<br>
            Arquitectura Lakehouse | NATO DOTMLPF Framework | NLP Sentiment Analysis<br>
            <i>Sistema de Evaluación de Capacidades Militares - Clasificación: NATO UNCLASSIFIED</i>
        </div>
    """, unsafe_allow_html=True)


# ============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    render_dashboard()
