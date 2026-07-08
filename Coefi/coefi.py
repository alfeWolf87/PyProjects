from decimal import Decimal, getcontext, ROUND_HALF_UP

# Configurar el redondeo estándar (el de toda la vida: si es 5, sube)
REDONDEO = Decimal('0.001')

def calcular_km(delta_x_M, A_M, T_M, T_int, V, I, k_PE, A_PE, delta_x_PE, T_sensores):
    # Convertimos todas las entradas a tipo Decimal para no perder precisión
    delta_x_M = Decimal(str(delta_x_M))
    A_M = Decimal(str(A_M))
    T_M = Decimal(str(T_M))
    T_int = Decimal(str(T_int))
    V = Decimal(str(V))
    I = Decimal(str(I))
    k_PE = Decimal(str(k_PE))
    A_PE = Decimal(str(A_PE))
    delta_x_PE = Decimal(str(delta_x_PE))
    
    # 1. Validación (se mantiene igual)
    if len(T_sensores) != 5:
        raise ValueError("La lista de temperaturas 'T_sensores' debe tener exactamente 5 elementos.")
    
    # Convertir la lista de sensores a Decimal
    T_sensores_dec = [Decimal(str(T)) for T in T_sensores]
    
    # 2. Calcular la sumatoria
    sumatoria_T = sum(T_i - T_int for T_i in T_sensores_dec)
    
    # 3. Calcular la potencia eléctrica
    potencia_electrica = V * I
    
    # 4. Calcular el término de pérdidas
    perdidas_estructura = k_PE * (A_PE / delta_x_PE) * sumatoria_T
    
    # 5. Calcular el denominador del factor externo
    denominador = A_M * (T_M - T_int)
    if denominador == 0:
        raise ZeroDivisionError("Error: El denominador es cero.")
    
    factor_externo = -delta_x_M / denominador
    
    # 6. Ecuación final
    k_M = factor_externo * (potencia_electrica + perdidas_estructura)
    
    # Redondear el resultado final exactamente a 3 decimales
    return k_M.quantize(REDONDEO, rounding=ROUND_HALF_UP)

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    datos = {
        "delta_x_M": 0.05,
        "A_M": 0.25,
        "T_M": 298.15,
        "T_int": 323.15,
        "V": 12.0,
        "I": 1.5,
        "k_PE": 0.04,
        "A_PE": 1.2,
        "delta_x_PE": 0.1,
        "T_sensores": [321.5, 322.0, 320.8, 322.5, 321.2]
    }

    try:
        resultado = calcular_km(**datos)
        # El resultado ya es un objeto Decimal de 3 dígitos exactos
        print(f"El coeficiente k_M calculado es: {resultado} W/(m·K)")
    except Exception as e:
        print(f"Error en el cálculo: {e}")