import subprocess
import os
os.system("clear")

print("\nSauvegarde et restauration d'un site Wordpress \n\n 1. Sauvegarde de wordpress sur le SFTP \n 2. Restauration de wordpress depuis le SFTP \n 3. Sortir du menu \n")
choice = input()

if choice =="1":
    print()
    print("Sauvegarde de Wordpress sur le SFTP\n")
    os.system("python3 backup-wordpress-to-ftp.py")
if choice =="2":
    print()
    print("Restauration de la sauvegarde Wordpress depuis le SFTP\n")
    os.system("python3 restore-wordpress-from-ftp.py")
if choice =="3":
    print()
    os.system("clear")
    exit()
while choice not in ["1","2","3","4"]:
     print ("La saisie n'est pas valide\n")
     break
