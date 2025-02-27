import sqlite3
import paho.mqtt.client as mqtt
import json

MQTT_Topic = "Home/BedRoom/#"
mqttBroker ="broker.hivemq.com"

# SQLite DB Name
DB_Name =  "IoT.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists Temperature_Data ;
create table Temperature_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Temperature text
);


drop table if exists Humidity_Data ;
create table Humidity_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Humidity text
);


drop table if exists Lumens_Data ;
create table Lumens_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Lumens text
);
"""

class DatabaseManager():
	def __init__(self):
		self.conn = sqlite3.connect(DB_Name)
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

def build_db(TableSchema):
	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()

	#Create Tables
	sqlite3.complete_statement(TableSchema)
	curs.executescript(TableSchema)

	#Close DB
	curs.close()
	conn.close()

# Function to save Temperature to DB Table
def Temp_Data_Handler(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	SensorID = json_Dict['Sensor_ID']
	Data_and_Time = json_Dict['Date']
	try:
	    Temperature = json_Dict['Temperature']
	    #Push into DB Table
	    dbObj = DatabaseManager()
	    dbObj.add_del_update_db_record("insert into Temperature_Data (SensorID, Date_n_Time, Temperature) values (?,?,?)",[SensorID, Data_and_Time, Temperature])
	    del dbObj
	except:
	    print("Inserted Temperature Data into Database.")

# Function to save Humidity to DB Table
def Humidity_Data_Handler(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	SensorID = json_Dict['Sensor_ID']
	Data_and_Time = json_Dict['Date']
	try:
	    Humidity = json_Dict['Humidity']
	    dbObj = DatabaseManager()
	    dbObj.add_del_update_db_record("insert into Humidity_Data (SensorID, Date_n_Time, Humidity) values (?,?,?)",[SensorID, Data_and_Time, Humidity])
	    del dbObj
	except:
	    print("Inserted Humidity Data into Database.")

# Function to save Light to DB Table
def Lumens_Data_Handler(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	SensorID = json_Dict['Sensor_ID']
	Data_and_Time = json_Dict['Date']
	try:
	    Lumens = json_Dict['Lumens']
	    dbObj = DatabaseManager()
	    dbObj.add_del_update_db_record("insert into Lumens_Data (SensorID, Date_n_Time, Lumens) values (?,?,?)",[SensorID, Data_and_Time, Lumens])
	    del dbObj
	except:
	    print("Inserted Lumens Data into Database.")

def sensor_Data_Handler(Topic, jsonData):
	##Topic="Home/BedRoom/1/Temperature"
	if Topic == "Home/BedRoom/1/Temperature":
		Temp_Data_Handler(jsonData)
	elif Topic == "Home/BedRoom/1/Humidity":
		Humidity_Data_Handler(jsonData)	
	elif Topic == "Home/BedRoom/1/Lumens":
		Lumens_Data_Handler(jsonData)

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    sensor_Data_Handler(message.topic, message.payload)

if __name__ == "__main__":
	build_db(TableSchema)
	##Topic="Home/BedRoom/1/Temperature"
	##client = mqtt.Client("mqttx_bd83f7566")
	client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"mqttx_bd83f7566")
	client.connect(mqttBroker) 

	client.subscribe(MQTT_Topic)
	client.on_message=on_message
	client.loop_forever() 