# SIEC v5.1: Sistema Integrado de Evaluación de Capacidades

## 🎯 Descripción General

POC (Proof of Concept) funcional End-to-End de un sistema de análisis estratégico para evaluación de **múltiples capacidades militares** basado en el framework **DOTmLPF-P de JCIDS** con **ingesta real de datos institucionales** y **referencia doctrinal**.

### **🆕 NUEVA VERSIÓN 5.1 - Referencia Doctrinal JCIDS & Mapeo de Fuentes Reales**

Esta versión implementa:
- ✅ **Taxonomía DOTmLPF-P Completa**: Incluye "Policy" como 8vo componente (D, O, T, M, L, P, F, Pol)
- ✅ **Página de Información Doctrinal**: Nueva sección "📚 Información & Doctrina" con:
  - Definiciones JCIDS oficiales de cada componente
  - Mapeo de fuentes de datos reales institucionales (eSIGEF, PDFs, BD)
  - Explicación del gráfico de Radar (Estado Actual vs Meta Operativa)
  - Flujo completo de procesamiento de datos
- ✅ **Mapeo de Fuentes Reales por Componente**:
  - **D (Doctrine)**: Partida 58, Manuales PDF, Publicaciones JP-3
  - **O (Organization)**: Partida 57, Reportes de reestructuración
  - **T (Training)**: Partida 53, Horas de vuelo, Simuladores
  - **M (Materiel)**: Partida 71/84, Sistema de disponibilidad, KPPs
  - **L (Leadership)**: Educación Militar, Cursos de ascenso
  - **P (Personnel)**: Partida 51, Partes de personal
  - **F (Facilities)**: Partida 75, Planes MILCON
  - **Pol (Policy)**: Partida 59, Convenios, ROE, Restricciones legales
- ✅ **Generación de Datos con Policy**: Items de convenios y acuerdos internacionales
- ✅ **Backward Compatibility**: Mantiene todas las funcionalidades v5.0 y v4.0

### **VERSIÓN 5.0 - Ingesta Real de Datos + Desambiguación Inteligente**

- ✅ **Selector de Modo**: Simulación (Demo) vs Ingesta Real de Datos
- ✅ **File Uploader Excel**: Procesa archivos eSIGEF con normalización automática de columnas
- ✅ **File Uploader PDF**: Extrae texto de reportes operativos con pdfplumber
- ✅ **Desambiguación Inteligente**: Función `clasificar_partida_inteligente()` con reglas de negocio
- ✅ **Clasificación por Keywords + Unidad**: Scoring automático y desempate por unidad beneficiaria
- ✅ **Normalización de Datos**: Mapeo flexible de columnas Excel (Código/Codigo/Partida, etc.)
- ✅ **Placeholder Conector BD**: Preparado para conexión directa a PostgreSQL/Oracle

### **VERSIÓN 4.0 - Scoring Ponderado Estratégico**
- ✅ **Pesos DOTMLPF configurables**: M: 20%, T: 19.4%, P: 16.6%, D: 15.1%, O: 15.1%, F: 13.8%
- ✅ **Orden de Batalla Real FAE**: 15 unidades operativas reales
- ✅ **Algoritmo de scoring ponderado**: Alistamiento = 70% weighted + 30% NLP
- ✅ **Controles en Sidebar**: Ajuste de pesos con validación (suma 100%)

### **VERSIÓN 3.0 - Arquitectura Modular Multicapacidad**
- ✅ **Landing Page** de selección de capacidad estratégica
- ✅ **Navegación dinámica** con st.session_state
- ✅ **Soporte multicapacidad**: Mando y Control, Maniobra Aérea, Ciberdefensa*, Logística*
- ✅ **Filtrado inteligente** de datos por capacidad seleccionada
- ✅ **Clasificadores automáticos** con machine learning (CAPABILITY_KEYWORDS)
- ✅ **Datos específicos** por capacidad (27 ítems Maniobra + 25 reportes)

