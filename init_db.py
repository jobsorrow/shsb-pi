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



