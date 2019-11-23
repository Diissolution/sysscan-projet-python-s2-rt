# !/usr/bin/python3
import socket #nécéssaire pour la connexion entre les machines
import sys   #nécéssaire pour afficher les erreurs système
import psutil #nécéssaire pour trouver les interfaces réseau de la machine
import ipaddress #nécéssaire pour trouver le réseau local
import os.path  #nééssaire pour tester l'existence d'un fichier
import colorama
from datetime import datetime
colorama.init()

# ------------------ Classe couleurs
# SGR color constants
# rene-d 2018 https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

#  ------------------ Création liste des interfaces réseau de la machine
int_ps=psutil.net_if_addrs()    #récupère toutes les infos sur les interfaces réseaux de la machine
int_list=[]                     #initialisation de la liste contenant uniquement le nom des intefaces
for i in int_ps.keys():         #ajoute à la liste int_list chaque nom d'interface trouvée
    int_list.append(i+" ("+int_ps[i][0].address+")")
    
# ------------------ Fonction SCAN d'@IP rentrées manuellement
def ip_liste():
    colorama.init()  
    print(Colors.RED+'/!\\'+Colors.YELLOW+' Entrez les adresses IP des Machines séparées par ";" : \n'+Colors.END)
    hotes=input(Colors.YELLOW+">> "+Colors.END)
    port=14528                                       #port utilisé pour la connexion
    hotesListe = hotes.split(';')                    #transforme la chaîne de caractère entrée en liste
    for i in hotesListe:                               #On parcourt la liste des @ des hôtes entrés par l'utilisateur
        try :
            client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(0.05)              #Attend 50ms avant de passer à l'essai suivant
        except :
            print (Colors.NEGATIVE+"Création de la socket impossible pour "+i+Colors.END)
        try :
            client_socket.connect((i, port))                                                        #Essaye de se connecter à l'hôte sur le port spécifié
            message_recu = client_socket.recv(1024).decode() 
            if ch_fich.upper()=="OUI":
                nouv_fich.write("["+i+"] :"+message_recu+"\n")                                       #Decode le message reçu de l'hôte
            print (Colors.YELLOW+"["+Colors.END+i+Colors.YELLOW+"]"+Colors.END+": "+message_recu)   #Affiche le message/les infos sous la forme [@IPmachine] : OS,Utilisateurs
            client_socket.close()                                                                   #Ferme la connexion
        except :
            print(Colors.NEGATIVE+"Connexion à "+i+" impossible"+Colors.END)                        #Erreur "simple"
            nouv_fich.write("Connexion à "+str(i)+" impossible\n")
            print(sys.exc_info())                                                                   #Erreur système "précise"
    if ch_fich.upper()=="OUI":
        nouv_fich.close()

# ----------------- Fonction SCAN d'@IP du réseau local

def ip_local():
    colorama.init()
    aff_err="OUI"                       #Par défaut, variable aff_err en OUI pour afficher toutes les erreurs
    port=14528                           #port utilisé pour la connexion
    print(Colors.YELLOW+"---- Scan du réseau local ----\n"+Colors.RED+"/!\\"+Colors.YELLOW+"Ecrivez le nom de l'interface (sans @IP) a utiliser pour détecter le réseau local"+Colors.END)
    for i in int_list:                  #affiche la liste des interfaces récupérées lignes 37-40
        if "lo" not in i:
            print(" > "+ i)
    print(Colors.YELLOW+"-----------------------------")
    ch_int=input(Colors.YELLOW+">> "+Colors.END)
    print(Colors.YELLOW+"Voulez vous afficher les erreurs de connexion?\nOui / Non : "+Colors.END) #Demande à l'utilisateur s'il souhaite les erreurs détaillées pour debug)
    aff_err=input(Colors.YELLOW+">> "+Colors.END)
    int_ip=int_ps[ch_int][0].address+"/"+int_ps[ch_int][0].netmask
    hote=ipaddress.ip_interface(int_ip) #convertit l'adresse IP de l'interface et le masque réseau en objet IPV4
    print(Colors.GREEN+"** Adresse utilisée: "+Colors.LIGHT_BLUE+str(hote)+Colors.GREEN+" **"+Colors.END)
    reseau_hote=hote.network #Trouve le réseau associé à l'objet IPV4 (l'adresse de l'interface)
    print(Colors.GREEN+"** Réseau détecté: "+Colors.LIGHT_BLUE+str(reseau_hote)+Colors.GREEN+" **"+Colors.END)
    listing_ip = list(reseau_hote.hosts()) #liste de toutes les machines du réseau
    print(Colors.GREEN+str(len(listing_ip))+" machines trouvées"+Colors.END)
    print(Colors.GREEN+"** Début du scan **"+Colors.END)
    for i in listing_ip:   #Connexion à chaque machine (IP) trouvée auparavant
        try :  
            client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(0.05)      #Attend 50ms avant de passer à l'essai suivant
        except :
            print (Colors.NEGATIVE+"Création de la socket impossible pour "+str(i)+Colors.END)
        try :
            client_socket.connect((str(i), port))                                               #Essaye de se connecter à l'hôte sur le port spécifié (converti en string)
            message_recu = client_socket.recv(1024).decode() 
            if ch_fich.upper()=="OUI":
                nouv_fich.write("["+i+"] :"+message_recu+"\n")                                   #Decode le message reçu de l'hôte                                    
            print (Colors.YELLOW+"["+Colors.END+str(i)+Colors.YELLOW+"]"+Colors.END+": "+message_recu)  #Affiche le message/les infos sous la forme [@IPmachine] : OS,Utilisateurs
            client_socket.close()                                                               #Ferme la connexion
        except :
            if aff_err.upper()=="OUI": 
                print(Colors.NEGATIVE+"Connexion à "+str(i)+" impossible"+Colors.END)             #Erreur "simple"                                                             
                print(sys.exc_info())                                                           #Erreur système "précise" SI l'utilisation l'a choisi
    if ch_fich.upper()=="OUI":
        nouv_fich.close()

