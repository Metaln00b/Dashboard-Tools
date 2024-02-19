import time
import random
import serial

# Serielle Schnittstelle initialisieren (anpassen Sie den Port und die Baudrate entsprechend)
#ser = serial.Serial('/dev/rfcomm0', 115200)
ser = serial.Serial('/dev/ttyUSB0', 115200)

max_drehzahl = 8000  # Maximale Motordrehzahl in U/min
max_geschwindigkeit = 220  # Maximale Geschwindigkeit in km/h
ps = 200  # Leistung des Fahrzeugs in PS
beschleunigungszeit_0_100 = 8  # Geschätzte Beschleunigungszeit von 0-100 km/h in Sekunden
gaenge = 5  # Anzahl der Gänge im Fahrzeug

# Berechnung der durchschnittlichen Beschleunigung von 0-100 km/h
durchschnittliche_beschleunigung = (max_geschwindigkeit * 1000 / 3600) / beschleunigungszeit_0_100

# Simulation von Beschleunigung und Schalten bis zur Höchstgeschwindigkeit
drehzahl = 0
geschwindigkeit = 0
gang = 1

while True:
    while geschwindigkeit < max_geschwindigkeit:
        # Zufällige Beschleunigung simulieren basierend auf der durchschnittlichen Beschleunigung
        beschleunigung = random.uniform(durchschnittliche_beschleunigung - 2, durchschnittliche_beschleunigung + 2)
        
        # Berechnung der neuen Drehzahl und Geschwindigkeit
        drehzahl = min(drehzahl + int(beschleunigung * 100), max_drehzahl)
        geschwindigkeit = min(geschwindigkeit + beschleunigung * 3.6, max_geschwindigkeit)  # Umrechnung von m/s in km/h
        
        # Schalten alle 10 km/h
        if geschwindigkeit > gang * 10 and gang < gaenge:
            gang += 1
            # Drehzahl wird auf den oberen Bereich des aktuellen Gangs gesetzt
            drehzahl = int((gang * max_drehzahl) / gaenge)
        
        # Daten über Bluetooth-Serielle-Schnittstelle senden
        data_to_send = f"{{{drehzahl:.0f}&{geschwindigkeit:.0f}&100&90&0&0&0&70}}"
        ser.write(data_to_send.encode())
        
        # Warten für 1 Sekunde, um die Simulation realistischer zu machen
        time.sleep(0.2)

    # Starke Abbremsung und Runterschalten
    while geschwindigkeit > 0:
        # Zufällige Verzögerung simulieren
        verzögerung = random.uniform(1, 5)
        
        # Berechnung der neuen Drehzahl und Geschwindigkeit während des Bremsens
        drehzahl -= int(verzögerung * 100)
        geschwindigkeit = max(geschwindigkeit - verzögerung * 3.6, 0)  # Umrechnung von m/s in km/h
        
        # Runterschalten alle 10 km/h (falls möglich)
        if geschwindigkeit < gang * 10 and gang > 1:
            gang -= 1
            # Drehzahl wird auf den unteren Bereich des aktuellen Gangs gesetzt
            drehzahl = int((gang * max_drehzahl) / gaenge)
        
        # Daten über Bluetooth-Serielle-Schnittstelle senden
        data_to_send = f"{{{drehzahl:.0f}&{geschwindigkeit:.0f}&100&90&0&0&0&70}}"
        ser.write(data_to_send.encode())
        
        # Warten für 1 Sekunde, um die Simulation realistischer zu machen
        time.sleep(0.2)

# Serielle Schnittstelle schließen
ser.close()
