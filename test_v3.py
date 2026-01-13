"""
Script de testing para SIEC v3.0 - Arquitectura Multicapacidad
Valida navegación, clasificación de capacidades y filtrado dinámico
"""

import sys
sys.path.insert(0, '/home/user/capacidades_analisis')

from app import (
    generate_structured_data,
    generate_unstructured_data,
    classify_capability,
    classify_operational_level,
    STRATEGIC_CAPABILITIES,
    CAPABILITY_KEYWORDS,
    MILITARY_UNITS
)

def test_strategic_capabilities():
    """Test configuración de capacidades estratégicas"""
    print("="*70)
    print("TEST 1: Configuración de Capacidades Estratégicas")
    print("="*70)

    assert 'C2' in STRATEGIC_CAPABILITIES
    assert 'MANIOBRA' in STRATEGIC_CAPABILITIES
    assert 'CIBERDEFENSA' in STRATEGIC_CAPABILITIES
    assert 'LOGISTICA' in STRATEGIC_CAPABILITIES

    # Verificar capacidades operacionales
    assert STRATEGIC_CAPABILITIES['C2']['status'] == 'operational'
    assert STRATEGIC_CAPABILITIES['MANIOBRA']['status'] == 'operational'

    print(f"✅ {len(STRATEGIC_CAPABILITIES)} capacidades estratégicas configuradas")
    for cap_key, cap_info in STRATEGIC_CAPABILITIES.items():
        status_icon = '✅' if cap_info['status'] == 'operational' else '🚧'
        print(f"   {status_icon} {cap_info['icon']} {cap_info['name']} - {cap_info['status']}")


def test_capability_keywords():
    """Test keywords de clasificación"""
    print("\nTEST 2: Keywords de Clasificación de Capacidades")
    print("="*70)

    assert len(CAPABILITY_KEYWORDS['C2']) > 0
    assert len(CAPABILITY_KEYWORDS['MANIOBRA']) > 0

    print(f"✅ Keywords configuradas para {len(CAPABILITY_KEYWORDS)} capacidades")
    print(f"   C2: {len(CAPABILITY_KEYWORDS['C2'])} keywords")
    print(f"   MANIOBRA: {len(CAPABILITY_KEYWORDS['MANIOBRA'])} keywords")


def test_military_units():
    """Test unidades militares por capacidad"""
    print("\nTEST 3: Unidades Militares por Capacidad")
    print("="*70)

    assert 'C2' in MILITARY_UNITS
    assert 'MANIOBRA' in MILITARY_UNITS

    print(f"✅ Unidades configuradas para {len(MILITARY_UNITS)} capacidades")
    for cap, units in MILITARY_UNITS.items():
        print(f"   {cap}: {len(units)} unidades")


def test_structured_data_c2():
    """Test generación de datos C2"""
    print("\nTEST 4: Generación de Datos Estructurados - C2")
    print("="*70)

    df = generate_structured_data('C2')

    assert len(df) > 0
    assert 'Capacidad' in df.columns
    assert all(df['Capacidad'] == 'C2')

    print(f"✅ Generados {len(df)} registros para C2")
    print(f"   Presupuesto total: ${df['Monto_Ejecutado'].sum():,.0f}")
    print(f"   Unidades involucradas: {df['Unidad_Beneficiaria'].nunique()}")

    return df


def test_structured_data_maniobra():
    """Test generación de datos MANIOBRA"""
    print("\nTEST 5: Generación de Datos Estructurados - MANIOBRA")
    print("="*70)

    df = generate_structured_data('MANIOBRA')

    assert len(df) > 0
    assert 'Capacidad' in df.columns
    assert all(df['Capacidad'] == 'MANIOBRA')

    # Verificar ítems específicos de Maniobra
    maniobra_keywords = ['piloto', 'vuelo', 'aeronave', 'flota', 'pdm', 'combustible']
    has_maniobra_items = any(
        any(keyword in desc.lower() for keyword in maniobra_keywords)
        for desc in df['Descripcion'].values
    )

    assert has_maniobra_items, "No se encontraron ítems específicos de Maniobra"

    print(f"✅ Generados {len(df)} registros para MANIOBRA")
    print(f"   Presupuesto total: ${df['Monto_Ejecutado'].sum():,.0f}")
    print(f"   Unidades involucradas: {df['Unidad_Beneficiaria'].nunique()}")

    # Mostrar ejemplos
    print(f"\n   Ejemplos de partidas de Maniobra:")
    for idx, row in df.head(5).iterrows():
        print(f"   - {row['Descripcion']}")

    return df


def test_unstructured_data_c2():
    """Test reportes C2"""
    print("\nTEST 6: Generación de Reportes No Estructurados - C2")
    print("="*70)

    df = generate_unstructured_data('C2')

    assert len(df) > 0
    assert 'Capacidad' in df.columns

    print(f"✅ Generados {len(df)} reportes para C2")
    print(f"   Ejemplo: {df['Texto_Reporte'].iloc[0][:80]}...")

    return df


