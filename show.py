import time
import keyboard
import serial

# Serielle Schnittstelle initialisieren (anpassen Sie den Port und die Baudrate entsprechend)
#ser = serial.Serial('/dev/rfcomm0', 115200)
ser = serial.Serial('/dev/ttyUSB0', 115200)

max_drehzahl = 8000  # Maximale Motordrehzahl in U/min
max_geschwindigkeit = 220  # Maximale Geschwindigkeit in km/h
max_coolant_temp_degC = 130
max_fuel_level_percent = 100

drehzahl = 0
geschwindigkeit = 0
blinker_l = 0
blinker_r = 0
coolant_temp_degC = 75
fuel_level_percent = 35
handbrake = 0
oil_temp_degC = 70

while True:
    if keyboard.is_pressed('right'):
        drehzahl += 200  # Erhöhen Sie die Drehzahl um 100 U/min
        print("RPM ", drehzahl, "\n")
    elif keyboard.is_pressed('left'):
        drehzahl -= 200  # Verringern Sie die Drehzahl um 100 U/min
        print("RPM ", drehzahl, "\n")
    elif keyboard.is_pressed('up'):
        geschwindigkeit += 10  # Erhöhen Sie die Geschwindigkeit um 10 km/h
        print("Speed ", geschwindigkeit, "\n")
    elif keyboard.is_pressed('down'):
        geschwindigkeit -= 10  # Verringern Sie die Geschwindigkeit um 10 km/h
        print("Speed ", geschwindigkeit, "\n")
    elif keyboard.is_pressed('w'):
        coolant_temp_degC += 10
        print("Coolant ", coolant_temp_degC, "\n")
    elif keyboard.is_pressed('s'):
        coolant_temp_degC -= 10
        print("Coolant ", coolant_temp_degC, "\n")
    elif keyboard.is_pressed('a'):
        fuel_level_percent -= 10
        print("Fuel ", fuel_level_percent, "\n")
    elif keyboard.is_pressed('d'):
        fuel_level_percent += 10
        print("Fuel ", fuel_level_percent, "\n")
    elif keyboard.is_pressed(','):
        blinker_l = 1
    elif keyboard.is_pressed('.'):
        blinker_r = 1
    elif keyboard.is_pressed('space'):
        handbrake = 1
    else:
        blinker_r = 0 
        blinker_l = 0
        handbrake = 0
    
    
    
    # Begrenzen
    drehzahl = max(0, min(drehzahl, max_drehzahl))
    geschwindigkeit = max(0, min(geschwindigkeit, max_geschwindigkeit))
    coolant_temp_degC = max(0, min(coolant_temp_degC, max_coolant_temp_degC))
    fuel_level_percent = max(0, min(fuel_level_percent, max_fuel_level_percent))
    

    # Daten über Bluetooth-Serielle-Schnittstelle senden
    # RPM FUEL COOLANT LEFT RIGHT HANDBRAKE OIL
    data_to_send = f"{{{drehzahl:.0f}&{geschwindigkeit:.0f}&{fuel_level_percent:.0f}&{coolant_temp_degC:.0f}&{blinker_l}&{blinker_r}&{handbrake}&{oil_temp_degC:.0f}}}"
    ser.write(data_to_send.encode())
    
    time.sleep(0.05)

# Serielle Schnittstelle schließen
ser.close()
