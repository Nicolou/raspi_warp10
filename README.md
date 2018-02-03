# grafana et warp10 sur Raspberry PI

ce projet présente la mise en oeuvre de Warp10.io et Grafana sur raspberry PI
dans le but de récolter et d'exploiter des métriques provenant de capteurs externes.

Le stockage et l'extration des métriques se fait à partir de l'application warp10 (http://warp10.io)
Les données sont consultées via un navigateur web avec l'application Grafana  ( https://grafana.com/ )

## le projet en actions :
### Exemple exploitation des métriques :
![img](doc/images/graf1.png)
La consultation des relevés des capteurs se fait simplement via un navigateur web.

### les matériels mis en oeuvre :
![matos](doc/images/matos1.jpg)
le Raspbery PI 2 B, avec quelques capteurs connectés en I2C


## Comment faire ...
### schéma des composants logiciels
![matos](doc/images/schema_archi1.jpg)


Nginx : serveur web frontal utilisé en reverse-proxy afin de permettre aux clients ( tablette, ordi, smartphone ) d'accéder aux applcations en passant par le port standard http (80). Ceci permet parfois d'éviter aux clients d'être bloqués par les politiques de sécurité mises en places par les fournisseurs d'accès à internet.

Grafana : qu'on ne présente plus...

Warp10 : idem.

Application de capture en python : c'est là que réside le travail de programmation dont les sources sont fournies dans ce dêpot.
Cette appli est à adapter (ou a réécrire entièrement ) en fonction des capteurs à relever. C'est ce programme qui va écrire dans warp10 les métriques via une connexion http de type POST.


### procédure d'installation des logiciels

#### pré-requis
avant de commencer, il faut avoir un raspberry opérationnel. Le rasp utilisé pour ce projet est de type B version 2.
Le système d'exploitation est un linux installé à partir de la disptribution officielle [Raspbian](https://www.raspberrypi.org/downloads/raspbian/).

graver l'image derniere version de raspbian sur microSD (https://www.raspberrypi.org/documentation/installation/installing-images/linux.md)

Pour plus de facilité, activer le serveur ssh du rasp afin de s'y connecter depuis son ordinateur favori.
voir la commande
> sudo raspi-config.
	* timezone
	* clavier
	* ssh	
	* activer i2c

#### Nginx
1. installation : sudo apt-get install nginx
> sudo apt-get nginx
dans le fichier de conf /etc/nginx/sites-enabled/default, ajouter à la rubrique server{}
```
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html;
	server_name _;
	location / {
		try_files $uri $uri/ =404;
	}
	location /grafana/ {
		proxy_pass http://localhost:3000/;
	}
	location /warp10/ {
		proxy_pass http://localhost:8080/;
	}
        location /quantum/ {
                proxy_pass http://localhost:8090/;
        }
}
```
1. puis restart de nginx
> sudo systemctl restart nginx.service

site pour comprendre ... : https://homeserver-diy.net/wiki/index.php?title=Installation_et_configuration_d%E2%80%99un_reverse_proxy_avec_NginX

#### Warp10

1. prérequis installer java sdk8 pour ARM
pour cela aller sur le site d'oracle java http://www.oracle.com/technetwork/java/javase/downloads/index.html
et choisir __SDK v8__

un fois téléchargé le fichier jdk-8u151-linux-arm32-vfp-hflt.tar.gz, le décompresser dans /opt du rasp

1. installer warp10
aller sur le site http://www.warp10.io/getting-started/ pour télécharger l'archive tar.gz (clic sur le bouton gris download)

configuration en user root :
> sudo su -
> cd /opt/warp10-1.2.12-rc2/bin
> vi warp10-standalone.sh 
adapter :
```
JAVA_HOME=/opt/jdk1.8.0_151/       <--- fonction de votre install java
WARP10_HEAP=512m		   <--- limite par notre raspberry
WARP10_HEAP_MAX=512m               <--- idem
```

1. première exécution
> ./warp10-standalone.sh bootstrap

1. ouvrir le fichier /opt/warp10-1.2.12-rc2/etc/conf-standalone.conf
> vi /opt/warp10-1.2.12-rc2/etc/conf-standalone.conf
et redefinir `standalone.host = x.x.x.x`  ou x.x.x.x est l'adresse du lan du rasp. ( par exemple 192.168.0.0) 

1. configurer warp10 avec systemd pour redémarrage automatique lors du boot du raspberry
copier le fichier war10.service  vers /lib/systemd/system
> cp /opt/warp10-1.2.12-rc2/bin/warp10.service /lib/systemd/system/
> chmod 644 /lib/systemd/system/pySensors.service /lib/systemd/system/warp10.service
> systemctl daemon-reload
puis démarrage de warp10 ( tada ! )
> systemctl start warp10-service

(fin de la config en user root)













