import firebase_admin
import threading
from firebase_admin import credentials
from firebase_admin import firestore

from gpiozero import LED
project_id = 'fir-playaround-94ba4'

# Use the application default credentials
cred = credentials.Certificate("/home/pi/shsb-pi/fir-playaround-94ba4-firebase-adminsdk-fjx0x-2095afb103.json")
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

db = firestore.client()


# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot_callback(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'update status : {doc.id} => {doc.to_dict()}')
    callback_done.set()

dev = db.collection(u'devices')

# Watch the devices
dev_watch = dev.on_snapshot(on_snapshot_callback)

#led_pins = [17,27,22,23,5,6]

#led_obj = [LED(led_pin) for led_pin in led_pins ]

while 1:
	pass
