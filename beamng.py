import time
import serial
import socket, struct

localIP = "0.0.0.0"
localPort = 4444
bufferSize = 256

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

#Car variables
carData = {}
maxRpm = 4000

def decodeFlag(flag):
    flagBin = str(bin(flag))
    flags = {"showTurbo":newBool(flagBin[2]),"showKM":not newBool(flagBin[1]),"showBAR":not newBool(flagBin[0])}
    return flags

def newBool(string):
    if(string == "0"):
        return False
    if(string == "1"):
        return True
	

def decodeLights(lightsAvailable,lightsActive):
    lightsAvBin = str(bin(lightsAvailable))[2:][::-1]
    lightsActBin = str(bin(lightsActive))[2:][::-1]
    lights = {}
    totalLights = ["shift_light","full_beam","handbrake","pit_limiter","tc","left_turn","right_turn","both_turns","oil_warn","battery_warn","abs","spare_light"]
    for i in range(0,12):
        try:
            lights[totalLights[i]] = newBool(lightsActBin[i])
        except Exception:
            lights[totalLights[i]] = False	
    return lights

def readData():
    global carData
    data = UDPServerSocket.recvfrom(bufferSize)
    unpackedData = struct.unpack("I4sHBBfffffffIIfff16s16sxxxx",data[0])
    carData = {"time":unpackedData[0],
            "carName":unpackedData[1].decode("utf-8"),
            "flags": decodeFlag(unpackedData[2]),
            "gear": unpackedData[3],
            "PLID": unpackedData[4],
            "speed": unpackedData[5],
            "rpm": unpackedData[6],
            "turboPressure":unpackedData[7],
            "engTemp":unpackedData[8],
            "fuel":unpackedData[9],
            "oilPressure":unpackedData[10],
            "oilTemp":unpackedData[11],
            "lights":decodeLights(unpackedData[12],unpackedData[13]),
            "throttle": unpackedData[14],
            "brake": unpackedData[15],
            "clutch": unpackedData[16],
            "misc1": unpackedData[17],
            "misc2": unpackedData[18]
            }
	
ser = serial.Serial('/dev/ttyUSB0', 115200)
while True:
    readData()
    if(maxRpm < carData["rpm"]):
        maxRpm = carData["rpm"]
    drehzahl = carData["rpm"]
    geschwindigkeit = carData["speed"] * 3.6
    fuel_level_percent = carData["fuel"] * 100.0
    coolant_temp_degC = carData["engTemp"]
    # Daten über Bluetooth-Serielle-Schnittstelle senden
    # RPM FUEL COOLANT LEFT RIGHT HANDBRAKE OIL
    data_to_send = f"{{{drehzahl:.0f}&{geschwindigkeit:.0f}&{fuel_level_percent:.0f}&{coolant_temp_degC:.0f}&0&0&0&80.0}}"
    ser.write(data_to_send.encode())

# Serielle Schnittstelle schließen
ser.close()