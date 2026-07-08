import serial
import time

# Configuración del puerto
# En Linux suele ser '/dev/ttyUSB0' o '/dev/ttyACM0'
# En Windows suele ser 'COM3', 'COM4', etc.
puerto = 'COM3' 
baudios = 9600

try:
    # Inicializar conexión
    ser = serial.Serial(puerto, baudios, timeout=1)
    time.sleep(2)  # Espera a que el microcontrolador se reinicie
    
    while True:
        # Enviar datos
        mensaje = "H" # Ejemplo: Encender un LED
        ser.write(mensaje.encode('utf-8'))
        print(f"Enviado: {mensaje}")
        
        # Leer respuesta
        if ser.in_waiting > 0:
            linea = ser.readline().decode('utf-8').strip()
            print(f"Recibido: {linea}")
            
        time.sleep(1)

except serial.SerialException as e:
    print(f"Error de conexión: {e}")
except KeyboardInterrupt:
    print("\nFinalizado por el usuario")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()