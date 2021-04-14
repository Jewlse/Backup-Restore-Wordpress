# Backup-Restore-Wordpress

Ce Script python permet de restaurer/sauvegarder en intégralité un site Wordpress depuis/vers un SFTP. 

## Pour commencer

WordPress est un logiciel destiné à la conception et à la mise à jour dynamique de sites web ou d'applications multimédias. L'objectif de ce script est de pouvoir sauvegarder et restaurer un site wordpress complet en un minimum de temps.

### Pré-requis

Le script ne peut être exécuté que sur un système disposant d'un serveur LAMP (Linux, Apache, MySQL, PHP) et d'une installation Wordpress.

Environnement lors de la fabrication du script :

- Ubuntu Server 20.04
- Apache 2
- MySQL 8.0.23
- PHP 7.4.3
- Wordpress 5.7
- Python 3.8.5

### Installation et configuration

1) Installer le paquet python3 sur votre système d'exploitation linux si celui-ce ne le possède pas déjà. 
Sur Ubuntu Server 20.04, saisir la commande suivante dans un terminal "sudo apt-get update && apt-get upgrade && apt-get install python3 -y".
2) Installer le gestionnaire de paquet python pip.
Sur Ubuntu Server 20.04, saisir la commande suivante dans un terminal "sudo apt-get install python3-pip -y"
3) Télécharger le contenu du dépôt https://github.com/Jewlse/Backup-Restore-Wordpress dans un dossier en local sur votre machine.
4) Installer les modules python3 listés dans le fichier requirements.txt, ils sont indispensables à la bonne exécution du scrit.
Sur Ubuntu Server 20.04, saisir la commande suivante dans une terminal "sudo pip3 install -r requirements.txt". Cette commande doit être exécutée dans le dossier contenant le fichier requirements.txt.
5) Ouvrir le fichier myconfiguration.py avec un editeur de texte et saisir les informations propres à votre installation à la place des XXXXXXXXXXX.

## Démarrage

Lancer le script avec la commande "sudo backup-restore-wordpress.py" dans un terminal qui pointe vers le dossier dans lequel se trouve le contenu du dépôt https://github.com/Jewlse/Backup-Restore-Wordpress

## Auteurs
* **Julien Dirr** _alias_ [@Jewlse](https://github.com/Jewlse)

## License

Ce projet est sous licence MIT - voir le fichier [LICENSE](https://github.com/Jewlse/Backup-Restore-Wordpress/blob/main/LICENSE) pour plus d'informations



