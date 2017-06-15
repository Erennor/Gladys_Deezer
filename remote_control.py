#!/usr/bin/env python
# coding: utf8

import json
import urllib2
import time
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
if len(sys.argv) != 1:
	print "ERROR : No arguments required"

with open("./config.json") as data_file:
	data = json.load(data_file)
TV_HOST = data["remote"]["host"]

CMD_URL = "http://" + TV_HOST + ":8080/remoteControl/cmd?operation="

def get_box_state():
	state_json = urllib2.urlopen(CMD_URL + "10").read()
	return state_json

def press_key(key, mode):
	operation_num = "01"
	urllib2.urlopen(CMD_URL + operation_num + "&key=" + str(key) + "&mode=" + str(mode)).read()

def decodeur_on_off():
	press_key(116, 0)

def decodeur_on():
	state = get_box_state()
	state = json.loads(state)
	state = state["result"]["data"]["activeStandbyState"]
	if state == "1":
		# La TV est éteinte
		press_key(116, 0)

def decodeur_off():
	state = get_box_state()
	state = json.loads(state)
	state = state["result"]["data"]["activeStandbyState"]
	if state == "0":
		# La TV est allumée
		press_key(116, 0)

def key_ch_plus():
	press_key(402, 0)

def key_ch_moins():
	press_key(403, 0)

def key_mute():
	press_key(113, 0)

def key_volume_plus():
	press_key(115, 0)

def key_volume_moins():
	press_key(114, 0)

def key_up():
	press_key(103, 0)

def key_down():
	press_key(108, 0)

def key_left():
	press_key(105, 0)

def key_right():
	press_key(106, 0)

def key_ok():
	press_key(352, 0)

def key_menu():
	press_key(139, 0)

def key_back():
	press_key(158, 0)

def key_vod():
	press_key(393, 0)

def key_num(num):
	num_length = len(str(num))
	# print num_length
	for i in str(num):
		# print i
		press_key(512 + int(i), 0)

def key_letter(letter):
	accenta = "aâäà"
	accente = "eéèêë"
	accenti = "iîï"
	accentu = "uùüû"
	accento = "oôö"
	# print letter
	if len(letter) > 1:
		print "ERROR"
		return 1
	if letter in accenta:
		key_num(2)
	if letter == 'b':
		key_num(22)
	if letter == 'c':
		key_num(222)
	if letter == 'd':
		key_num(3)
	if letter in accente:
		key_num(33)
	if letter == 'f':
		key_num(333)
	if letter == 'g':
		key_num(4)
	if letter == 'h':
		key_num(44)
	if letter in accenti:
		key_num(444)
	if letter == 'j':
		key_num(5)
	if letter == 'k':
		key_num(55)
	if letter == 'l':
		key_num(555)
	if letter == 'm':
		key_num(6)
	if letter == 'n':
		key_num(66)
	if letter in accento:
		key_num(666)
	if letter == 'p':
		key_num(7)
	if letter == 'q':
		key_num(77)
	if letter == 'r':
		key_num(777)
	if letter == 's':
		key_num(7777)
	if letter == 't':
		key_num(8)
	if letter in accentu:
		key_num(88)
	if letter == 'v':
		key_num(888)
	if letter == 'w':
		key_num(9)
	if letter == 'x':
		key_num(99)
	if letter == 'y':
		key_num(999)
	if letter == 'z':
		key_num(9999)
	if letter == ' ':
		key_num(0)
		key_num(0)
	key_ok()

def key_word(word):
	for c in word.decode('utf8'):
		key_letter(c)

def zapping(epg_id, uui):
	urllib2.urlopen("http://192.168.1.27:8080/remoteControl/cmd?operation=09&epg_id=*******192&uui=1").read()

# Affiche les films à l'affiche dans la vod
def vod_films_a_l_affiche():
	key_vod()
	key_down()
	key_ok()

# Affiche la recherche dans la vod
def vod_recherche():
	key_vod()
	time.sleep(0.2)
	key_up()
	key_ok()

# Lance la recherche du mot word dans la vod
def vod_recherche_directe(word):
	vod_recherche()
	key_word(word)

# vod_recherche_directe("le prénom")

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
# 106 : RIGHT
# 352 : OK
# 158 : BACK
# 139 : MENU
# 164 : PLAY/PAUSE
# 168 : FBWD
# 159 : FFWD
# 167 : REC
# 393 : VOD