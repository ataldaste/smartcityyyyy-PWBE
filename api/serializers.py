from rest_framework import serializers
from .models import Ambiente, Sensor, Historico
from django.contrib.auth.models import User

class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiente
        fields = ['id', 'sig', 'nome', 'localizacao', 'descricao', 'ni', 'responsavel']

class SensorSerializer(serializers.ModelSerializer):
    ambiente_sig = serializers.CharField(source='ambiente.sig', read_only=True)
    
    class Meta:
        model = Sensor
        fields = ['id', 'tipo', 'mac_address', 'status', 'latitude', 'longitude', 'ambiente', 'ambiente_sig']

class HistoricoSerializer(serializers.ModelSerializer):
    sensor_tipo = serializers.CharField(source='sensor.tipo', read_only=True)
    ambiente_sig = serializers.CharField(source='sensor.ambiente.sig', read_only=True)
    
    class Meta:
        model = Historico
        fields = ['id', 'valor', 'timestamp', 'unidade_medida', 'sensor', 'sensor_tipo', 'ambiente_sig']


class AutenticacaoSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=255, required=True)
    matricula = serializers.CharField(min_length=6, max_length=6, required=True)

    def validate_matricula(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Matrícula deve conter apenas dígitos.")
        return value