*Ciberdefensa y Logística: placeholders para desarrollo futuro

### Arquitectura Tecnológica

- **Framework de Datos**: Lakehouse Híbrido (Datos Estructurados + NLP No Estructurado) + **ETL Real**
- **Stack Tecnológico**: Python 3.8+ | Streamlit | Pandas | Plotly | NumPy | **pdfplumber** | **openpyxl**
- **Ingesta de Datos**: Excel (eSIGEF) + PDFs + Placeholder PostgreSQL/Oracle
- **Metodología**: JCIDS DOTmLPF-P Framework | Joint Publication 3-0
- **Versión**: 5.1 (DOTmLPF-P + Doctrinal Reference + Real Data Mapping)
- **Clasificación**: NATO UNCLASSIFIED

---

## 🚀 Capacidades Estratégicas Implementadas

### 1. 🎯 MANDO Y CONTROL (C2)
**Status**: ✅ Operacional

Análisis de capacidades de Command, Control, Communications, Computers & Intelligence (C4I):
- 20 partidas específicas: Software C2, Radios HF, Bunkers, Ciberdefensa
- 25 reportes operativos específicos
- Niveles operacionales: Estratégico, Operacional, Táctico, Guerra Electrónica
- Unidades: 5 comandos especializados

### 2. ✈️ MANIOBRA AÉREA
**Status**: ✅ Operacional (NUEVO en v3.0)

Análisis de operaciones de combate aéreo y proyección de poder:
- **Personal (P)**: Sueldos Pilotos, Bonificación Vuelo, Tripulación Aerotécnica
- **Training (T)**: Horas de Vuelo, Simulador Full Mission, Combate Aéreo Avanzado, Tiro Real
- **Material (M)**: Repuestos Super Tucano, PDM, Munición Aérea, Rotables, Overhaul Motor
- **Operaciones (O)**: Combustible JP1, Seguro Casco Aéreo
- **Facilities (F)**: Mantenimiento Pista, Hangar Alerta, Torre Control
- 27 partidas específicas + 25 reportes operativos
- Niveles: Combate Aéreo, Apoyo Cercano, Interdicción, Reconocimiento
- Unidades: 6 alas de combate y escuadrones

### 3. 🛡️ CIBERDEFENSA
**Status**: 🚧 Placeholder (Próximamente)

Operaciones cibernéticas defensivas y ofensivas.

### 4. 📦 LOGÍSTICA
**Status**: 🚧 Placeholder (Próximamente)

Sostenimiento y cadena de suministro militar.

---

## 📂 Ingesta Real de Datos (v5.0)

### Modo de Operación

El sistema ahora soporta **dos modos**:

#### 🛠️ MODO SIMULACIÓN (Demo)
- Datos generados automáticamente para demo
- 70 partidas presupuestarias por capacidad
- 25 reportes operativos simulados
- Ideal para: Testing, capacitación, demos sin datos sensibles

#### 📂 MODO INGESTA DE DATOS (Real)
- Carga archivos Excel (eSIGEF) con partidas presupuestarias
- Carga PDFs múltiples con reportes operativos
- Normalización automática de columnas
- Clasificación inteligente por capacidad y DOTMLPF

### Función de Desambiguación Inteligente

```python
clasificar_partida_inteligente(codigo, descripcion, unidad) → (capacidad, tag_dotmlpf)
```

**Reglas de negocio:**

1. **Clasificación de Capacidad** (C2, MANIOBRA, etc.):
   - Scoring por keywords en descripción
   - Desempate por unidad beneficiaria
   - Fallback a default si no hay match

2. **Clasificación DOTMLPF** (D, O, T, M, L, P, F):
   - Mapeo por código presupuestario eSIGEF
   - Refinamiento por keywords si código es genérico
   - Ejemplo: '710401' → 'M' (Material)

**Ejemplos:**

