# hvac-telegram-bot

## My Hardware

 * Raspberry Pi Model B. (old one)
 * HVAC IR Remote for arduino / Raspberry Pi
   * https://www.cooking-hacks.com/hvac-ir-remote-shield-for-raspberry-pi
   * https://www.cooking-hacks.com/documentation/tutorials/control-hvac-infrared-devices-from-the-internet-with-ir-remote/

## Setting up HVAC IR Remote for LIRC

 * Instructions

> https://www.hackster.io/austin-stanton/creating-a-raspberry-pi-universal-remote-with-lirc-2fd581

 * Install lirc package

```
sudo apt-get install lirc
```

 * Configure kernel module

```
vi /etc/modules
lirc_dev
lirc_rpi gpio_in_pin=18 gpio_out_pin=23
```
> note I/O port is different than above documentation.
> You can find GPIO port for HVAC IR Remote in arduPi.cpp

```
vi /etc/lirc/hardware.conf
```
> see above document

```
vi /etc/lirc/lirc_options.conf
```
> https://raspberrypi.stackexchange.com/questions/50873/lirc-wont-transmit-irsend-hardware-does-not-support-sending
> set driver to 'default'

 * Record IR signal or obtain configuration file.
> http://lirc.sourceforge.net/remotes/

> My testing board didn't work as expected.
> I can only control IR LED, two buttons, two indication LEDs. but can't read IR signal. I don't know board is broken or something.

## Preparations

following my own blog https://www.dgkim.net/wordpress/2017/08/24/telegram-bot-%ed%85%8c%ec%8a%a4%ed%8a%b8-%eb%85%b8%ed%8a%b8/

### python-telegram-bot
> I tried 
```
git clone https://github.com/python-telegram-bot/python-telegram-bot

cd python-telegram-bot
git submodule update
```

> But, today I changed plan.
> https://pypi.org/project/python-telegram-bot/

## programming part

> I referenced https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples

> quickly created firstbot.py

