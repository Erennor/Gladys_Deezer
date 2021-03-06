#!/usr/bin/env python
# coding: utf8

import subprocess
import json
import urllib2
import Queue
import threading
import sys
import ctypes
import time
from myDeezerApp import *
from text_recognition import *

global project_location
global gladys_location

project_location = "."

# A MODIFIER
gladys_location = "/usr/lib/node_modules/gladys"

global logfile
global jsonfile
logfile = '/tmp/gladys.log'
jsonfile = '/tmp/gladys.json'

# token de test
global access_token
access_token = "oWAz08VJzJKCdoahBePpfD4zCzpx"


def launch_server():
	# Lancement du serveur nodejs
	subprocess.call(project_location + "/start_gladys.sh " + gladys_location, shell=True)

def get_json_line(lines):
	# On recupere la ligne du JSON en detectant la ligne
	# commencant par "[{\"message\""
	for line in lines:
		if line[:11] == "[{\"message\"":
			return line
	return "null"

def read_line():
	# On va lire le fichier temporaire cree contenant le JSON
	# et on recupere le champ "text"
	lines = open(logfile).readlines()
	lines = [x.strip() for x in lines]
	line = get_json_line(lines)
	if line != "null":

		# On ecrit dans le json
		open(jsonfile, 'w').write(line)

		# Parsing du JSON
		with open(jsonfile) as data_file:
			data = json.load(data_file)

		text = data[0]["message"]["text"]
		print(text)
		open(logfile, 'w').write("break\n")	
		return text
	return "null text"

def add_input(input_queue):
    while True:
    	user_input = read_line()
        if user_input == "pause" or user_input == "play":
        	input_queue.put("P\n")
        if user_input == "start" or user_input == "stop":
        	input_queue.put("S\n")
        if user_input == "quitter" or user_input == "arrête la musique" or user_input == "coupe la musique" or user_input == "éteins la musique":
        	input_queue.put("Q\n")
        	break
        if user_input == "suivant" or user_input == "musique suivante":
        	input_queue.put("+\n")
        if user_input == "précédent" or user_input == "musique précédente":
        	input_queue.put("-\n")
        if user_input[:17] == "mets le volume a " or user_input[:17] == "mets le volume à ":
        	value = user_input[17:]
        	# Correction lors de la lecture des valeurs
        	if value == "zéro":
        		value = 0
        	elif value == "deux":
        		value = 2
        	else:
        		value = int(user_input[17:])
        	volume = 10 * value
        	subprocess.call( project_location + "/set_volume.sh " + str(volume) + "%", shell=True)

def process_input(app):
    input_queue = Queue.Queue()
    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()
    while app.connection.active or app.player.active:
        if not input_queue.empty():
            command = input_queue.get()
            if len(command) != 2 or command[0] not in "PSQ+-?R":
                print ("INVALID COMMAND")
                log_command_info()
            else:
                app.process_command(command)

def play_music(track):
	app = MyDeezerApp(True)
	app.set_content(track)
	process_input(app)
	print "FIN DE LA MUSIQUE"
	return 0

def play_radio(radio_name):
	subprocess.call("python " + project_location + "/radio_listening.py \"" + radio_name + "\"", shell=True)
	return 0

def main():
	reload(sys)  # Reload does the trick!
	sys.setdefaultencoding('UTF8')
	if len(sys.argv) != 1:
		print "ERROR : No arguments required"
		return 1

	# Lancement du serveur gladys nodejs
	launch_server()

	while True:
		text = read_line()
		track = text_recognition(text)

		# Jouer la musqiue sur Deezer
		if track[:7] == "dzmedia":
			play_music(track)

		# Jouer la radio
		elif track[:5] == "radio":
			play_radio(track[5:])

	return 0

if __name__ == "__main__":
    main()