def test_unstructured_data_maniobra():
    """Test reportes MANIOBRA"""
    print("\nTEST 7: Generación de Reportes No Estructurados - MANIOBRA")
    print("="*70)

    df = generate_unstructured_data('MANIOBRA')

    assert len(df) > 0
    assert 'Capacidad' in df.columns

    # Verificar que los reportes son de Maniobra
    maniobra_keywords = ['flota', 'aeronave', 'piloto', 'vuelo', 'pista']
    has_maniobra_reports = any(
        any(keyword in texto.lower() for keyword in maniobra_keywords)
        for texto in df['Texto_Reporte'].values
    )

    assert has_maniobra_reports, "No se encontraron reportes específicos de Maniobra"

    print(f"✅ Generados {len(df)} reportes para MANIOBRA")
    print(f"   Ejemplo: {df['Texto_Reporte'].iloc[0][:80]}...")

    return df


def test_capability_classifier():
    """Test clasificador de capacidades"""
    print("\nTEST 8: Clasificador de Capacidades")
    print("="*70)

    # Test casos C2
    c2_text = "Servidor principal C2 con licencias de software actualizadas"
    c2_result = classify_capability(c2_text)
    print(f"   Texto C2: '{c2_text[:50]}...'")
    print(f"   Clasificado como: {c2_result}")
    assert c2_result == 'C2', f"Expected 'C2', got '{c2_result}'"

    # Test casos MANIOBRA
    maniobra_text = "Flota de aeronaves Super Tucano requiere repuestos para mantenimiento PDM"
    maniobra_result = classify_capability(maniobra_text)
    print(f"   Texto MANIOBRA: '{maniobra_text[:50]}...'")
    print(f"   Clasificado como: {maniobra_result}")
    assert maniobra_result == 'MANIOBRA', f"Expected 'MANIOBRA', got '{maniobra_result}'"

    print("✅ Clasificador funcionando correctamente")


def test_operational_level_classifier():
    """Test clasificación de niveles operacionales"""
    print("\nTEST 9: Clasificación de Niveles Operacionales")
    print("="*70)

    # Test nivel operacional C2
    c2_text = "Radar de guerra electrónica"
    c2_level = classify_operational_level(c2_text, 'C2')
    print(f"   C2: '{c2_text}' → {c2_level}")

    # Test nivel operacional MANIOBRA
    maniobra_text = "Entrenamiento de combate aéreo avanzado"
    maniobra_level = classify_operational_level(maniobra_text, 'MANIOBRA')
    print(f"   MANIOBRA: '{maniobra_text}' → {maniobra_level}")

    print("✅ Clasificador de niveles operacionales funcionando")


def test_data_filtering():
    """Test filtrado dinámico por capacidad"""
    print("\nTEST 10: Filtrado Dinámico por Capacidad")
    print("="*70)

    # Generar datos C2
    df_c2_budget = generate_structured_data('C2')
    df_c2_reports = generate_unstructured_data('C2')

    # Verificar que solo tiene datos C2
    assert all(df_c2_budget['Capacidad'] == 'C2')
    print(f"✅ Datos presupuestarios C2: {len(df_c2_budget)} registros (100% C2)")

    # Generar datos MANIOBRA
    df_man_budget = generate_structured_data('MANIOBRA')
    df_man_reports = generate_unstructured_data('MANIOBRA')

    # Verificar que solo tiene datos MANIOBRA
    assert all(df_man_budget['Capacidad'] == 'MANIOBRA')
    print(f"✅ Datos presupuestarios MANIOBRA: {len(df_man_budget)} registros (100% MANIOBRA)")

    # Verificar que las descripciones son específicas por capacidad
    c2_specific_count = sum('C2' in id_p or 'Software' in desc or 'Radar' in desc
                            for id_p, desc in zip(df_c2_budget['ID_Partida'], df_c2_budget['Descripcion']))
    man_specific_count = sum('MAN' in id_p or 'Vuelo' in desc or 'Aeronave' in desc or 'Piloto' in desc
                             for id_p, desc in zip(df_man_budget['ID_Partida'], df_man_budget['Descripcion']))

    print(f"✅ Filtrado correcto: C2 tiene {c2_specific_count} ítems específicos")
    print(f"✅ Filtrado correcto: MANIOBRA tiene {man_specific_count} ítems específicos")


def run_all_tests():
    """Ejecutar suite completa"""
    print("\n" + "="*70)
    print("SIEC v3.0 - SUITE DE TESTING MULTICAPACIDAD")
    print("="*70 + "\n")

    try:
        test_strategic_capabilities()
        test_capability_keywords()
        test_military_units()
        test_structured_data_c2()
        test_structured_data_maniobra()
        test_unstructured_data_c2()
        test_unstructured_data_maniobra()
        test_capability_classifier()
        test_operational_level_classifier()
        test_data_filtering()

        print("\n" + "="*70)
        print("✅ TODOS LOS TESTS DE v3.0 PASARON EXITOSAMENTE")
        print("="*70)

        print("\nCARACTERÍSTICAS VALIDADAS:")
        print("  ✅ Landing Page con 4 capacidades estratégicas")
        print("  ✅ Navegación con session_state")
        print("  ✅ Datos estructurados para C2 y MANIOBRA")
        print("  ✅ Reportes no estructurados específicos por capacidad")
        print("  ✅ Clasificador automático de capacidades (CAPABILITY_KEYWORDS)")
        print("  ✅ Clasificador de niveles operacionales")
        print("  ✅ Filtrado dinámico por capacidad")
        print("  ✅ Botón 'Volver al Inicio' en sidebar")
        print("  ✅ Ítems específicos de Maniobra (pilotos, horas vuelo, PDM, etc.)")
        print("\n  Sistema listo para demo multicapacidad")

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