| Código | Descripción | Unidad | → Capacidad | Tag |
|--------|-------------|--------|-------------|-----|
| 710101 | Servidor C2 principal | COA | C2 | M |
| 510201 | Sueldos pilotos | Ala 21 | MANIOBRA | P |
| 530510 | Horas vuelo | ESMA | MANIOBRA | T |
| 750201 | Mantenimiento pista | Ala 23 | MANIOBRA | F |

### Normalización de Columnas Excel

El sistema reconoce múltiples variantes de nombres:

- **Código**: Código / Codigo / Cod_Presupuestario / CodPresup / Partida
- **Descripción**: Descripción / Descripcion / Detalle / Desc / Concepto
- **Asignado**: Asignado / Monto_Asignado / Presupuesto / Codificado
- **Ejecutado**: Ejecutado / Monto_Ejecutado / Devengado / Ejecucion
- **Unidad**: Unidad / Unidad_Beneficiaria / Beneficiario / Dependencia

### Procesamiento de PDFs

- Extracción de texto con `pdfplumber`
- Detección automática de unidad en el texto
- Integración con motor NLP para análisis de riesgo
- Soporte para múltiples PDFs simultáneos

### Conector de Base de Datos (Placeholder)

Preparado para conexión directa a sistemas institucionales:

```python
# Configuración futura
DB_HOST = 'postgresql://esigef.institucional.ec'
DB_PORT = 5432
DB_NAME = 'esigef_produccion'
```

**Requiere:**
- Variables de entorno para credenciales
- Usuario read-only
- Conexión SSL/TLS
- IP whitelisting
- Auditoría de accesos

---

## 🏗️ Arquitectura del Sistema v5.0

### Flujo de Navegación v5.0

```
1. Landing Page → Selección de Capacidad
                  ├─ [🎯 MANDO Y CONTROL] → Dashboard C2
                  ├─ [✈️ MANIOBRA AÉREA]  → Dashboard Maniobra
                  ├─ [🛡️ CIBERDEFENSA]     → (En desarrollo)
                  └─ [📦 LOGÍSTICA]        → (En desarrollo)

2. Dashboard → Sidebar con Selector de Modo (v5.0)
   │
   ├─ 🛠️ MODO SIMULACIÓN (Demo)
   │   └─ Datos generados automáticamente
   │
   ├─ 📂 MODO INGESTA DE DATOS (Real)
   │   ├─ Uploader Excel (eSIGEF)
   │   ├─ Uploader PDFs (Reportes múltiples)
   │   └─ Info Conector BD
   │
   ├─ ⚙️ Configuración Pesos DOTMLPF (v4.0)
   │   └─ Sliders con validación suma 100%
   │
   └─ 📊 Métricas Ejecutivas

3. Dashboard → 3 TABS
   ├─ TAB 1: Situational Awareness (Heatmap Ponderado + Radar)
   ├─ TAB 2: Gobernanza & Calidad del Gasto (Matriz Eficiencia)
   └─ TAB 3: Data Intelligence (NLP + Risk Analysis)
```

### Módulos Principales v5.0

1. **Módulo de Ingesta Real de Datos (v5.0 - NUEVO)**
   - Función `clasificar_partida_inteligente()`: Desambiguación con reglas de negocio
   - Función `procesar_excel_esigef()`: Normalización automática de columnas
   - Función `extraer_texto_pdf()`: Procesamiento con pdfplumber
   - Función `procesar_pdfs_reportes()`: Batch processing de múltiples PDFs
   - Placeholder `conectar_base_institucional()`: Conector BD PostgreSQL/Oracle

2. **Módulo de Scoring Ponderado Estratégico (v4.0)**
   - Función `calculate_weighted_dotmlpf_scores()`: Cálculo con pesos configurables
   - Controles interactivos en sidebar con validación
   - Fórmula: Alistamiento = 70% weighted + 30% NLP
   - Visualizaciones con valores ponderados (Heatmap + Radar)

