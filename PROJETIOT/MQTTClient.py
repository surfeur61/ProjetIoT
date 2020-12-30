import paho.mqtt.client as mqtt
import json
import testPars

app_id = "030398"
app_key = "ttn-account-v2.zIp6IPVVKgEW_fMuCCSG2fbmk7rosYNxYitFb9QEZwY"
host = "eu.thethings.network"
count = 0
strTest = {"app_id": "030398", "dev_id": "arduino_otaa", "hardware_serial": "00EC54127B22570C", "port": 1, "counter": 521, "payload_raw": "FSo=", "payload_fields": {"Data": {"Humidity": 42, "Temperature": 21}}, "metadata": {"time": "2020-12-25T16:58:46.250333843Z", "frequency": 868.1, "modulation": "LORA", "data_rate": "SF7BW125", "airtime": 46336000, "coding_rate": "4/5", "gateways": [{"gtw_id": "eui-58a0cbfffe800692", "timestamp": 1826269403, "time": "2020-12-25T16:58:46.412625074Z", "channel": 0, "rssi": -70, "snr": 9.25, "rf_chain": 0}, {"gtw_id": "eui-58a0cbfffe8003e5", "timestamp": 85013771, "time": "2020-12-25T16:58:46.252034902Z", "channel": 0, "rssi": -55, "snr": 9.5, "rf_chain": 0}]}}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic='+/devices/+/up', qos=0)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global count
    count+=1

    print(msg.topic+" "+str(msg.payload))
    decoded_message = str(msg.payload.decode("utf-8", "ignore"))
    decoded_list=json.loads(decoded_message)
    with open('data.json', 'a') as outfile:
        outfile.write("Value N "+ str(count)+"\n")
        json.dump(decoded_list, outfile)
        outfile.write("\n")

def getDataFromJson(msg):
    global strTest
    decoded_list=json.loads(strTest)




if __name__ == '__main__':

    client = mqtt.Client(client_id=app_id)

    client.username_pw_set(username=app_id, password=app_key)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, 1883, 60)
        
    testPars.getDataFromJson()
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
