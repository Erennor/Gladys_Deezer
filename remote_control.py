#!/usr/bin/env python
# coding: utf8

import json
import urllib2

global tv_host
with open("./config.json") as data_file:
	data = json.load(data_file)
tv_host = data["remote"]["host"]

global cmd_url
cmd_url = "http://" + tv_host + ":8080/remoteControl/cmd?operation=01"

def get_box_state():
	state_json = urllib2.urlopen("http://192.168.1.27:8080/remoteControl/cmd?operation=10").read()
	return state_json

def set_command(key, mode):
	urllib2.urlopen(cmd_url + "&key=" + str(key) + "&mode=" + str(mode)).read()

def on_off():
	set_command(116, 0)

def decodeur_on():
	state = get_box_state()
	state = json.loads(state)
	state = state["result"]["data"]["activeStandbyState"]
	if state == "1":
		# La TV est éteinte
		set_command(116, 0)

def decodeur_off():
	state = get_box_state()
	state = json.loads(state)
	state = state["result"]["data"]["activeStandbyState"]
	if state == "0":
		# La TV est allumée
		set_command(116, 0)

def ch_plus():
	set_command(402, 0)

def ch_moins():
	set_command(403, 0)

def mute():
	set_command(113, 0)

def volume_plus():
	set_command(115, 0)

def volume_moins():
	set_command(114, 0)

def menu():
	set_command(139, 0)

def back():
	set_command(158, 0)

def vod():
	set_command(393, 0)

def touche_num(num):
	num_length = len(str(num))
	# print num_length
	for i in str(num):
		# print i
		set_command(512 + int(i), 0)

# vod()

# urllib2.urlopen(cmd_url).read()

# numéro_mode :
# 0 : envoi unique de touche
# 1 : appui prolongé de touche
# 2 : relacher la touche après un appui prolongé

# code_touche :
# 116 : ON/OFF
# 512 : 0
# 513 : 1
# 514 : 2
# 515 : 3
# 516 : 4
# 517 : 5
# 518 : 6
# 519 : 7
# 520 : 8
# 521 : 9
# 402 : CH+
# 403 : CH-
# 115 : VOL+
# 114 : VOL-
# 113 : MUTE
# 103 : UP
# 108 : DOWN
# 105 : LEFT
# 116 : RIGHT
# 352 : OK
# 158 : BACK
# 139 : MENU
# 164 : PLAY/PAUSE
# 168 : FBWD
# 159 : FFWD
# 167 : REC
# 393 : VOD