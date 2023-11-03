from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Kino


class AktyorSerializer(serializers.Serializer):
    ism = serializers.CharField()
    davlat = serializers.CharField()
    jins = serializers.CharField()
    tugilgan_sana = serializers.DateField()

    def validate_jins(self, qiymat):
        if qiymat == "Male" or qiymat == "Famale":
            return qiymat
        raise ValidationError("Wrong value for gender!")
    def validate_ism(self, qiymat):
        if len(qiymat) > 3:
            return qiymat
        raise ValidationError("You need to write letter more than 3")

class TarifSerialaizer(serializers.Serializer):
    nom = serializers.CharField()
    davomiylik = serializers.CharField()
    narx = serializers.CharField()

class KinoSerializer(serializers.ModelSerializer):
    # aktyorlar = AktyorSerializer(many=True)
    class Meta:

        model = Kino
        fields = "__all__"  #["id", "nom"]

class KinoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kino
        fields = "__all__"  #["id", "nom"]
