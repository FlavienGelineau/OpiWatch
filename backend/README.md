# Interface de simulation - OpiWatch
Express JS + MongoDB data interface for dealing with multiple peripheral sources.

## Description générale
Dans son fonctionnement réel, l'application devra collecter des données provenant de multiple sources distinctes (qui sont les signaux vitaux des patients d'un hôpital ou d'une EPHAD par exemple), pour les analyser. Ce serveur de données s'acquite de la âche de centralisation.

## Contenu
L'outil présente 3 services :
- *Asclepios* : Serveur ExpressJS + MongoDB qui va enregistrer des sources de données périphériques, régulièrement collecter les données qu'elles produisent et les stocker de manière centralisée.
- *Disciple* : Source de données périphérique. Serveur ExpressJS qui produit des une série de données imitant des signaux vitaux (ECG, courbe sp02, ...) et pouvant transmettre cette série sur un réseau local.
- *Disciple-dashboard* : Serveur ExpressJS qui peut collecter la donnée d'une source de données périphérique et l'afficher en temps réel dans un navigateur web. Permet de contrôler la série produite par le service *disciple*

## Description des services

### Disciple

### Disciple-dashboard

### Asclepios

## Installation et tests

### Disclaimer
Les services vivent dans des conteneurs Docker donc à priori il n'y a pas besoin d'installer node ou quoi que ce soit d'autre que Docker pour pouvoir installer les différents serveurs.

Les conteneurs ne vivent pas encore sur des repo distants, il faut donc récupérer le code source depuis le repo github et build les conteneurs (mais pas de panique, c'est pas sorcier).

La procédure a été testé sur MacOS, à priori elle s'étend à des architectures unix. Le fonctionnement de Docker sous Windows étant particulier, je ne sais pas à quel point cela s'étend à cet os.

### Procédure
#### 1. Cloner le repos github
En vous plaçant dans le dossier où vous souhaitez enregistre l'application :

Normalement ça doit prendre un max de temps parce que **FLAVIEN GIT SES DATASETS**

````
> git clone git@github.com:FlavienGelineau/OpiWatch.git
> cd OpiWatch/backend
````
On se place en suite dans le dossier contenant les codes sources des différents serveurs.

#### 2. Créer les build des conteneurs
En principe, si vous n'avez pas de conteneurs docker en cours d'éxecution auparavant, la liste des processus docker donnée par la commande `docker ps` doit être vide :

````=bash
> docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAME
````

**Build pour le serveur disciple**
````
> docker build --no-cache -t opiwatch-disciple ./disciple
> docker run -p 49160:8080 -d opiwatch-disciple
````
Ne faites pas attention au arguments pour le moment, typiquement le `49160:8080` est voué à disparaître les ports réseau seront attribués dynamiquement.

À partir de là, vous avez une source de données qui tourne en local sur votre machine, accéssible à l'url `localhost:49160/history` :

````
> curl -i localhost:49160/history
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: http://localhost:49161
Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept
Content-Type: text/plain; charset=utf-8
Content-Length: 1857
ETag: W/"741-GzdzoFOL5zQqgFE0ONbW2J6kbAI"
Date: Wed, 06 Mar 2019 15:41:04 GMT
Connection: keep-alive

{
    "data": [<la série de données générée>], 
    "name": <l'id du serveur générant la série>
}
````

**Build pour le serveur disciple-dashboard**

*Avoir des données c'est bien, les voir, c'est mieux !*

Le build est très semblable à ce qui a été fait précédemment.

````
> docker build --no-cache -t opiwatch-disciple-dashboard ./disciple-dashboard
> docker run -p 49161:8080 -d opiwatch-disciple-dashboard
````

Maintenant, en ouvrant un navigateur et en allant à l'adresse `localhost:49161/dashboard` vous verrez la série temporelle défiler devant vos yeux. Pour le moment elle ne ressemble à rien, c'est normal. Par ailleurs les différents services sont encore en développement, c'est donc normal qu'il y ait quelques artefacts qui traînent en attendant d'avoir une version plus stable (typiquement, la courbe défile de manière saccadée, c'est normal et sera réglé par la suite).

**Build pour le serveur asclepios**

Ici, la procédure est beaucoup plus simple pour le build et tient en une ligne :

````
> cd asclepios
> docker-compose up --build
````
Vous allez avoir plein de trucs qui s'affichent, c'est normal (développement => plein de logs pas encore dissimulés).

Pour le moment, on ne peut enregistrer qu'un seul patient (parce que je dois régler l'attribution/detections des ip et que pour le moment elles sont codées en dur dans les sources).


Enregistrement : 
````
> curl localhost:49100/register
=> renvoie un id (name)
````
Utilisation : `
````
> curl localhost:49100/patient/< cet id >
=> série de données en temps réel correspondant à ce patient
````

