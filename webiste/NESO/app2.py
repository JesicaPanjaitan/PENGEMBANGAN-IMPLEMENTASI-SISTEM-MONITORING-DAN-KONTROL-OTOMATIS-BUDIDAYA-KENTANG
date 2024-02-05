from flask import Flask, render_template, request
import paho.mqtt.client as mqtt
import mysql.connector

app = Flask(__name__)

# # Konfigurasi MQTT broker
# mqtt_broker = "192.168.43.19"
# mqtt_port = 1883
# topic1 = "topic/perangkat1"
# topic3 = "topic/perangkat3"

def run_query(query):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='neso'
    )
    
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone() 
    connection.close()
    
    return result
# def on_publish(client, userdata, mid):
#     print("Pesan berhasil terkirim")

# # Inisialisasi MQTT client
# mqtt_client = mqtt.Client()
# mqtt_client.on_publish = on_publish
# mqtt_client.connect(mqtt_broker, mqtt_port)

@app.route('/')
def index():
    # Query pertama
    query1 = 'SELECT * FROM nesodb WHERE id = "sensor1" ORDER BY timestamp DESC LIMIT 1'
    data1 = run_query(query1)
    
    # Query kedua
    query2 = 'SELECT * FROM nesodb WHERE id = "sensor2" ORDER BY timestamp DESC LIMIT 1'
    data2 = run_query(query2)
    
    # Query ketiga
    query3 = 'SELECT * FROM nesodb WHERE id = "sensor3" ORDER BY timestamp DESC LIMIT 1'
    data3 = run_query(query3)
    
    # Query keempat
    query4 = 'SELECT * FROM nesodb WHERE id = "sensor4" ORDER BY timestamp DESC LIMIT 1'
    data4 = run_query(query4)

    return render_template('home.html',data1=data1,data2=data2,data3=data3,data4=data4)

@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        status1 = request.form.get('status1')
        status2 = request.form.get('status2')
        status3 = request.form.get('status3')

        if status1 == 'on':
            mqtt_client.publish(topic1, 'ON')
        elif status1 == 'off':
            mqtt_client.publish(topic1, 'OFF')

        if status2 == 'on':
            mqtt_client.publish(topic3, 'ON3')
        elif status2 == 'off':
            mqtt_client.publish(topic3, 'OFF3')

        if status3 == 'on':
            mqtt_client.publish(topic3, 'ON4')
        elif status3 == 'off':
            mqtt_client.publish(topic3, 'OFF4')

    return render_template('control.html')

if __name__ == '__main__':
    app.run(debug=True)
