import datetime
from google.cloud.firestore import CollectionReference
from django.core.exceptions import ObjectDoesNotExist
#from rest_framework.authentication import TokenAuthentication
from rest_framework import authentication
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from rest_framework import exceptions
from firebase_admin import db

class BaseModel():
    id = None
    created = datetime.datetime.now()

    @staticmethod
    def from_dict(source, id, create_time):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

    @staticmethod
    def collection() -> CollectionReference:
        raise NotImplementedError

    @classmethod
    def all(cls):
        return [cls.from_dict(doc.to_dict(), doc.id, doc.create_time) for doc in cls.collection().stream()]

    def save(self):
        doc = self.collection().document(document_id=self.id)
        doc.set(document_data=self.to_dict())
        self.id = doc.id
        return self

    @classmethod
    def get(cls, id):
        doc = cls.collection().document(id).get()
        if doc.exists:
            return cls.from_dict(doc.to_dict(), doc.id, doc.create_time)
        raise ObjectDoesNotExist

    @classmethod
    def toArrays(cls, docs):
        return [cls.from_dict(doc.to_dict(), doc.id, doc.create_time) for doc in docs]
    # @classmethod
    # def all(cls):
    #     return [cls.from_dict(doc.to_dict(), doc.id, doc.create_time) for doc in cls.collection().stream()]


class CustomTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
        
        try:
            id_token = auth_header.split()[1]
            print('test')
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            
            user = auth.get_user(uid)
            print(user)
            return (user, None)
        except Exception as e:
            raise exceptions.AuthenticationFailed('Firebase ID 토큰이 유효하지 않습니다.')
# class CustomTokenAuthentication(TokenAuthentication):
#     def authenticate_credentials(self, key):

#         try:
#             decoded_token = auth.verify_id_token(key)
#             uid = decoded_token['uid']
#             user = auth.get_user(uid)
#             return (user, key)
#         except Exception:
#             raise exceptions.AuthenticationFailed('Invalid token.')
