"""Ejercicio 1 - Sanitización y análisis estadístico de sensores."""

DEFAULT_UBICACION = "No especificada"


def limpiar_registro_sensor(registro_raw):
    sensor_id = str(registro_raw.get("sensor_id", "")).strip().upper()

    temperatura_cruda = registro_raw.get("temperatura")
    if isinstance(temperatura_cruda, (int, float)):
        temperatura = float(temperatura_cruda)
    else:
        texto = str(temperatura_cruda or "").strip()
        texto = texto.replace("°", "").replace("C", "").replace("c", "").strip()
        texto = texto.replace(",", ".")
        if not texto:
            raise ValueError(f"Temperatura invalida para el sensor '{sensor_id}'")
        try:
            temperatura = float(texto)
        except ValueError as exc:
            raise ValueError(
                f"Temperatura no numerica: '{registro_raw.get('temperatura')}'"
            ) from exc

    ubicacion_cruda = registro_raw.get("ubicacion")
    ubicacion = str(ubicacion_cruda).strip() if ubicacion_cruda is not None else ""
    if not ubicacion:
        ubicacion = DEFAULT_UBICACION

    return {"sensor_id": sensor_id, "temperatura": temperatura, "ubicacion": ubicacion}


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    if not lista_sensores_limpios:
        return [], 0.0

    lista_sensores_alerta = [
        registro["sensor_id"]
        for registro in lista_sensores_limpios
        if registro["temperatura"] > umbral_temperatura
    ]
    promedio = sum(registro["temperatura"] for registro in lista_sensores_limpios) / len(
        lista_sensores_limpios
    )
    return lista_sensores_alerta, round(promedio, 2)


if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 31,8 °C", "ubicacion": "Planta Sur"},
        {"sensor_id": " SENSOR-003", "temperatura": "19C", "ubicacion": ""},
        {"sensor_id": "sensor-004 ", "temperatura": "28,9C"},
        {"sensor_id": "SENSOR-005", "temperatura": "33.2°C", "ubicacion": "  Planta Mura "},
    ]

    limpios = [limpiar_registro_sensor(raw) for raw in registros_crudos]

    umbral = 30.0
    en_alerta, promedio = generar_resumen_sensores(limpios, umbral)

    print("=" * 62)
    print("REPORTE DE SENSORES - EcoTech Solutions")
    print("=" * 62)
    for registro in limpios:
        print(
            f"{registro['sensor_id']:<12} {registro['temperatura']:>6.2f} C  "
            f"{registro['ubicacion']}"
        )
    print("-" * 62)
    print(f"Umbral de alerta : {umbral:.2f} C")
    print(f"Sensores en alerta: {', '.join(en_alerta) if en_alerta else 'ninguno'}")
    print(f"Promedio global   : {promedio:.2f} C")
    print("=" * 62)
