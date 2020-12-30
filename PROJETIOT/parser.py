from math import pow, sqrt
import json


file_path = "data_Leo" #source path
dest_path = "results_leo"

exp_separator = "#MESURE "
nb_mesures = 20

gtw_switcher = {"eui-58a0cbfffe800570":"RSSI_gen",
				"eui-58a0cbfffe800692":"RSSI_hall",
				"eui-58a0cbfffe8003e5":"RSSI_td"}

device_list = ["arduino_1", "arduino_2", "arduino_3", "arduino_4", "arduino_5"]

gtw_list = ["RSSI_gen", "RSSI_hall", "RSSI_td"]
gtw_coord = {"gen":	{"x":34,"y":0.95},
			"hall":	{"x":0.44,"y":5.15}, 
			"td":	{"x":11.05,"y":42.2}}


######################  RSSI  #############################


def load_data():
	"""loads data. 
	data a table of measure series"""

	data = ""
	with open(file_path, 'r') as f:
		data = f.read()
	data = data.split(exp_separator)
	for i in range(len(data)):
		data[i]=data[i].splitlines()

	return data


def load_single_measure(s):
	#takes string returns json
	i = s.index('{')
	s = s[i:]
	json_mes = json.loads(s)

	return json_mes



def mean_measure(s):
	#retourne série sans doublon (les doublon sont juste moyennés)
	ret = [] #retourne série = tableau de dictionnaires
	serie = s #pour ne pas modifier l'originale

	for device in device_list:
		ret.append({"device":device})

		for gtw in gtw_list:
			count = 0
			rssi_sum = 0
			for measure in serie:
				if measure["device"]==device:
					if gtw in measure:
						count +=1
						rssi_sum += measure[gtw]

			if count != 0:			
				moy = rssi_sum / count
				ret[-1][gtw] = moy

	#petit nettoyage des data
	ret2=[]
	for i in ret:
		if len(i)!=1:
			ret2.append(i)

	return ret2


def process_single_measure(json_mes):
	"""returns rssi list for a single measure
	ret : {"device":"arduino1"
			<idGtw>:<rssiValue>
			<idGtw>:<rssiValue>
			...}
	"""
	# load device name
	ret = {"device":json_mes["dev_id"]}

	#load RSSIs
	gtw_data = json_mes["metadata"]["gateways"]
	for gtw in gtw_data:
		gtw_id = gtw["gtw_id"]
		if gtw_id in gtw_switcher:
			ret[gtw_switcher[gtw_id]] = gtw["rssi"]

	return ret


def wash_serie(serie):
	#vire les mesures qui ont moins de 3 gtw
	ret = []
	for i,measure in enumerate(serie):
		if len(measure)>=4:
			ret.append(measure)

	return ret


def process_measure_series(serie):
	ret = []
	for measure in serie:
		json = load_single_measure(measure)
		ret.append(process_single_measure(json))

	#moyennage des mesures par arduino
	ret = mean_measure(ret)

	#supression des mesures avec moins de 3 gtw
	ret = wash_serie(ret)

	return ret


data = load_data()
data = data[1:]
processed = []

#by measure series
for serie in data:
	serie = serie[1:] #1st value is useless
	processed.append(process_measure_series(serie))


######################  POSITION  #############################

