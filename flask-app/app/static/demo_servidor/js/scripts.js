var socket = io.connect('http://' + document.domain + ':' + location.port);

            // Se ejecuta el evento de un mensaje mqtt
            socket.on("mqtt_message", function (msg) {
                console.log("Mensaje recibido en el tópico '" + msg.topic + "': " + msg.payload);  // Muestro por consola el tópico y mensaje recibido

                $('#mensaje').text(msg.payload);    // Actualizo el texto que se encuentra en el recuadro principal, con el mensaje recibido

            });