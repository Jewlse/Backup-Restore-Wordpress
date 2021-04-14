#!/usr/bin/env python

import os

os.system ("apt-get install python3-pip -y")
os.system ("pip3 install -r requirements.txt")
os.system ("clear")

import tarfile
import subprocess
import datetime
import time
import paramiko
from myconfiguration import *

### Fonction de sauvegarde de wordpress vers le SFTP

def backupwordpresstosftp():

    # Arret du service apache

    os.system("systemctl stop apache2.service")

    # Execution du backup de la base de données wordpress et copie du backup à la racine /root

    os.system("clear")
    command = "mysqldump -u " + mysqluser +" --password=" + mysqlpassword + " wordpress > /root/backupmysql.sql"
    os.system(command)
    os.system("clear")
    print("Sauvegarde de la base de données Wordpress et du dossier " + wordpresslocalpath + " en cours, veuillez patienter.")

    # Mise en variable du fichier /root/backupwordpress.tar.gz

    file_name_wp = "/root/backupwordpress.tar.gz"

    # Archivage du dossier wordpress pour le backup wordpress

    tar = tarfile.open(file_name_wp, "w:gz")
    os.chdir(wordpresslocalpath)
    for name in os.listdir("."):
        tar.add(name)
    tar.close()

    # Redemarrage du service apache

    os.system("systemctl start apache2.service")

    # Connection ssh_client

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password, port=port)

    # Depot des fichiers backupmysql et backupwordpress sur le SFTP avec renommage à la date du jour

    datestamp = datetime.datetime.now()
    antislash = ('/')
    backupmysql = 'backupmysql.sql'
    backupwordpress = 'backupwordpress.tar.gz'
    backupmysqlwithdate = "backupmysql.sql."+(datestamp.strftime("%d%m%y"))
    backupwordpresswithdate = "backupwordpress.tar.gz."+(datestamp.strftime("%d%m%y"))
    backupmysqlwithdate_path = remotepath + antislash + backupmysql + '.'  + (datestamp.strftime("%d%m%y"))
    backupwordpresswithdate_path = remotepath + antislash + backupwordpress + '.'  + (datestamp.strftime("%d%m%y"))
    remote_backupmysql = remotepath + antislash + backupmysql
    remote_backupwordpress = remotepath + antislash + backupwordpress

    ftp_client = ssh_client.open_sftp()
    print()
    print("Chargement du fichier", backupmysqlwithdate,"sur le SFTP.")
    ftp_client.put('/root/backupmysql.sql', backupmysqlwithdate_path)
    print()
    print("Chargement du fichier", backupwordpresswithdate,"sur le SFTP.")
    ftp_client.put('/root/backupwordpress.tar.gz', backupwordpresswithdate_path)
    ftp_client.close()

    # Suppression des fichiers qui ont dépassé la durée de stockage renseignée dans le fichier myconfiguration

    transport = paramiko.Transport((host, port))
    transport.connect(username = username, password = password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    for entry in sftp.listdir_attr(remotepath):
        timestamp = entry.st_mtime
        createtime = datetime.datetime.fromtimestamp(timestamp)
        now = datetime.datetime.now()
        delta = now - createtime
        if delta > datetime.timedelta(minutes=storageduration):
            filepath = remotepath + '/' + entry.filename
            sftp.remove(filepath)
    sftp.close()
    transport.close()

    # Suppression des fichiers backupmysql.tar.gz et backupwordpress.tar.gz dans /root local

    os.system("rm /root/backupmysql.sql")
    os.system("rm /root/backupwordpress.tar.gz")
    os.system("clear")

    # Confirmation de la bonne exécution de la sauvegarde

    print()
    print("La sauvegarde de Wordpress sur le SFTP s'est bien déroulée.")
    print()

### Fonction de restauration de wordpress depuis le SFTP

def restorewordpressfromsftp():

    # Connection ssh_client

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password, port=port)

    # Liste les fichiers dans le dossier backupwebsite et les affiches

    sftp = ssh_client.open_sftp()
    files = sftp.listdir(remotepath)
    os.system("clear")
    print ("Voici la liste des backupwordpress et backupmysql actuellement disponibles sur le SFTP:")
    print ()
    print (files)
    print ()
    ssh_client.close()

    # Choix et telechargements des backupwordpress et backupmysql du SFTP vers le répertoire local /root

    backupmysql = (input("Saisir le nom du fichier backupmysql à restaurer : "))
    backupwordpress = (input("Saisir le nom du fichier backupwordpress à restaurer : "))
    print()
    print("Téléchargement des fichiers en cours, veuillez patienter.")
    print()
    antislash = ('/')
    remote_backupmysql = remotepath + antislash + backupmysql
    remote_backupwordpress = remotepath + antislash + backupwordpress

    os.system("mkdir /root/backup")
    localpathmysql = "/root/backup/mysql.sql"
    localpathwordpress = "/root/backup/wordpress.tar.gz"

    try:
        ssh_client.connect(hostname=host, username=username, password=password, port=port)
        sftp = ssh_client.open_sftp()
        sftp.chdir(remotepath)
        try:
            print(sftp.stat(remote_backupmysql))
            sftp.get(remote_backupmysql,localpathmysql)
            print("Le fichier", backupmysql, "est présent sur le SFTP et a bien été restauré.")
        except IOError:
            os.system("clear")
            print()
            print("Le fichier", backupmysql, "n'est pas présent sur le SFTP, la restauration est annulée.")
            print()
            os.system("rm -r /root/backup")
            menu()
        ssh_client.close()
    except paramiko.SSHException:
        print("Connection Error")
        exit()

    try:
        ssh_client.connect(hostname=host, username=username, password=password, port=port)
        sftp = ssh_client.open_sftp()
        sftp.chdir(remotepath)
        try:
            print(sftp.stat(remote_backupwordpress))
            sftp.get(remote_backupwordpress,localpathwordpress)
            print("Le fichier", backupwordpress, "est présent sur le SFTP et a bien été restauré.")
        except IOError:
            print()
            os.system("clear")
            print("Le fichier", backupwordpress, "n'est pas présent sur le SFTP, la restauration est annulée.")
            print()
            os.system("rm -r /root/backup")
            menu()
        ssh_client.close()
    except paramiko.SSHException:
        print("Connection Error")
        exit()

    # Arret du service apache

    os.system("systemctl stop apache2.service")

    # Decompression de l'archive backupwordpress vers le dossier local wordpress

    tar = tarfile.open(localpathwordpress, "r:gz")
    tar.extractall(wordpresslocalpath)
    tar.close()

    # Restauration de la base de données wordpress dans MySQL

    os.system("clear")
    command = "mysql -u " + mysqluser +" --password=" + mysqlpassword + " --database=wordpress < /root/backup/mysql.sql"
    os.system(command)
    print("La restauration de la base de données Wordpress est en cours, veuillez patienter.")
    os.system("clear")

    # Demarrage du service apache

    os.system("systemctl start apache2.service")

    # Suppression des fichiers backupmysql.sql et backupwordpess.tar.gz dans /root local 

    os.system("rm -r /root/backup")
    os.system("clear")

    # Confirmation de la bonne exécution de la restauration

    print()
    print("La restauration de Wordpress depuis le SFTP s'est bien déroulée.")
    print()

### Fonction sortie du programme

def exitmenu():
    exit()

### Fonction affichage du menu

def menu():

    # Affichage du menu

    print("\nSauvegarde et restauration d'un site Wordpress \n\n 1. Sauvegarde de wordpress sur le SFTP \n 2. Restauration de wordpress depuis le SFTP \n 3. Sortir du menu \n")
    choice = input()

    if choice =="1":
        print()
        print("Sauvegarde de Wordpress sur le SFTP\n")
        backupwordpresstosftp()
        menu()
    if choice =="2":
        print()
        print("Restauration de la sauvegarde Wordpress depuis le SFTP\n")
        restorewordpressfromsftp()
        menu()
    if choice =="3":
        print()
        os.system("clear")
        exitmenu()
    while choice not in ["1","2","3","4"]:
        print ("La saisie n'est pas valide\n")
        break
menu()
