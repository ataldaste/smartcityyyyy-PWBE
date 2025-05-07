from rest_framework import serializers
from .models import Ambiente, Sensor, Historico
from django.contrib.auth.models import User

class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiente
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class HistoricoSerializer(serializers.ModelSerializer):
    sensor = SensorSerializer(read_only=True)
    ambiente = AmbienteSerializer(read_only=True)

    class Meta:
        model = Historico
        fields = '__all__'


class AutenticacaoSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=255, required=True)
    matricula = serializers.CharField(min_length=6, max_length=6, required=True)

    def validate_matricula(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Matrícula deve conter apenas dígitos.")
        return value