3. **Generación de Datos Estructurados (Modo Simulación)**
   - 70 registros presupuestarios por capacidad
   - Datos específicos C2: Software, Radios, Bunkers, Servidores
   - Datos específicos Maniobra: Pilotos, Horas Vuelo, Repuestos, PDM, Hangares
   - Códigos presupuestarios clasificados por DOTMLPF
   - Orden de Batalla Real FAE (15 unidades)

4. **Generación de Datos No Estructurados (Modo Simulación)**
   - 25 reportes operativos por capacidad
   - Simulación de PDFs de novedades militares
   - Análisis de sentimiento y riesgo operacional

5. **Motor NLP de Análisis de Riesgo**
   - Clasificación automática de sentimiento (critical, warning, positive)
   - Cálculo de Risk Score (0-100)
   - Índice de Alistamiento Operativo
   - Integración con PDFs reales (v5.0)

6. **Clasificador Multidimensional DOTMLPF x Capacidad**
   - Eje Capacidades: C2, MANIOBRA, CIBERDEFENSA, LOGISTICA
   - Niveles operacionales por capacidad
   - Eje DOTMLPF: Doctrine, Organization, Training, Material, Leadership, Personnel, Facilities
   - Clasificación automática mediante keywords y códigos presupuestarios

7. **Algoritmo de Calidad del Gasto**
   - KPI 1: % Ejecución Presupuestaria
   - KPI 2: Índice de Alistamiento Operativo (ponderado)
   - Matriz de Eficiencia (4 cuadrantes)
   - Integración con pesos DOTMLPF estratégicos

8. **Dashboard Interactivo Streamlit**
   - TAB 1: Situational Awareness (Heatmap DOTMLPF Ponderado, Radar Chart)
   - TAB 2: Gobernanza & Calidad del Gasto (Scatter Matrix Eficiencia)
   - TAB 3: Data Intelligence (NLP Analytics + Risk Assessment)

---

## 🚀 Instalación y Ejecución

### Requisitos Previos

```bash
Python 3.8 o superior
pip (gestor de paquetes)
```

### Instalación

```bash
# Clonar repositorio
git clone <repository-url>
cd capacidades_analisis

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

---

## 📊 Framework DOTMLPF

### Taxonomía de Capacidades (NATO Standard)

| Código | Componente | Descripción |
|--------|------------|-------------|
| **D** | Doctrine | Principios, tácticas, técnicas y procedimientos |
| **O** | Organization | Estructura organizacional y relaciones |
| **T** | Training | Instrucción especializada y certificación |
| **M** | Material | Equipos, sistemas, armas y tecnología |
| **L** | Leadership | Liderazgo y desarrollo de mandos |
| **P** | Personnel | Recursos humanos y personal especializado |
| **F** | Facilities | Infraestructura e instalaciones |

---

## 🎯 Niveles de Comando y Control

1. **C2 Estratégico**: Comando Nacional, Integración Conjunta
2. **C2 Operacional**: Teatro de Operaciones, Coordinación Interagencias
3. **C2 Táctico**: Unidades de combate, Comunicaciones de campo
4. **Guerra Electrónica**: Radar, Frecuencias, Espectro Electromagnético

---

## 📈 Matriz de Calidad del Gasto

### Cuadrantes de Eficiencia

```
                    │
   SUB-EJECUCIÓN    │   EFICIENTE
   (Optimizar)      │   (Mantener)
                    │
────────────────────┼────────────────────
                    │
   CRÍTICO          │   INEFICIENTE
   (Intervenir)     │   (Auditar)
                    │
