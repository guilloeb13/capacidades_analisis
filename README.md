# SIEC v3.0: Sistema Integrado de Evaluación de Capacidades

## 🎯 Descripción General

POC (Proof of Concept) funcional End-to-End de un sistema de análisis estratégico para evaluación de **múltiples capacidades militares** basado en el framework **DOTMLPF de la OTAN**.

### **NUEVA VERSIÓN 3.0 - Arquitectura Modular Multicapacidad**

Esta versión implementa:
- ✅ **Landing Page** de selección de capacidad estratégica
- ✅ **Navegación dinámica** con st.session_state
- ✅ **Soporte multicapacidad**: Mando y Control, Maniobra Aérea, Ciberdefensa*, Logística*
- ✅ **Filtrado inteligente** de datos por capacidad seleccionada
- ✅ **Clasificadores automáticos** con machine learning (CAPABILITY_KEYWORDS)
- ✅ **Datos específicos** por capacidad (27 ítems Maniobra + 25 reportes)

*Ciberdefensa y Logística: placeholders para desarrollo futuro

### Arquitectura Tecnológica

- **Framework de Datos**: Lakehouse Híbrido (Datos Estructurados + NLP No Estructurado)
- **Stack Tecnológico**: Python 3.8+ | Streamlit | Pandas | Plotly | NumPy
- **Metodología**: NATO DOTMLPF Framework | Joint Publication 3-0
- **Versión**: 3.0 (Multi-Capability Architecture)
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

## 🏗️ Arquitectura del Sistema v3.0

### Flujo de Navegación

```
1. Landing Page → Selección de Capacidad
                  ├─ [🎯 MANDO Y CONTROL] → Dashboard C2
                  ├─ [✈️ MANIOBRA AÉREA]  → Dashboard Maniobra
                  ├─ [🛡️ CIBERDEFENSA]     → (En desarrollo)
                  └─ [📦 LOGÍSTICA]        → (En desarrollo)

2. Dashboard → 3 TABS + Sidebar
   ├─ TAB 1: Situational Awareness (Heatmap + Radar)
   ├─ TAB 2: Gobernanza & Calidad del Gasto
   ├─ TAB 3: Data Intelligence (NLP)
   └─ Sidebar: [⬅️ VOLVER AL INICIO] + Métricas + Filtros
```

### Módulos Principales

1. **Generación de Datos Estructurados (SQL Simulado)**
   - 80 registros presupuestarios por capacidad
   - Datos específicos C2: Software, Radios, Bunkers, Servidores
   - Datos específicos Maniobra: Pilotos, Horas Vuelo, Repuestos, PDM, Hangares
   - Códigos presupuestarios clasificados por DOTMLPF

2. **Generación de Datos No Estructurados (NLP Simulado)**
   - 50 reportes operativos de texto libre
   - Simulación de PDFs de novedades militares
   - Análisis de sentimiento y riesgo operacional

3. **Motor NLP de Análisis de Riesgo**
   - Clasificación automática de sentimiento (critical, warning, positive)
   - Cálculo de Risk Score (0-100)
   - Índice de Alistamiento Operativo

4. **Clasificador Multidimensional DOTMLPF x C2**
   - Eje C2: Estratégico, Operacional, Táctico, Guerra Electrónica
   - Eje DOTMLPF: Doctrine, Organization, Training, Material, Leadership, Personnel, Facilities
   - Clasificación automática mediante keywords y códigos presupuestarios

5. **Algoritmo de Calidad del Gasto**
   - KPI 1: % Ejecución Presupuestaria
   - KPI 2: Índice de Alistamiento Operativo
   - Matriz de Eficiencia (4 cuadrantes)

6. **Dashboard Interactivo Streamlit**
   - TAB 1: Situational Awareness (Heatmap DOTMLPF, Radar Chart)
   - TAB 2: Gobernanza & Calidad del Gasto (Scatter Matrix)
   - TAB 3: Data Intelligence (NLP Analytics)

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

**Última actualización**: 2026-01-13
**Versión**: 3.0 (Multi-Capability Architecture)
**Status**: POC Funcional Multicapacidad
**Nuevas Capacidades**: Maniobra Aérea ✈️ | Navegación Modular 🎯 | Landing Page 🚀
