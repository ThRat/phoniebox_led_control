#!/usr/bin/python3

import signal
import sys
import os
import subprocess
from time import sleep

from gpiozero import PWMLED

LED_PREV = PWMLED(12)
LED_PLAY = PWMLED(27)
LED_NEXT = PWMLED(22)
LED_PWR = PWMLED(16)

#ALL_GPIO = [LED_PREV, LED_PLAY, LED_NEXT, LED_VOLUP, LED_VOLDOWN]

def sigterm_handler(*_):
    sleep(0.1)
    LED_PREV.off()
    LED_NEXT.off()
    LED_PREV.close()
    LED_NEXT.close()
    sleep(0.1)
    LED_PLAY.off()
    LED_PLAY.close()
#    for device in ALL_GPIO:
#        device.off()
#        device.close()
    sys.exit(0)


def getshell():
    process = subprocess.Popen("echo -e status\\nclose | nc -w 1 localhost 6600 | grep 'OK MPD'", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
    return process

def initiate_animation():
    process = ""
    pos = 1
    direction = 0
    while process == "":
        print(process)
        if pos == 1:
            LED_PLAY.pulse(n=1, fade_in_time=0.2, fade_out_time=0.8)
            sleep(0.2)
        elif pos == 2:
            LED_PREV.pulse(n=1, fade_in_time=0.2, fade_out_time=0.8)
            LED_NEXT.pulse(n=1, fade_in_time=0.2, fade_out_time=0.8)
            sleep(0.2)
        elif pos == 3:
            process = getshell()
            print(process)
            sleep(0.8)
            pos=0
        pos += 1
        sleep(0.04)


def leds_on():
    LED_PLAY.on()
    sleep(0.1)
    LED_PREV.on()
    LED_NEXT.on()
    sleep(0.1)
    LED_PWR.on()

def leds_off():
    LED_PLAY.off()
    LED_PREV.off()
    LED_NEXT.off()
    LED_PWR.off()
    sleep(0.1)

def main():
    dummy = ""
    while dummy == "":
        if(os.path.exists("/tmp/nightmode.led")):
            leds_off()
        else:
            leds_on()
        sleep(2)


if __name__ == "__main__":
    initiate_animation()
    leds_on()
    signal.signal(signal.SIGTERM, sigterm_handler)
    main()
