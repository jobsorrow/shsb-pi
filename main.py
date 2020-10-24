import firebase_admin
import threading
from firebase_admin import credentials
from firebase_admin import firestore

from gpiozero import LED
project_id = 'fir-playaround-94ba4'

# Use the application default credentials
cred = credentials.Certificate('/home/pi/firebase-playaround-365c54f5905a.json')
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

db = firestore.client()


# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_write(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'update status : {doc.id} => {doc.to_dict()}')
        appl_stats = doc.to_dict()['appl_status']
        for appl_stat_idx in range(len(appl_stats)):
            if appl_stats[appl_stat_idx] == '0':
                led_obj[appl_stat_idx].off()
            elif appl_stats[appl_stat_idx] == '1':
                led_obj[appl_stat_idx].on()
            else:
                print('error: invalid appl state')
    callback_done.set()

doc_ref = db.collection(u'users').document(u'jobs_home')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_write)

led_pins = [17,27,22,23,5,6]

led_obj = [LED(led_pin) for led_pin in led_pins ]

while 1:
	pass
