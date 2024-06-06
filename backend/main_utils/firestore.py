from .singleton import SingletonMeta
from firebase_admin import firestore

class Firestore(metaclass=SingletonMeta):
    client = firestore.client()

    