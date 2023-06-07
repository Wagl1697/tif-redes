import os
import json
import eventlet
from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, make_response, session
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)
#Configuración de la app de Flask
# app.config['SERVER_NAME'] = '0.0.0.0'

# Configuración de la librería flask_mqtt
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
topic = 'flask/mqtt'    # Tópico al que se conecta la app

mqtt = Mqtt(app, connect_async=True)
socketio = SocketIO(app, cors_allowed_origins='*') # , manage_session=False
bootstrap = Bootstrap(app)

# Diccionario donde se almacenarán los paquetes recibidos mediante MQTT
data = dict(
    topic='',
    payload=''
)

@app.route('/')
def index():
    return demo_servidor()

# Ruta para mostrar la Demo Servidor
@app.route('/DemoServidor')
def demo_servidor():
    return render_template("demo_servidor.html")

# Ruta para mostrar la Demo Cliente
@app.route('/DemoCliente')
def demo_cliente():
    return render_template("demo_cliente.html")


'''
============
    MQTT
============
'''

# Conexión del cliente
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    ''' Se ejecuta cuando se establece una conexión
    exitosa del cliente con el broker. '''

    if rc == 0:
        mqtt.subscribe(topic) # Suscribe el cliente mqtt al tópico actual
        print('\nConexión exitosa!')
        print(f"Tópico: {topic}\n")
    else:
        print('Conexión fallida. Código:', rc)


# Muestro mensaje recibido
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    ''' Guarda en un diccionario, el mensaje publicado en el tópico. '''
    global data
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    # Muestro por consola el dato recibido
    print(f'Mensaje recibido en el tópico "{data["topic"]}": {data["payload"]}')

    # Envía el valor del mensaje a través del canal "mqtt_message"
    socketio.emit('mqtt_message', {'topic': data["topic"], 'payload': data["payload"]})



'''
================
    SocketIO
================
'''

@socketio.on('connect')
def connect():
    print ('\nSocket client connected.', request.sid, '\n')
    socketio.send ('Socket server ready.')

@socketio.on('disconnect')
def disconnect():
    print('\nClient disconnected.', request.sid, '\n')


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8080, debug=True)

    # Aplicación de SocketIO que trabaja con WebSocket
    socketio.run(app, host='0.0.0.0', port=8080, use_reloader=True, debug=True)