from simulations.serializers import SimulationSerializer, ChatSerializer, MemberSerializer, OpenSimulationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from main_utils.chatgpt import ChatGPT
from simulations.models import Simulation, Chat, ChatPersistent, Member, OpenSimulation
from firebase_admin import auth


class SimulationsList(APIView):

    def get_object(self, pk, current_user_id):
        try:
            sim = Simulation.objects.get(id=pk)
            members = sim.member_set.all()

            sim.members = auth.get_users(
                [auth.UidIdentifier(x.uid) for x in members]).users

            for member in sim.members:
                if current_user_id == member.uid:
                    member.current_user = True
                    print(member.uid)
                    break
            return sim
        except Simulation.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

    def get(self, request, pk=None, format=None):
        if pk is not None:
            return Response(SimulationSerializer(self.get_object(pk, request.user)).data)
        simuations = Simulation.objects.filter(member__uid=request.user.uid)
        serializer = SimulationSerializer(simuations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SimulationSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user != 'AnonymousUser':
                return Response({'error' : 'User is not authenticated'}, status=HTTP_400_BAD_REQUEST)
            print('생성중')
            msg = ChatGPT().run(serializer.validated_data['title'], request.data['disease'], request.data['item'], request.data['etc'])
            #msg = ChatGPT().run(serializer.validated_data['title'])
            chats = Chat()
            sim = serializer.create(serializer.validated_data)
            sim.content = msg.content
            sim.chat_id = chats.id

            sim.save()
            member = Member(uid=request.user.uid,
                            email=request.user.email, simulation=sim, owner=True)
            member.save()
            chats.id = str(sim.id)
            chats.save()
            print('응답완료')

            return Response(SimulationSerializer(sim).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class MemberList(APIView):
    def post(self, request, pk):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if (Member.objects.filter(
                        email=serializer.validated_data['email'], simulation=pk).exists()):

                    return Response({'email': ['User already added']}, status=HTTP_400_BAD_REQUEST)
                user = auth.get_user_by_email(
                    serializer.validated_data['email'])

                member = Member()
                member.email = user.email
                member.uid = user.uid
                member.simulation_id = pk
                member.save()
                return Response(MemberSerializer(user).data, status=HTTP_201_CREATED)
            except auth.UserNotFoundError:
                return Response({'email': ['User doesnot exists']}, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ChatList(APIView):
    def get(self,  request, pk, format=None):

        # chats = Chat.collection().where(
        #     filter=firestore.FieldFilter("simulation_id", "==", pk)).get()
        chats = ChatPersistent.objects.filter(simulation=pk)
        print(chats)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            chat_persistent = serializer.save(
                sender=request.user.uid, simulation_id=pk)
            chat = Chat()
            chat.id = str(pk)
            chat.chat_id = str(chat_persistent.id)
            chat.content = serializer.validated_data['content']
            chat.sender = request.user.uid
            chat.simulation_id = pk
            chat.save()

            return Response(ChatSerializer(chat_persistent).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class Regenerate(APIView):
    def post(self, request):
        print(request.data)
        simulations_id = request.data.get('sim_id')
        chats = ChatPersistent.objects.filter(simulation_id=simulations_id).order_by('created').values_list('content', flat=True)
        contents = Simulation.objects.filter(id=simulations_id).values_list('content')[0]
        msg = ChatGPT().re_run(contents[0], chats)
        simulation_instance = Simulation.objects.filter(id=simulations_id).first()
        print(msg.content)
        simulation_instance.content = msg.content
        simulation_instance.save()
        
        return Response(simulations_id, status=HTTP_201_CREATED)
    
class OpenSimulationList(APIView):
    def get(self, request):
        diseases = OpenSimulation.objects.all()
        serializer = OpenSimulationSerializer(diseases, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        simulations_id = request.data.get('sim_id')
        title = Simulation.objects.filter(id=simulations_id).values_list('title')[0]
        content = Simulation.objects.filter(id=simulations_id).values_list('content')[0]
        msg = ChatGPT().runscenario(content)
        imgurl = ChatGPT().imagegpt(content)
        scenario = msg.content
        print(simulations_id)
        data = {
            'id' : str(simulations_id),
            'title' : str(title[0]),
            'content' : str(content[0]),
            'scenario' : str(scenario),
            'imgurl' : str(imgurl)
        }
        simulation_instance = Simulation.objects.filter(id=simulations_id).first()
        simulation_instance.scenario = scenario
        simulation_instance.save()
        serializer = OpenSimulationSerializer(data=data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            scenario_serializer = serializer.save()

            return Response(OpenSimulationSerializer(scenario_serializer).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
