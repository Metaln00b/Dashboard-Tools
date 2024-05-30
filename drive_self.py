import time
import keyboard
import serial

def berechne_geschwindigkeit(motordrehzahl, gang, getriebe_uebersetzungen, reifen_breite, reifen_profil, felgendurchmesser, achsantrieb_uebersetzung):
    if gang < 1 or gang > len(getriebe_uebersetzungen):
        gang = 1

    uebersetzung = getriebe_uebersetzungen[gang - 1]
    radumdrehungen_pro_minute = motordrehzahl / (uebersetzung * achsantrieb_uebersetzung)
    reifendurchmesser = (2 * reifen_profil / 100 * reifen_breite + felgendurchmesser * 25.4) / 1000
    umfang_des_rades = reifendurchmesser * 3.14159
    geschwindigkeit_mps = umfang_des_rades * radumdrehungen_pro_minute / 60
    geschwindigkeit_kmh = geschwindigkeit_mps * 3.6
    return geschwindigkeit_kmh
    
def berechne_motordrehzahl(geschwindigkeit, gang, getriebe_uebersetzungen, reifen_breite, reifen_profil, felgendurchmesser, achsantrieb_uebersetzung):
    if gang < 1 or gang > len(getriebe_uebersetzungen):
        gang = 1

    reifendurchmesser = (2 * reifen_profil / 100 * reifen_breite + felgendurchmesser * 25.4) / 1000
    umfang_des_rades = reifendurchmesser * 3.14159
    geschwindigkeit_mps = geschwindigkeit / 3.6
    radumdrehungen_pro_minute = geschwindigkeit_mps / umfang_des_rades * 60
    uebersetzung = getriebe_uebersetzungen[gang - 1] * achsantrieb_uebersetzung
    motordrehzahl = radumdrehungen_pro_minute * uebersetzung
    return motordrehzahl

# Serielle Schnittstelle initialisieren (anpassen Sie den Port und die Baudrate entsprechend)
#ser = serial.Serial('/dev/rfcomm0', 115200)
ser = serial.Serial('/dev/ttyUSB1', 115200)

getriebe_uebersetzungen = [3.545, 2.105, 1.429, 1.029, 0.838]

# Reifenabmessungen
reifen_breite = 145  # in mm
reifen_profil = 65  # in Prozent
felgendurchmesser = 14  # in Zoll

# Übersetzungsverhältnis des Achsantriebs
achsantrieb_uebersetzung = 4.111

max_drehzahl = 7000  # Maximale Motordrehzahl in U/min
max_geschwindigkeit = 200  # Maximale Geschwindigkeit in km/h
max_coolant_temp_degC = 130
max_fuel_level_percent = 100

gang = 1
drehzahl = 0
geschwindigkeit = 0
blinker_l = False
blinker_r = False
coolant_temp_degC = 90
fuel_level_percent = 50
handbrake = False
oil_temp_degC = 70

accelerate = True
iteration = 1

while True:
    if accelerate:
        geschwindigkeit += 1
        geschwindigkeit = max(0, min(geschwindigkeit, max_geschwindigkeit))

        coolant_temp_degC += 1
        coolant_temp_degC = max(0, min(coolant_temp_degC, max_coolant_temp_degC))

        fuel_level_percent += 1
        fuel_level_percent = max(0, min(fuel_level_percent, max_fuel_level_percent))
    else:
        geschwindigkeit -= 1
        geschwindigkeit = max(0, min(geschwindigkeit, max_geschwindigkeit))

        coolant_temp_degC -= 1
        coolant_temp_degC = max(0, min(coolant_temp_degC, max_coolant_temp_degC))

        fuel_level_percent -= 1
        fuel_level_percent = max(0, min(fuel_level_percent, max_fuel_level_percent))


    if geschwindigkeit >= max_geschwindigkeit:
        accelerate = False
        handbrake = True
    elif geschwindigkeit == 0:
        accelerate = True
        handbrake = False
    
    #speed_kmh = berechne_geschwindigkeit(drehzahl, gang, getriebe_uebersetzungen, reifen_breite, reifen_profil, felgendurchmesser, achsantrieb_uebersetzung)
    motordrehzahl = berechne_motordrehzahl(geschwindigkeit, gang, getriebe_uebersetzungen, reifen_breite, reifen_profil, felgendurchmesser, achsantrieb_uebersetzung)
    
    # Begrenzen
    drehzahl = max(0, min(motordrehzahl, max_drehzahl))
    geschwindigkeit = max(0, min(geschwindigkeit, max_geschwindigkeit))

    if (drehzahl >= 5000):
    	if (gang >= 1 and gang < len(getriebe_uebersetzungen)):
            gang += 1
            print("Gang ", gang, "\n")
    	
    if (drehzahl <= 2000):
    	if (gang > 1 and gang <= len(getriebe_uebersetzungen)):
            gang -= 1
            print("Gang ", gang, "\n")

    if (iteration >= 1000):
        blinker_l = not blinker_l
        blinker_r = not blinker_r
        iteration = 1

    # Daten über Bluetooth-Serielle-Schnittstelle senden
    # RPM FUEL COOLANT LEFT RIGHT HANDBRAKE OIL
    data_to_send = f"{{{drehzahl:.0f}&{geschwindigkeit:.0f}&{fuel_level_percent:.0f}&{coolant_temp_degC:.0f}&{blinker_l:.0f}&{blinker_r:.0f}&{handbrake:.0f}&{oil_temp_degC:.0f}}}"
    ser.write(data_to_send.encode())
    
    time.sleep(0.05)
    iteration += iteration

# Serielle Schnittstelle schließen
ser.close()