mapper ={
	"1": {
		"1": (0, 0.6),
		"2": (0, 2.4),
		"3": (0, 4.2),
		"4": (None, None),
		"5": (None, None)
	},
	"2": {
		"1": (1.8, 0.6),
		"2": (1.8, 2.4),
		"3": (1.8, 4.2),
		"4": (1.8, 6),
		"5": (None, None)
	},
	"3": {
		"1": (3.6, 0.6),
		"2": (3.6, 2.4),
		"3": (3.6, 4.2),
		"4": (3.6, 6),
		"5": (3.6, 7.8)
	},
	"4": {
		"1": (5.4, 0.6),
		"2": (5.4, 2.4),
		"3": (5.4, 4.2),
		"4": (5.4, 6),
		"5": (5.4, 7.8)
	},
	"5": {
		"1": (7.2, 0.6),
		"2": (7.2, 2.4),
		"3": (7.2, 4.2),
		"4": (7.2, 6),
		"5": (7.2, 7.8)
	},
	"6": {
		"1": (9, 0.6),
		"2": (9, 2.4),
		"3": (9, 4.2),
		"4": (9, 6),
		"5": (9, 7.8)
	},
	"7": {
		"1": (10.8, 0.6),
		"2": (10.8, 2.4),
		"3": (10.8, 4.2),
		"4": (10.8, 6),
		"5": (10.8, 7.8)
	},
	"8": {
		"1": (12.6, 0.6),
		"2": (12.6, 2.4),
		"3": (12.6, 4.2),
		"4": (12.6, 6),
		"5": (12.6, 7.8)
	},
	"9": {
		"1": (14.4, 0.6),
		"2": (14.4, 2.4),
		"3": (14.4, 4.2),
		"4": (14.4, 6),
		"5": (14.4, 7.8)
	},
	"10": {
		"1": (16.2, 0.6),
		"2": (16.2, 2.4),
		"3": (16.2, 4.2),
		"4": (16.2, 6),
		"5": (16.2, 7.8)
	},
	"11": {
		"1": (18, 0.6),
		"2": (18, 2.4),
		"3": (18, 4.2),
		"4": (18, 6),
		"5": (18, 7.8)
	},
	"12": {
		"1": (19.8, 0.6),
		"2": (19.8, 2.4),
		"3": (19.8, 4.2),
		"4": (19.8, 6),
		"5": (19.8, 7.8)
	},
	"13": {
		"1": (21.6, 0.6),
		"2": (21.6, 2.4),
		"3": (21.6, 4.2),
		"4": (21.6, 6),
		"5": (21.6, 7.8)
	},
	"14": {
		"1": (23.4, 0.6),
		"2": (23.4, 2.4),
		"3": (23.4, 4.2),
		"4": (23.4, 6),
		"5": (23.4, 7.8)
	},
	"15": {
		"1": (25.2, 0.6),
		"2": (25.2, 2.4),
		"3": (25.2, 4.2),
		"4": (25.2, 6),
		"5": (25.2, 7.8)
	},
	"16": {
		"1": (25.2, 9.6),
		"2": (23.4, 9.6),
		"3": (21.6, 9.6),
		"4": (19.8, 9.6),
		"5": (18, 9.6)
	},
	"17": {
		"1": (16.2, 9.6),
		"2": (14.4, 9.6),
		"3": (12.6, 9.6),
		"4": (10.8, 9.6),
		"5": (9, 9.6)
	},
	"18": {
		"1": (8.4, 11.4),
		"2": (8.4, 13.2),
		"3": (8.4, 15),
		"4": (8.4, 16.8),
		"5": (8.4, 18.6)
	},
	"19": {
		"1": (10.2, 11.4),
		"2": (10.2, 13.2),
		"3": (10.2, 15),
		"4": (10.2, 16.8),
		"5": (10.2, 18.6)
	},
	"20": {
		"1": (10.2, 20.4),
		"2": (10.2, 22.2),
		"3": (8.4, 20.4),
		"4": (8.4, 22.2),
		"5": (6.6, 22.2)
	},
	"21": {
		"1": (7.57, 31.16),
		"2": (8.23, 40.98),
		"3": (-2.89, 36.64),
		"4": (2.82, 41.8),
		"5": (2.82, 40)
	},
	"22": {
		"1": (2.82, 38.2),
		"2": (2.82, 36.4),
		"3": (2.82, 34.6),
		"4": (2.82, 32.8),
		"5": (2.82, 31)
	}
}


def add_coord(mesure, coord):
	mesure["x"]=coord[0]
	mesure["y"]=coord[1]


def get_coord(i_exp, i_arduino):
	return mapper[str(i_exp)][str(i_arduino)]


for i_exp,exp in enumerate(processed):
	for mesure in exp:
		i_arduino = mesure["device"][-1]
		coord = get_coord(i_exp+1, i_arduino)

		add_coord(mesure, coord)


final = []
#on enlève les mesues inutiles
for exp in processed:
	for mes in exp:
		if mes["x"]!=None:
			final.append(mes)




#######################   CALCUL POSITIONS   #################
for line in final:
	x = line["x"]
	y = line["y"]
	line["d_hall"] = sqrt(pow((gtw_coord["hall"]["x"] - x),2) + pow((gtw_coord["hall"]["y"] - y),2))
	line["d_gen"]  = sqrt(pow((gtw_coord["gen"]["x"] - x),2) + pow((gtw_coord["gen"]["y"] - y),2))
	line["d_td"]   = sqrt(pow((gtw_coord["td"]["x"] - x),2) + pow((gtw_coord["td"]["y"] - y),2))


######################   DUMP IN RESULT FILE   #####################
with open(dest_path, "w") as f:
	f.write("")

with open(dest_path, 'a') as f:
	for i in final :

		f.write(json.dumps(i)+"\n")



