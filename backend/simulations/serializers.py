import time

from main_utils.serializers import FirebaseModelSerializer
from rest_framework import serializers
from simulations.models import Simulation, Chat, ChatPersistent, Member, OpenSimulation
from firebase_admin import auth
from django.contrib.auth.models import User

class MemberSerializer(serializers.Serializer):

    display_name = serializers.CharField(read_only=True)
    uid = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=True)
    photo_url = serializers.CharField(read_only=True)
    current_user = serializers.BooleanField(read_only=True)
    
class OpenSimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenSimulation
        fields = ['id', 'title', 'content', 'scenario', 'imgurl']


class SimulationSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, required=False)
    class Meta:
        model = Simulation
        fields = ['id', 'title', 'disease' 'item', 'etc', 'content', 'created', 'members', 'scenario']
        read_only_fields = ['id', 'content', 'created', 'members']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatPersistent
        fields = ['id', 'sender', 'content', 'created']
        read_only_fields = ['id', 'sender', 'created']


# class ChatSerializer(FirebaseModelSerializer):
#     uid = serializers.CharField(read_only=True)
#     content = serializers.CharField(required=True)
#     created = serializers.CharField(read_only=True)

#     def create(self, validated_data):
#         obj = Chat()
#         obj.content = validated_data['content']
#         obj.uid = validated_data['uid']
#         obj.created = time.time()
#         return obj

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.sender = validated_data.get('sender', instance.sender)
#         instance.content = validated_data.get('content', instance.content)
#         instance.save()
#         return instance
