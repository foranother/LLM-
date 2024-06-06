from main_utils.firestore import Firestore
from django.db import models
from simnursebe.models import BaseModel
import uuid

# Create your models here.


class Simulation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False)
    diseaseitem = models.CharField(max_length=100, null=True)
    owner_id = models.TextField(blank=False)
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    item = models.TextField(null=True)
    scenario = models.TextField(blank=True, null=True)
    etc = models.TextField(max_length=200, blank=True, null=True)
    
class OpenSimulation(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    scenario = models.TextField(blank=False)
    imgurl = models.TextField(blank=True)
    

class Member(models.Model):
    uid = models.TextField(blank=False)
    email = models.TextField(blank=False)
    owner = models.BooleanField(default=False)
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)


class ChatPersistent(models.Model):
    sender = models.TextField(blank=False)
    content = models.TextField(blank=False)
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Chat(BaseModel):

    sender = None
    content = None
    simulation_id = None
    chat_id = None

    @staticmethod
    def collection():
        return Firestore().client.collection('chats')

    @staticmethod
    def from_dict(source, id, create_time):
        obj = Chat()

        obj.sender = source['sender']
        obj.content = source['content']
        obj.simulation_id = source['simulation_id']
        obj.id = id
        obj.chat_id = source['chat_id']
        obj.created = create_time
        return obj

    def to_dict(self):
        return {
            'sender': self.sender,
            'content': self.content,
            'simulation_id': self.simulation_id,
            'chat_id': self.chat_id
        }


