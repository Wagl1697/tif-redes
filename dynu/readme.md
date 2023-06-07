# CronJob para actualizar DDNS Dynu
##Configuracion
Para mantener actualizada la IP a la que apuntar el dominio DDNS deberá de agregarse un cronjob


```
cd ~
mkdir /dynu
cd dynu
chmod 700 dynu.sh
crontab -e
```

Agregar el siguiente comando al final del crontab

```
*/5****~/dynu/dynu.sh>>/dev/null 2>&1
```

