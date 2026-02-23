# Follow Format
About:

Forensic challenge
Level: Easy
Subject:

Our client sent us this image and told us that they deleted a file. Please help them recover it. The file contains confidential information. Flag format: CCOI26{S0mething_here} https://cdn.cattheflag.org/cybercup/challenge1/challenge.img

# Writeups
On reçoit un fichier challenge.img de 100 Mo. La commande file confirme qu'il s'agit d'un système de fichiers ext4 Linux nommé WORK_DRIVE.
Mon premier réflexe face à une image disque : lancer strings pour voir si quelque chose n'est pas simplement lisible en clair dans les données brutes — avant même de monter le volume ou de sortir un outil de récupération. Et ça a payé.

```powershell
┌──(raph㉿RAPH-PORTABLE)-[F:\PROJET\COMPETITIONS\CYBERSECURITE\CYBERCUP\Etape 2\forensics\follow format]
└─# file .\challenge.img
.\challenge.img: Linux rev 1.0 ext4 filesystem data, UUID=ae6148e4-8e10-49db-a77b-9c52b2529b02, volume name "WORK_DRIVE" (extents) (64bit) (large files) (huge files)
┌──(raph㉿RAPH-PORTABLE)-[F:\PROJET\COMPETITIONS\CYBERSECURITE\CYBERCUP\Etape 2\forensics\follow format]
└─# strings .\challenge.img | findstr CCOI
CCOI26{iNod3_n3v3r_f0rg3ts_2026}
┌──(raph㉿RAPH-PORTABLE)-[F:\PROJET\COMPETITIONS\CYBERSECURITE\CYBERCUP\Etape 2\forensics\follow format]
└─# 
```
Le flag apparaît directement dans la sortie, encore présent dans les blocs de l'inode malgré la suppression du fichier.

```
CCOI26{iNod3_n3v3r_f0rg3ts_2026}
```