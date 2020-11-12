import code

import time

from gpiozero import PWMLED, Buzzer, LightSensor

import threading

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Adafruit_DHT

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


log = 1

RST = None

cred = credentials.Certificate("/home/pi/shsb-pi/fir-playaround-94ba4-firebase-adminsdk-fjx0x-2095afb103.json")

project_id = 'fir-playaround-94ba4'

firebase_admin.initialize_app(cred, {'projectId': project_id,})

db = firestore.client()


disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)


disp.begin()

bulb = dict()

bz = Buzzer(14)
ldr = LightSensor(18)

def init():
    for dev in devs.get():
        dev_dict = dev.to_dict()
        if dev_dict['deviceType'] == "light":
            bulb[dev_dict['deviceControlAt']]=(PWMLED(dev_dict['deviceControlAt'],active_high=False))

    ldr.when_dark = darkTurnOn
    ldr.when_light = darkTurnOff

    
def on_light(pin):
    if log:
        print('*  gpio  * turn light on pin: ', pin)
    bulb[pin].on()

def off_light(pin):
    if log:
        print('*  gpio  * turn light off pin: ',pin)
    bulb[pin].off()

def on_air(pin):
    if log:
        print('*  gpio  * turn air on devId: ', pin)

def off_air(pin):
    if log:
        print('*  gpio  * turn air off devId: ',pin)

def set_pwm(pin,val):
    if log:
        print('*  gpio  * set pwm on pin: ',pin,' of val: ',val)
        if(val>100):
            print("*  gpio  * setPwmFail: brightness exceeds 100")
    if val <= 100:    
        bulb[pin].value = val/100

def set_temp(id,val,stat):
    if log:
        print('*  gpio  * set temp on pin: ',id,' of val: ',val)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((0,0),'devId: {}'.format(id), font=font, fill=255)
    draw.text((0,fontsize+2),'temp: {}'.format(val), font=font, fill=255)
    draw.text((0,2*fontsize+4),'on: {}'.format(stat),font=font, fill=255)
    disp.image(image)
    disp.display()
    bz.blink(n=1,on_time=0.05)

def darkTurnOn():
    if log:
        print('*  gpio  * light sensor detect darkness')
    for doc in devs.where('darkTurnOn','==',True).get():
        devs.document(doc.id).update({'on': True})
def darkTurnOff():
    if log:
        print('*  gpio  * light sensor detect light')
    for doc in devs.where('darkTurnOn','==',True).get():
            devs.document(doc.id).update({'on': False})

def pollHumiditySensor():
    while (1):
        if sampleRate['humidity']:
            starttime = time.time()
            humidity,temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,4)
            sensors.document('humidSensor').update({'humidity':humidity,'temp':temp})
            print('*  gpio  * sampled for humid = {} and temp = {}'.format(humidity,temp))
            try:
                if (1/sampleRate['humidity']-(time.time()-starttime)) > 0:
                    time.sleep(1/sampleRate['humidity']-(time.time()-starttime))
            except ZeroDivisionError:
                pass

def pollLightSensor():
    while (1):
        if sampleRate['light']:
            starttime  = time.time()
            print('*  gpio  * sampled for light, intensity = {}'.format(ldr.value))            
            sensors.document('lightSensor').update({'intensity':ldr.value})
            try:
                if (1/sampleRate['light']-(time.time()-starttime)) > 0:
                    time.sleep(1/sampleRate['light']-(time.time()-starttime))
            except ZeroDivisionError:
                pass
fontsize = 20
font = ImageFont.truetype('/home/pi/shsb-pi/arial.ttf',fontsize)

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot_callback(doc_snapshot, changes, read_time):
    try :
        for change in changes:
            if log:
                print(f'*firebase* change in devs : {change.document.id}')

            #room,devtype,pin = change.document.id.strip().split('$')

            dev_dict = change.document.to_dict()
            if 'deviceType' in dev_dict:    
                if dev_dict['deviceType']=='light':
                    if dev_dict['on']:
                        on_light(dev_dict['deviceControlAt'])
                        set_pwm(dev_dict['deviceControlAt'],dev_dict['brightness'])
                    else :
                        off_light(dev_dict['deviceControlAt'])
                elif dev_dict['deviceType']=='air':
                    if dev_dict['on']:
                        on_air(dev_dict['deviceId'])
                    else :
                        off_air(dev_dict['deviceId'])
                    set_temp(dev_dict['deviceId'],dev_dict['temp'],dev_dict['on'])
                
        callback_done.set()
    except Exception as e:
        print('*  Errr  *',e)

def on_snapshot_sensors_callback(doc_snapshot,changes,read_time):
    for change in changes:
        if log:
            print('*firebase* change in sensors: {}'.format(change.document.id))
        if 'sampleRate' in change.document.to_dict():
            if 'humidSensor' == change.document.id:
                sampleRate['humidity'] = change.document.to_dict()['sampleRate']
            elif 'lightSensor' == change.document.id:
                sampleRate['light'] = change.document.to_dict()['sampleRate']

devs = db.collection(u'devices')
sensors = db.collection('sensors')


init()

sampleRate = {'humidity':0,'light':0}

# Watch the devices
devs_watch = devs.on_snapshot(on_snapshot_callback)
sensors_watch = sensors.on_snapshot(on_snapshot_sensors_callback)


humiditySensorThread = threading.Thread(target=pollHumiditySensor)
humiditySensorThread.start()

lightSensorThread = threading.Thread(target = pollLightSensor)
lightSensorThread.start()

#code.interact(local=locals())

while 1:
        pass


