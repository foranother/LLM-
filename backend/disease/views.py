from rest_framework.views import APIView
from rest_framework.response import Response
from disease.models import Disease
from disease.serializers import DiseaseSerializers
from firebase_admin.firestore import firestore
import pandas as pd
# Create your views here.


def init_disease(request):
    pass
    # for index, row in pd.read_csv('data/disease_list.csv').iterrows():
    #     d = Disease()
    #     d.id = row['id']
    #     d.en = row['en']
    #     d.kr = row['kr']
    #     d.save()


class DiseaseList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        # query_param = request.GET.get('name', None)
        # filter_1 = firestore.And(
        #     filters=[firestore.FieldFilter('en', '>=', query_param), firestore.FieldFilter('en', '<=', query_param + '~')])

        # filter_2 = firestore.And(
        #     filters=[firestore.FieldFilter('kr', '>=', query_param), firestore.FieldFilter('kr', '<=', query_param + '~')])

        # filters = firestore.Or(filters=[filter_1, filter_2])
        # if (query_param is not None):
        #     diseases = Disease.toArrays(Disease.collection().where(
        #     serializer = DiseaseSerializers(diseases, many=True)
        #     return Response(serializer.data)

        diseases = Disease.objects.all()
        serializer = DiseaseSerializers(diseases, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
