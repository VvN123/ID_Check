'''Modulo de funciones para interacciones con FIREBASE. '''
import firebase_admin
import uuid
from firebase_admin import credentials
from firebase_admin import firestore
from modules.helper import generar_ruta, obtener_tiempo

def connect_to_fb(): 
    global app
    global db
    cred = credentials.Certificate(generar_ruta('firebase','credentials_fb.json'))
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()

def retrieve_pending():
    pending_list = []
    try:
        docs = db.collection(u'DATA').where(u'pending', u'==', True).stream()
        for doc in docs:
            data=doc
            pending_list.append(data.to_dict())
        return pending_list
    except:
        None

def upoload_to_fb(uuid: str, persona):
    db.collection(u'DATA').document(uuid).set(persona)

def retrieve_uuid(uuid: str): #  Para buscar por nombre documento
    doc_ref = db.collection(u'DATA').document(uuid)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        print(u'No such document!')