```

**Métricas de Clasificación:**
- **Eficiente**: Ejecución > 80% AND Alistamiento > 80%
- **Ineficiente (Auditar)**: Ejecución > 80% AND Alistamiento < 50%
- **Sub-Ejecución**: Ejecución < 50% AND Alistamiento > 80%
- **Crítico**: Ejecución < 50% AND Alistamiento < 50%

---

## 🧠 Motor NLP - Análisis de Riesgo

### Keywords de Riesgo (Risk Score)

| Keyword | Score | Severidad |
|---------|-------|-----------|
| crítico | 100 | Máxima |
| inoperativo | 90 | Muy Alta |
| falla | 80 | Alta |
| obsoleto | 85 | Alta |
| sin capacitación | 75 | Media-Alta |

### Fórmula de Alistamiento

```
Índice de Alistamiento = 100 - Risk Score
```

---

## 🔍 Casos de Uso

### 1. Auditoría Presupuestaria

Detectar unidades con alta ejecución presupuestaria pero bajo alistamiento operativo (posible ineficiencia o malversación).

### 2. Identificación de Gaps de Capacidad

Visualizar en el Heatmap DOTMLPF las celdas vacías (inversión $0) que representan capacidades críticas sin financiamiento.

### 3. Priorización de Recursos

Utilizar el Radar Chart para identificar desequilibrios (ej: mucho Material, poca Capacitación).

### 4. Análisis de Riesgo Operacional

Procesar reportes de novedades mediante NLP para generar alertas automáticas sobre sistemas críticos.

---

## 📁 Estructura de Archivos

```
capacidades_analisis/
│
├── app.py                 # Aplicación principal Streamlit
├── requirements.txt       # Dependencias Python
├── README.md             # Este archivo
└── .gitignore            # Archivos a ignorar en Git
```

---

## 🛡️ Seguridad y Clasificación

**Clasificación de Seguridad**: NATO UNCLASSIFIED

Este sistema utiliza datos **simulados** para propósitos de demostración. En un entorno de producción:

- Implementar autenticación y autorización (OAuth 2.0, SAML)
- Encriptación de datos en tránsito (TLS 1.3) y en reposo (AES-256)
- Auditoría completa de accesos (SIEM integration)
- Clasificación de datos según normativa nacional (ej: RESERVADO, CONFIDENCIAL, SECRETO)

---

## 🔧 Configuración Avanzada

### Variables de Entorno (Producción)

```bash
export SIEC_DB_HOST="postgresql://..."
export SIEC_CLASSIFICATION_LEVEL="UNCLASSIFIED"
export SIEC_LOG_LEVEL="INFO"
```

### Integración con Bases de Datos Reales

Modificar `generate_structured_data()` para conectarse a eSIGEF:

```python
import psycopg2

def load_from_esigef():
    conn = psycopg2.connect(...)
    query = "SELECT * FROM partidas_presupuestarias WHERE año=2024"
    return pd.read_sql(query, conn)
```

---

## 📚 Referencias Técnicas

- **NATO DOTMLPF Framework**: Allied Administrative Publication (AAP)
- **Joint Publication 3-0**: Joint Operations (US Department of Defense)
- **eSIGEF**: Sistema de Gestión Financiera - Ministerio de Economía y Finanzas (Ecuador)
- **Streamlit Documentation**: https://docs.streamlit.io
- **Plotly Python**: https://plotly.com/python/

---

## 👥 Contribuciones

Este proyecto es una POC académica y de demostración. Para contribuciones:

1. Fork del repositorio
2. Crear branch de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

---

## 📄 Licencia

Este proyecto es de uso académico y demostrativo.

---

## 📧 Contacto

Para consultas sobre el sistema SIEC-C2, contactar al equipo de Defense Analytics.

---

**Última actualización**: 2026-01-18
**Versión**: 5.1 (DOTmLPF-P + Doctrinal Reference + Real Data Mapping)
**Status**: POC Funcional con Framework JCIDS Completo
**Nuevas Capacidades v5.1**: 📚 Página Doctrinal JCIDS | 🏛️ Taxonomía DOTmLPF-P (8 componentes) | 🗺️ Mapeo Fuentes Reales | 📊 Explicación Radar Chart
**Capacidades v5.0**: 📂 Excel ETL | 📄 PDF Processing | 🧠 Desambiguación Inteligente | 💾 DB Connector Ready
**Capacidades v4.0**: ⚖️ Scoring Ponderado | 🏛️ OOB Real FAE (15 unidades)
