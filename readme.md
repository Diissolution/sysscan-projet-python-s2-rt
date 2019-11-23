
# Projet Python (Sys_Scan)

Outil écrit en **python** permettant d'obtenir des informations sur une machine à distance à l'aide de son adresse IP.

23/11/2019
V1.1

## Patch notes
1.1 
* Ajout de la possiblité de sauvegarder des logs des résultats du scan (.txt)
* Changements mineurs des messages affichés

## Prérequis

  

- Python 3.7+

Installation Unix :
```
> sudo apt-get update
> sudo apt-get install python3.7
> python3 --version
```
Installation windows : 
[https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

- Module psutil : [https://pypi.org/project/psutil/](https://pypi.org/project/psutil/)

## Utilisation
Lancez sur les postes à scanner le script 
`> python3 serveur.py`

(Utiliser Cron/Crontab pour lancer le script à chaque démarrage sous Linux : [https://www.linuxtricks.fr/wiki/cron-et-crontab-le-planificateur-de-taches](https://www.linuxtricks.fr/wiki/cron-et-crontab-le-planificateur-de-taches) )

---

Lancez sur la machine administrateur le script 
`> python3 client.py`

Vous avez 3 possiblités lorsque vous effectuez un scan : 
1. En rentrant les adresses IP à la suite.
2. En laissant le script détecter le sous-réseau / réseau local, il scannera ensuite toutes les adresses présentes dans le réseau.
3. A partir d'un fichier contenant une liste d'adresses IP.
---
**addr.txt** est un fichier de test pour la fonction de scan à partir d'un fichier

---
__Option : Erreurs précises__

Lors de l'utilisation du script, vous devrez choisir d'afficher des erreurs précises ou simples.

Les erreurs **simples** sont des erreurs/messages du type 
> Connexion à 192.168.2.1 impossible

 Les erreurs **précises** sont les erreurs **systèmes brutes** du type
> (<class 'socket.gaierror'>, gaierror(-3, 'Temporary failure in name resolution'), <traceback object at 0x7fa536568148>)

---
**Détection automatique des adresses du réseau**
Lors de l'utilisation de la détection de sous réseau, le script vous liste les interfaces réseau disponibles.
Choisissez une interface, le script utilisera son adresse IP pour calculer celles des autres machines présentes sur le réseau.


---
**Format de fichier à respecter lors d'un scan à partir d'un fichier** :
Les adresses doivent être écrites **à la suite**, séparées par **un caractère** de votre choix, exemple :
> 192.168.12.2;192.168.12.3;192.168.2.2

Le format (txt,csv) n'importe pas

**Le fichier doit être écrit sur une unique ligne**

## Membres du projet :
```
Resta Antoine
Gaglio Quentin
Gaglio Thomas
```
