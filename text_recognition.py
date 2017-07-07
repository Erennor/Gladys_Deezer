#!/usr/bin/env python
# coding: utf8

import subprocess
import json
import urllib2
import time
# from remote_control import *

def get_value_from_text(text):
	# Correction lors de la lecture des valeurs
	if text == "zéro":
		text = 0
	elif text == "deux":
		text = 2
	else:
		text = int(text)

	return text

def text_recognition(text):
	
	# Jouer un artiste
	if text[:8] == "joue du ":
		artist = text[8:].replace(" ", "+")
		track = urllib2.urlopen("https://api.deezer.com/search?q=" + artist).read()
		track = json.loads(track)
		print(track["data"][0]["album"]["title"])
		# play_music("dzmedia:///album/" + str(track["data"][0]["album"]["id"]))
		return "dzmedia:///album/" + str(track["data"][0]["album"]["id"])

	# Jouer un album
	if text[:13] == "joue l'album ":
		album = text[13:].replace(" ", "+")
		track = urllib2.urlopen("https://api.deezer.com/search?q=" + album).read()
		track = json.loads(track)
		print(track["data"][0]["album"]["title"])
		# play_music("dzmedia:///album/" + str(track["data"][0]["album"]["id"]))
		return "dzmedia:///album/" + str(track["data"][0]["album"]["id"])

	# Jouer une musique
	if text[:16] == "joue la musique ":
		music = text[16:].replace(" ", "+")
		track = urllib2.urlopen("https://api.deezer.com/search?q=" + music).read()
		track = json.loads(track)
		print(track)
		# play_music("dzmedia:///track/" + str(track["data"][0]["id"]))
		return "dzmedia:///track/" + str(track["data"][0]["id"])

	# Jouer la radio
	if text[:5] == "joue " and text[len(text) - 17:] == " sur Orange radio":
		radio_name = text[5:len(text) - 17]
		print "\"" + radio_name + "\""
		return "radio" + radio_name
		# play_radio(radio_name)

	# Couper la radio
	if text == "coupe la radio" or text == "arrête la radio" or text == "coupe la musique" or text == "éteins la radio":
		subprocess.call(["killall mplayer"], shell=True)
		return "null_command"

	# Configurer le volume
	if text[:17] == "mets le volume a " or text[:17] == "mets le volume à ":
		value = text[17:]
		# Correction lors de la lecture des valeurs
		if value == "zéro":
			value = 0
		elif value == "deux":
			value = 2
		else:
			value = int(text[17:])
		volume = 10 * value
		subprocess.call( "./set_volume.sh " + str(volume) + "%", shell=True)
		return "null_command"

	## COMMANDES RELATIVES A LA TV ##

	# Allumer la TV
	if text == "allume la tv":
		decodeur_on()
		# Cette boucle sert à fermer le menu à l'allumage de la TV
		# afin d'afficher directement la chaine
		while True:
			state = get_box_state()
			state = json.loads(state)
			context = state["result"]["data"]["osdContext"]
			if context == "HOMEPAGE":
				key_menu()
				break
		return "null_command"

	# Eteindre la TV
	if text == "éteins la tv" or text == "coupe la tv":
		decodeur_off()
		return "null_command"

	# Mettre une chaine
	if text[:8] == "mets la ":
		num = get_value_from_text(text[8:])
		key_menu()
		key_num(num)
		key_ok()
		return "null_command"
	# Correction du au probleme de reconnaissance vocale
	if text[:7] == "mail à ":
		num = get_value_from_text(text[7:])
		key_menu()
		key_num(num)
		key_ok()
		return "null_command"

	# Recherche de films sur la vod
	if text[:10] == "recherche " and text[len(text) - 10:] == " sur la TV":
		film_name = text[10:len(text) - 10]
		vod_recherche_directe(film_name)

	# Zapper sur une chaine
	if text[:10] == "zappe sur ":
		response = get_response(text)
		response = json.loads(response)
		epgid = response["result"]["epgId"]
		print epgid
		zapping(epgid, 1)

	return "null_command"