# ------------------ Fonction SCAN d'@IP depuis un fichier  
  
def ip_fichier():                       #Par défaut, variable aff_err en OUI pour afficher toutes les erreurs
    colorama.init()
    aff_err="OUI"   
    port=14528                           #port utilisé pour la connexion     
    print(Colors.YELLOW+"---- Scan a partir d'un fichier ----\nEntrez le nom du fichier (avec extension)"+Colors.END)
    nom_fich=input(Colors.YELLOW+">> "+Colors.END)
    if os.path.isfile(nom_fich) == False :  #test si le fichier existe, sinon sort de la fonction
        print("Le fichier spécifié n'existe pas ou est un dossier")
        return #sort de la fonction
    print(Colors.YELLOW+"Entrez le caractère qui sépare les adresses"+Colors.END)
    carac=input(Colors.YELLOW+">> "+Colors.END)
    print(Colors.YELLOW+"Voulez vous afficher les erreurs de connexion?\nOui / Non : "+Colors.END) #Demande à l'utilisateur s'il souhaite les erreurs détaillées pour debug)
    aff_err=input(Colors.YELLOW+">> "+Colors.END)
    f=open(nom_fich,'r')                #Ouverture du fichier donné par l'utilisateur
    contenu=f.read()                    #Stocke le contenu du fichier dans la variable contenu
    listing_ip_fich = contenu.split(carac)          #Transforme en liste en séparant par le caractère donné par l'utilisateur
    for i in range(len(listing_ip_fich)) :          #On parcours la liste
        if "\n" in listing_ip_fich[i] :             #Test si lors de la transformation, un retour à la ligne sous forme \n est apparu
            listing_ip_fich[i]=listing_ip_fich[i][0:-1]     #A ce moment on supprime ce retour à la ligne
    for i in listing_ip_fich:   #Connexion à chaque machine (IP) trouvée dans le fichier
        try :         #IDEM que les fonctions précédentes niveau connexion aux machines
            client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(0.05)
        except :
            print (Colors.NEGATIVE+"Création de la socket impossible pour "+str(i)+Colors.END)
        try :
            client_socket.connect((str(i), port))
            message_recu = client_socket.recv(1024).decode()
            if ch_fich.upper()=="OUI":
                nouv_fich.write("["+i+"] :"+message_recu+"\n")
            print (Colors.YELLOW+"["+Colors.END+str(i)+Colors.YELLOW+"]"+Colors.END+": "+message_recu) 
            client_socket.close()
        except :
            if aff_err.upper()=="OUI": 
                print(Colors.NEGATIVE+"Connexion à "+str(i)+" impossible"+Colors.END)
                print(sys.exc_info())
    f.close()
    if ch_fich.upper()=="OUI":
        nouv_fich.close()


    
fct_dict=[ip_liste,ip_local,ip_fichier,exit]            #Liste des fonctions séléctionnables dans le menu

while True :
    print(Colors.PURPLE+"""
--------------------------------------------
 __               __                 
/ _\_   _ ___    / _\ ___ __ _ _ __  
\ \| | | / __|   \ \ / __/ _` | '_ \ 
_\ \ |_| \__ \   _\ \ (_| (_| | | | |
\__/\__, |___/___\__/\___\__,_|_| |_|v1.1
    |___/ 
    """)
    print("--------------------------------------------"+Colors.END)
    print(Colors.CYAN+"""1"""+ Colors.END+""" > Scan d'adresses IP manuel
"""+Colors.CYAN+"""2"""+Colors.END+""" > Scan d'adresses IP sur le réseau (détection automatique des machines)
"""+Colors.CYAN+"""3"""+Colors.END+""" > Scan d'adresses IP depuis un fichier
"""+Colors.RED+"""4"""""" > Quitter X"""+Colors.END)
    ch=int(input(Colors.YELLOW+">> "+Colors.END))
    if ch!= 4:
        print(Colors.YELLOW+"Voulez sauvegarder les résultats du scan dans un "+Colors.BOLD+"fichier"+Colors.YELLOW+"?\nOui / Non"+Colors.END)
        ch_fich=input(Colors.YELLOW+">> "+Colors.END)
        if ch_fich.upper()=="OUI":
            print(Colors.GREEN+"Le fichier de log sera créé dans le dossier logs"+Colors.END)
            print(Colors.YELLOW+"-----------------------------")
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y-%H_%M_%S")
            nouv_fich=open("./logs/log-"+dt_string+".txt",'w')

    if ch in range(1,5):            #test si l'utilisateur séléctionne une fonction existante
        fct_dict[ch-1]()            #execute la fonction choisie
    else:
        print(Colors.RED+"** Choix non disponible, réssayez **"+Colors.END) #sinon le renvoie au menu
