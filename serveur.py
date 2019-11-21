# !/usr/bin/python3
import socket
import time
import psutil
import platform

hote=''
port=14528

serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #création de la socket serveur
serveur_socket.bind((hote,port))                                    #association du port / accepte toutes les IP
print("Le serveur ecoute sur le port "+str(port))

while True:
    os_name=platform.system()                                       #récupération de l'OS utilisé
    users=psutil.users()                                            #récupération des utilisateurs connectés
    info_str=""                                                     #initialisation de la variable info_str qui sera envoyée au client
    serveur_socket.listen(5)                                        #Autorise 5 échecs de connexion avant de refuser toute connexion
    connexion,info_client=serveur_socket.accept()                   
    info_str=os_name+";"                                            #ajout de l'OS dans la chaîne info_str
    for i in range(0,len(users)):                                   
        info_str=info_str+users[i][0]+";"                           #parcours le tableau de users puis les ajout à la chaîne info_str
    connexion.send(info_str.encode())                               #encode et envoie la chaîne info_str
