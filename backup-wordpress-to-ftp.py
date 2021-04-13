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
from sftpconfig import *
from mysqlconfig import *

# Arret du service apache

os.system("systemctl stop apache2.service")

# Execution du backup de la base de donnée wordpress et copie du backup wordpress.sql à la racine /root

os.system("clear")
command = "mysqldump -u " + mysqluser +" --password=" + mysqlpassword + " wordpress > /root/backupmysql.sql"
os.system(command)
os.system("clear")
print("Sauvegarde de la base de données Wordpress et du dossier /var/www/wordpress en cours, veuillez patienter.")

# Mise en variable du fichier /root/backupwordpress.tar.gz

file_name_wp = "/root/backupwordpress.tar.gz"

# Archivage du dossier /var/www/html/wordpress pour le backup wordpress

tar = tarfile.open(file_name_wp, "w:gz")
os.chdir("/var/www/wordpress")
for name in os.listdir("."):
        tar.add(name)
tar.close()

# Redemarrage du services apache

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

antislash = ('/')
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

# Suppression des fichiers de + de 4 semaines

transport = paramiko.Transport((host, port))
transport.connect(username = username, password = password)

sftp = paramiko.SFTPClient.from_transport(transport)

for entry in sftp.listdir_attr(remotepath):
    timestamp = entry.st_mtime
    createtime = datetime.datetime.fromtimestamp(timestamp)
    now = datetime.datetime.now()
    delta = now - createtime
    if delta > datetime.timedelta(minutes=43200):
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
