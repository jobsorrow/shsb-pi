import firebase_admin
import threading
from firebase_admin import credentials
from firebase_admin import firestore
from platform import system


log = 1


if system()== 'Windows':
    cred = credentials.Certificate("C:\\Users\\61301765\\Documents\\shsb-pi\\fir-playaround-94ba4-firebase-adminsdk-fjx0x-2095afb103.json")
else :
    cred = credentials.Certificate("/home/pi/shsb-pi/fir-playaround-94ba4-firebase-adminsdk-fjx0x-2095afb103.json")
#from gpiozero import LED
project_id = 'fir-playaround-94ba4'

# Use the application default credentials

firebase_admin.initialize_app(cred, {'projectId': project_id,})

db = firestore.client()

def on_light(pin):
    if log:
        print('*  gpio  * turn light on pin: ', pin)

def off_light(pin):
    if log:
        print('*  gpio  * turn light off pin: ',pin)
        
def on_air(pin):
    if log:
        print('*  gpio  * turn air on devId: ', pin)

def off_air(pin):
    if log:
        print('*  gpio  * turn air off devId: ',pin)

def set_pwm(pin,val):
    if log:
        print('*  gpio  * set pwm on pin: ',pin,' of val: ',val)

def set_temp(id,val):
    if log:
        print('*  gpio  * set temp on pin: ',id,' of val: ',val)


# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot_callback(doc_snapshot, changes, read_time):
    for change in changes:
        if log:
            print(f'*firebase* change : {change.document.id}')

        #room,devtype,pin = change.document.id.strip().split('$')

        dev_dict = change.document.to_dict()
        if dev_dict['deviceType']=='light':
            if dev_dict['on']:
                on_light(dev_dict['deviceControlAt'])
                set_pwm(dev_dict['deviceControlAt'],dev_dict['brightness'])
            else :
                off_light(dev_dict['deviceControlAt'])
        elif dev_dict['deviceType']=='air':
            if dev_dict['on']:
                on_air(dev_dict['deviceId'])
                set_temp(dev_dict['deviceId'],dev_dict['temp'])
            else :
                off_air(dev_dict['deviceId'])
        
    callback_done.set()

dev = db.collection(u'devices')

# Watch the devices
dev_watch = dev.on_snapshot(on_snapshot_callback)

#led_pins = [17,27,22,23,5,6]

#led_obj = [LED(led_pin) for led_pin in led_pins ]

while 1:
        pass


