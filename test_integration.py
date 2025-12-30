"""
Script de testing de integración para SIEC-C2
Valida que todas las funciones principales funcionen correctamente
"""

import sys
sys.path.insert(0, '/home/user/capacidades_analisis')

from app import (
    generate_structured_data,
    generate_unstructured_data,
    analyze_sentiment_readiness,
    classify_c2_level,
    map_dotmlpf,
    calculate_quality_metrics,
    create_dotmlpf_matrix
)

def test_structured_data_generation():
    """Test generación de datos estructurados"""
    print("TEST 1: Generación de datos estructurados...")
    df_budget = generate_structured_data()

    assert len(df_budget) == 150, f"Expected 150 records, got {len(df_budget)}"
    assert 'ID_Partida' in df_budget.columns
    assert 'DOTMLPF_Tag' in df_budget.columns
    assert 'Monto_Asignado' in df_budget.columns

    print(f"✅ Generados {len(df_budget)} registros presupuestarios")
    print(f"   Columnas: {list(df_budget.columns)}")
    return df_budget

def test_unstructured_data_generation():
    """Test generación de datos no estructurados"""
    print("\nTEST 2: Generación de datos no estructurados...")
    df_reports = generate_unstructured_data()

    assert len(df_reports) == 50, f"Expected 50 reports, got {len(df_reports)}"
    assert 'Texto_Reporte' in df_reports.columns
    assert 'Report_ID' in df_reports.columns

    print(f"✅ Generados {len(df_reports)} reportes operativos")
    print(f"   Ejemplo: {df_reports['Texto_Reporte'].iloc[0][:80]}...")
    return df_reports

def test_nlp_analysis():
    """Test motor NLP"""
    print("\nTEST 3: Motor NLP - Análisis de sentimiento...")

    test_texts = [
        "Falla crítica en servidor principal por sobrecalentamiento",
        "Enlaces satelitales operando al 100% de capacidad",
        "Personal de radar sin curso de actualización vigente"
    ]

    for text in test_texts:
        result = analyze_sentiment_readiness(text)
        print(f"   Texto: {text[:50]}...")
        print(f"   Risk Score: {result['risk_score']}, Sentiment: {result['sentiment']}")

        assert 'risk_score' in result
        assert 'sentiment' in result
        assert 'readiness_index' in result

    print("✅ Motor NLP funcionando correctamente")

def test_classification():
    """Test clasificadores"""
    print("\nTEST 4: Clasificadores DOTMLPF x C2...")

    # Test C2 classification
    c2_level = classify_c2_level("Construcción de bunker estratégico de comando")
    print(f"   Clasificación C2: '{c2_level}'")
    assert c2_level in ['C2 Estratégico', 'C2 Operacional', 'C2 Táctico', 'Guerra Electrónica']

    # Test DOTMLPF mapping
    dotmlpf = map_dotmlpf('710101', 'Equipos de comunicación')
    print(f"   Mapeo DOTMLPF: '{dotmlpf}'")
    assert dotmlpf in ['D', 'O', 'T', 'M', 'L', 'P', 'F']

    print("✅ Clasificadores funcionando correctamente")

def test_metrics_calculation(df_budget, df_reports):
    """Test cálculo de métricas"""
    print("\nTEST 5: Cálculo de métricas de calidad...")

    # Primero necesitamos enriquecer df_reports con análisis NLP
    nlp_results = df_reports['Texto_Reporte'].apply(analyze_sentiment_readiness)
    df_reports['risk_score'] = nlp_results.apply(lambda x: x['risk_score'])
    df_reports['readiness_index'] = nlp_results.apply(lambda x: x['readiness_index'])

    df_metrics = calculate_quality_metrics(df_budget, df_reports)

    assert len(df_metrics) > 0
    assert 'Ejecucion_Pct' in df_metrics.columns
    assert 'Alistamiento_Pct' in df_metrics.columns
    assert 'Cuadrante' in df_metrics.columns

    print(f"✅ Métricas calculadas para {len(df_metrics)} unidades")
    print(f"   Cuadrantes: {df_metrics['Cuadrante'].value_counts().to_dict()}")
    return df_metrics

def test_dotmlpf_matrix(df_budget):
    """Test creación de matriz DOTMLPF"""
    print("\nTEST 6: Matriz DOTMLPF x C2...")

    # Enriquecer datos
    df_budget['C2_Level'] = df_budget['Descripcion'].apply(classify_c2_level)

    matrix = create_dotmlpf_matrix(df_budget)

    assert matrix.shape[1] == 7  # 7 componentes DOTMLPF
    assert matrix.shape[0] > 0   # Al menos un nivel C2

    print(f"✅ Matriz creada: {matrix.shape[0]} niveles C2 x {matrix.shape[1]} componentes DOTMLPF")
    print(f"   Dimensiones: {matrix.shape}")
    print(f"   Total invertido: ${matrix.sum().sum():,.0f}")

def run_all_tests():
    """Ejecutar todos los tests"""
    print("="*70)
    print("SIEC-C2 - SUITE DE TESTING DE INTEGRACIÓN")
    print("="*70)

    try:
        df_budget = test_structured_data_generation()
        df_reports = test_unstructured_data_generation()
        test_nlp_analysis()
        test_classification()
        df_metrics = test_metrics_calculation(df_budget, df_reports)
        test_dotmlpf_matrix(df_budget)

        print("\n" + "="*70)
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("="*70)
        print("\nRESUMEN:")
        print(f"  - {len(df_budget)} partidas presupuestarias generadas")
        print(f"  - {len(df_reports)} reportes operativos procesados")
        print(f"  - {len(df_metrics)} unidades militares analizadas")
        print(f"  - Sistema listo para deploy")

        return True

    except AssertionError as e:
        print(f"\n❌ TEST FALLIDO: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
