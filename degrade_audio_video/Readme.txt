Pour lancer le script : sh degrade_audio-video.sh

Pour utiliser ce script il faut d'abord télécharger ffmpeg (https://ffmpeg.org/download.html)

Ce script permet de :
- dégrader les fichiers audio wav en mp3 (44khz)
- dégrader les fichier vidéo mp4 en 
	. mp4 (320x240) si 4/3
	. mp4 (320x180) si 16/9 (par défault)
Les résultats sont mis dans un répertoire nommé "output"


********

To run the script : sh degrade_audio-video.sh

To use this script you need to download ffmpeg (https://ffmpeg.org/download.html)

This script will:
- degrade a wav audio file to mp3 format (44khz)
- degrade an mp4 video audio to 
	. mp4 format (320x240) if 4/3
	. mp4 format (320x180) if 16/9 (by default)

The results are put in a directory called "output"