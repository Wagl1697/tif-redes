// Conecto cliente al broker especificado en constructor.
var client = mqtt.connect("ws://test.mosquitto.org:8080/mqtt");
// Declaro topico.
var topico = "flask/mqtt";

// Declaro funcion que se ejecuta al conectarse.
function EventoConectar() {
  // Muestro en consola de navegador si se conecto.
  console.log("¡Conectado al broker!");
  // Suscribo cliente al topico.
  client.subscribe(topico, function (err) {
    if (!err) {
      // Si se conecto correctamente muestra en consola de navegador 'Se suscribio al topico'
      console.log("Se suscribió al tópico: '" + topico + "'");
    }
  });
}

// Funcion para captar mensaje y mostarlo.
function EventoMensaje(topic, message) {
  if (topic == topico) {
    // Muestra en consola navegador.
    console.log("Mensaje recibido en el tópico '" + topic + "': " + message.toString());
    // Reemplaza variable de html con mensaje de MQTT entrante.
    document.getElementById("mensaje_mqtt").innerHTML = message.toString();
  }
  // console.log(topic + " - " + message.toString());
  // client.end()
}


// Cliente sobrescribe sus funciones base con las funciones creadas para que sean ejecutadas.
client.on("connect", EventoConectar);
client.on("message", EventoMensaje);

