#!/usr/bin/env python

import os

os.system ("apt-get install python3-pip -y")
os.system ("pip3 install -r requirements.txt")
os.system ("clear")

import tarfile
import subprocess
import paramiko
from sftpconfig import *
from mysqlconfig import *

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
        print("Le fichier", backupmysql, "est présent sur le SFTP et a bien été téléchargé.")
    except IOError:
        print("Le fichier", backupmysql, "n'est pas présent sur le SFTP, la restauration est annulée.")
        print()
        os.system("rm -r /root/backup")
        exit()
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
        print("Le fichier", backupwordpress, "est présent sur le SFTP et a bien été téléchargé.")
    except IOError:
        print("Le fichier", backupwordpress, "n'est pas présent sur le SFTP, la restauration est annulée.")
        print()
        os.system("rm -r /root/backup")
        exit()
    ssh_client.close()
except paramiko.SSHException:
    print("Connection Error")
    exit()

# Arret du service apache

os.system("systemctl stop apache2.service")

# Decompression de l'archives backupwordpress dans /var/www/wordpress

tar = tarfile.open(localpathwordpress, "r:gz")
tar.extractall("/var/www/wordpress")
tar.close()

# restauration de la base de données wordpress dans MySQL

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
