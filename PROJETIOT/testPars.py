import json
strTest = {"app_id": "030398", "dev_id": "arduino_otaa", "hardware_serial": "00EC54127B22570C", "port": 1, "counter": 521, "payload_raw": "FSo=", "payload_fields": {"Data": {"Humidity": 42, "Temperature": 21}}, "metadata": {"time": "2020-12-25T16:58:46.250333843Z", "frequency": 868.1, "modulation": "LORA", "data_rate": "SF7BW125", "airtime": 46336000, "coding_rate": "4/5", "gateways": [{"gtw_id": "eui-58a0cbfffe800692", "timestamp": 1826269403, "time": "2020-12-25T16:58:46.412625074Z", "channel": 0, "rssi": -70, "snr": 9.25, "rf_chain": 0}, {"gtw_id": "eui-58a0cbfffe8003e5", "timestamp": 85013771, "time": "2020-12-25T16:58:46.252034902Z", "channel": 0, "rssi": -55, "snr": 9.5, "rf_chain": 0}]}}
idArduino = ''
nameArduino = ''
data = []
gateways = [[]]

# il faudrait ajouter dans un tableau les locations de base des gateways (lattitude/longitude)

def getDataFromJson():
    global strTest
    global idArduino
    global nameArduino
    global data
    global gateways

    try :
        idArduino = strTest["hardware_serial"]
        print(idArduino)
    except :
        print('no hardware_serial')

    try :
        nameArduino = strTest["dev_id"]
        print(nameArduino)
    except :
        print('no dev_id')

    try :
        data.append(strTest["payload_fields"]["Data"]["Humidity"])
        data.append(strTest["payload_fields"]["Data"]["Temperature"])
        print(strTest["payload_fields"]["Data"]["Humidity"])
        print(strTest["payload_fields"]["Data"]["Temperature"])
    except :
        print('no data')
  
    gateways = [[''] * 3 for i in range(len(strTest["metadata"]["gateways"]))]
    
    try : 
        for nbGateways in range(len(strTest["metadata"]["gateways"])):
            gateways[nbGateways][0] = strTest["metadata"]["gateways"][nbGateways]["gtw_id"]
            gateways[nbGateways][1] = strTest["metadata"]["gateways"][nbGateways]["time"]
            gateways[nbGateways][2] = strTest["metadata"]["gateways"][nbGateways]["rssi"]
        
        print(gateways)
    except :
        print('no data')
    



