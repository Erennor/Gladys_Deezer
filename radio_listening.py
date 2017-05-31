#!/usr/bin/env python
# coding: utf8

import subprocess
import json
import time
import sys
from pathlib import Path

def curl_cmd(url, jsonfile):
	cmd = "curl -s -o " + str(jsonfile) + " -X GET -H \"Authorization: Bearer " + access_token + "\" \\" + url
	return cmd


def get_radio_infos():
	radio_info_jsonfile = Path("/tmp/radio_infos.json")
	url = "https://api.orange.com/orangeradio/v1/selections/fr/radios"
	subprocess.call(["rm " + str(radio_info_jsonfile)], shell=True)
	subprocess.call([curl_cmd(url, radio_info_jsonfile)], shell=True)

    # Wait for the file to be created
	while not radio_info_jsonfile.exists():
		pass

	with open(str(radio_info_jsonfile)) as data_file:
		data = json.load(data_file)

	for i in range(0, len(data)):
		print data[i]["name"]

	return data


def get_stream(radio_name):
	radio_stream_jsonfile = Path("/tmp/radio_stream.json")

	# Correction des slug des radio
	if radio_name.lower() == "europe1":
		radio_name = "europe_1"

	if radio_name.lower() == "france bleu paris":
		radio_name = "france_bleu_1071"

	if radio_name.lower() == "fun radio":
		radio_name = "fun_radio_france"


	print radio_name.lower().replace(" ", "_")
	url = "https://api.orange.com/orangeradio/v1/radios/" + radio_name.lower().replace(" ", "_") + "/streams"
	subprocess.call(["rm " + str(radio_stream_jsonfile)], shell=True)
	subprocess.call([curl_cmd(url, radio_stream_jsonfile)], shell=True)
	# Wait for the file to be created
	while not radio_stream_jsonfile.exists():
		pass

	with open(str(radio_stream_jsonfile)) as data_file:
		data = json.load(data_file)

	# for i in range(0, len(data)):
	# 	print data[i]["url"]

	return data

def check_radio(radio_name):
	if radio_name.lower() in radio_names:
		return True
	else :
		print "ERREUR : la radio demandée n'est pas supportée."
		print "Les radios supportées sont les suivantes :"
		for i in range(0, len(radio_names)):
			print radio_names[i]
		return False


def main():

    if len(sys.argv) != 2:
    	print "ERREUR : 1 seul argument requis"
        return 1

    global radio_name
    radio_name = sys.argv[1]

    global radio_names
    radio_names = ["nrj", "rtl", "france inter", "europe1", "france info", "rmc", "france bleu paris", "skyrock", "fun radio", "nostalgie"]

    global access_token
    access_token = "oWAz08VJzJKCdoahBePpfD4zCzpx"

    if not check_radio(radio_name):
    	return 1

    stream = get_stream(radio_name)
    stream_url = stream[0]["url"]
    print stream_url

    subprocess.call(["mplayer " + stream_url + " &"], shell=True)

    return 0


if __name__ == "__main__":
    main()
