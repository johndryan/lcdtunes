# LCC Display of Shairport-Sync Metadata on Raspberry Pi

A fork of John Harris’s [lcdtunes](https://github.com/john-a-harris/lcdtunes) designed to show Airplay Metadata (from [Shairport](https://github.com/mikebrady/shairport-sync)) on an [LCD Display](https://www.sparkfun.com/products/9051) (one that utilizes the common ST7066/HD44780 parallel interface) attached to a Raspberry Pi. My fork uses the [Adafruit LCD library](https://github.com/adafruit/Adafruit_Python_CharLCD). 

## Installation

1. Install [shairport-sync](https://github.com/mikebrady/shairport-sync-metadata-reader) and enable metadata.
2. Clone this repo, and update submodules
3. Install [Adafruit LCD library](https://github.com/adafruit/Adafruit_Python_CharLCD):
	1. `sudo apt-get update`
	2. `sudo apt-get install build-essential python-dev python-smbus python-pip`
	3. `sudo pip install RPi.GPIO`
	4. `sudo python Adafruit_Python_CharLCD/setup.py install`
4. …

## LCD Wiring

This is the wiring for a **3.3V** LCD Display:

![Wiring diagram from Adafruit](https://cdn-learn.adafruit.com/assets/assets/000/018/260/medium800/raspberry_pi_RaspberryPiRGB_bb.png?1405984925)

## Requirements, etc.

To come…

## Todo

- [ ] Add scrolling for long titles
- [ ] Toggle backlight on-and-off after set period
- [ ] Finish README instructions/requirements/etc.
- [ ] Install as launch service
- [ ] Tidy dependencies and install process
- [ ] Add support for Spotify
- [ ] Redesign as API for other services to display information?