#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi

import os
import base64
import xml.etree.ElementTree
import time

# LCD SETTINGS -------------------------------------------------- #

import sys
sys.path.insert(0, "Adafruit_Python_CharLCD")
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration (for Model B)
lcd_rs        = 7
lcd_en        = 8
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# For some reason, my LCD backlight switch is backwards
off = 1
on = 0

# LOGGING ------------------------------------------------------- #
# Set up the logging, based on the command line arguments

import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', help='Log debug information to screen', action="store_true")
parser.add_argument('-f', '--file', help='Log debug information to file', action="store_true")
parser.add_argument('-q', '--quiet', help='No output to screen', action="store_true")
args = parser.parse_args()
if args.debug:
	loglevel = logging.DEBUG
elif args.quiet:
	loglevel = 60
else:
    loglevel = logging.INFO

# logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',filename='example.log',level=loglevel)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create console handler to show messages on screen
ch = logging.StreamHandler()
ch.setLevel(loglevel)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(levelname)s: %(message)s')
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
ch.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)


# create file handler which logs messages to file if user specifed it on the command line
if args.file:
    fh = logging.FileHandler('logger.log', 'w')
    fh.setLevel(loglevel)
    fh.setFormatter(file_formatter)
    logger.addHandler(fh)



# HELPER FUNCTIONS --------------------------------------------- #

# Some magic to decode ascii digits to string
def ascii_integers_to_string(string, base=16, digits_per_char=2):
	return "".join([chr(int(string[i:i+digits_per_char], base=base)) for i in range(0, len(string), digits_per_char)])

# helper function to add a single space pad to a string if it is over 20 chars long
# so that it looks better when marquee scrolling
def pad_string(string_to_pad):
	if len(string_to_pad) > 20:
		string_to_pad = string_to_pad + " "
		return string_to_pad
	else:
		return string_to_pad



# MAIN ---------------------------------------------------------- #

def main():
	# initialize the connection
	lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

	path = "/tmp/shairport-sync-metadata"
	fifo = open(path, "r")
	wholeelement = ""
	title = ""
	album = ""
	artist = ""
	info = ""
	updateflag = False

	with fifo as f:
		while True:
			line = f.readline()
			line = line.strip()
			logger.debug("Got " + line)
			wholeelement += line
			if line.endswith("</item>"):
				logger.debug("end of item")
				logger.debug("element = " + wholeelement)

				# Now that we've got a whole xml element, we can process it
				doc = xml.etree.ElementTree.fromstring(wholeelement)

				# get the type and convert to ascii
				type = doc.findtext('type')
				type = ascii_integers_to_string(type)
				# get the code and convert to ascii
				code = doc.findtext('code')
				code = ascii_integers_to_string(code)

				# get the data out, if there is any
				data = doc.findtext('data')
				if data != None:
					data = base64.b64decode(data)
				else:
					data = ""
				if type == "ssnc":
					#if code == "pfls":
						#title = ""
						#album = ""
						#artist = ""
						#updateflag = True

					if code == "pend":
						logger.info("Playback finished...")
						lcd.clear()
						title = ""
						album = ""
						artist = ""
						info = ""
						updateflag = True
						lcd.set_backlight(off)

					if code == "pbeg":
						lcd.set_backlight(on)
						logger.info("Playback started...")
						# device.lcd_clear()
					if code == "snua":
						logger.info("User agent received")
						info = data
						updateflag = True
					if code == "pvol":
						# set up the volume screen
# 						vol_screen = lcd.add_screen("Volume")
# 						vol_screen.set_heartbeat("off")
# 						vol_title = vol_screen.add_title_widget("vol_title", text = "Volume")
# 						vol_screen.set_priority("foreground")
# 						vol_screen.set_timeout(2)


						logger.info("volume information received")
				if type == "core":
					#process the codes that we're interested in
					if code == "assn":
						if ((title != data) and (data !="")):
							title = data
							updateflag = True
					if code == "minm":
						if ((title != data) and (data !="")):
							title = data
							updateflag = True
					if code == "asar":
						if artist != data:
							artist = data
							updateflag = True
					if code == "asal":
						if album != data:
							album = data
							updateflag = True
					if code == "asbr":
						logger.info("Bitrate:")
						logger.info(int("0x" + ''.join([hex(ord(x))[2:] for x in data]), base=16))


				if data != "":
					logger.info("Type: " + type + ", Code: " + code + ", Data: " + data)
				else:
					logger.info("Type: " + type + ", Code: " + code)

				wholeelement = ""
			if updateflag:
				logger.info("\nTitle: " + title + "\nArtist: " + artist + "\nAlbum: " + album)
				# update the lines with the new contents of the variables
				lcd.set_backlight(on)
				lcd.clear()
				lcd.message(pad_string(title) + "\n" + pad_string(artist))
				updateflag = False
	fifo.close()

if __name__ == "__main__":
	main()