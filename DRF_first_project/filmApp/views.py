from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializer import *


class HelloApi(APIView):
    def get(self, request):
        d = {
            "xabar": "Salom dunyo!",
            "qo'shimcha": "Bu DRF dagi birinchi API miz boldi"
        }
        return Response(d)
    def post(self, request):
        data = request.data
        p = {
            "xabar": "post data qilish",
            "post bolgan malumot": data
        }
        return Response(p)
class AboutMe(APIView):
    def get(self, request):
        I = {
            "name": "Abdulhamid",
            "lastName": "Ahmedov",
            "age": 19,
            "region": "Uzbekistan",
            "job": "Programmer"
        }
        return Response(I)

class AktyorlarApi(APIView):
    def get(self, request):
        aktyorlar = Aktyor.objects.all()
        qidiruv_sozi = request.query_params.get("name")
        if qidiruv_sozi:
            aktyorlar = Aktyor.objects.filter(ism__contains=qidiruv_sozi)
        chet_ellik = request.query_params.get("chet_ellik")
        if qidiruv_sozi:
            aktyorlar = Aktyor.objects.filter(ism__contains=qidiruv_sozi)
        if chet_ellik is not None:
            if chet_ellik == 'False':
                aktyorlar = aktyorlar.filter(davlat="O'zbekiston")
            else:
                aktyorlar = aktyorlar.exclude(davlat="O'zbekiston")
        serializer = AktyorSerializer(aktyorlar, many=True)
        return Response(serializer.data)
    def post(self, request):
        aktyor = request.data
        serializer = AktyorSerializer(data=aktyor)
        if serializer.is_valid():
            valid_data = serializer.validated_data
            Aktyor.objects.create(
                ism = valid_data.get('ism'),
                davlat = valid_data.get('davlat'),
                jins = valid_data.get('jins'),
                tugilgan_sana = valid_data.get('tugilgan_sana'),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AktyorApi(APIView):
    def get(self, request, pk):
        aktyor = Aktyor.objects.get(id=pk)
        serializer = AktyorSerializer(aktyor)
        return Response(serializer.data)
    def put(self, request, pk):
        data = request.data
        aktyor = Aktyor.objects.filter(id=pk)
        serializer = AktyorSerializer(aktyor, data=data)
        if serializer.is_valid():
            aktyor.update(
                davlat=serializer.validate_data.get('davlat')
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        aktyor = Aktyor.objects.get(id=pk)
        aktyor.delete()
        return Response({"success": "true"}, status=status.HTTP_200_OK)

class TarifApi(APIView):
    def get(self, request):
        tariflar = Tarif.objects.all()
        serializer = TarifSerialaizer(tariflar, many=True)
        return Response(serializer.data)
    def post(self, request):
        tarif = request.data
        serializer = TarifSerialaizer(data=tarif)
        if serializer.is_valid():
            valid_data = serializer.validated_data
            print(valid_data)
            Tarif.objects.create(
                nom = valid_data.get('nom'),
                davomiylik = valid_data.get('davomiylik'),
                narx = valid_data.get('narx'),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KinolarApi(APIView):
    def get(self, request):
        kinolar = Kino.objects.all()
        qidiruv_sozi = request.query_params.get("name")
        if qidiruv_sozi:
            kinolar = Kino.objects.filter(nom__contains=qidiruv_sozi)
        serializer = KinoSerializer(kinolar, many=True)
        return Response(serializer.data)
    def post(self, request):
        kino = request.data
        serializer = KinoPostSerializer(data=kino)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class KinoApi(APIView):
    def get(self, request, pk):
        kino = Kino.objects.get(id=pk)
        serializer = KinoSerializer(kino)
        return Response(serializer.data)
    def put(self, request, pk):
        data = request.data
        kino = Kino.objects.get(id=pk)
        serializer = KinoPostSerializer(kino, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class KinoModelViewSet(ModelViewSet):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nom", "janr", "yil"]  #/movies/?search=
    ordering_fields = ["id", "yil", "nom"]  #/movies/?ordering=(bu yerda faqat ustunni nomi yozilishi mumkin)

    pagination_class = PageNumberPagination
    pagination_class.page_size = 2

    def get_queryset(self):
        queryset = self.queryset
        ismi = self.request.query_params.get("ism")
        if ismi:
            queryset = queryset.filter(aktyorlar__ism__contains=ismi)
        return queryset
