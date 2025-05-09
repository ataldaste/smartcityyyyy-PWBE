from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ambiente, Sensor, Historico
from .serializers import AmbienteSerializer, SensorSerializer, HistoricoSerializer, AutenticacaoSerializer
from django.contrib.auth.models import User
from unidecode import unidecode
from rest_framework.parsers import MultiPartParser, FormParser
import csv

# ======================= AMBIENTES =======================
class AmbienteViewSet(viewsets.ModelViewSet):
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sig', 'descricao']  

    @action(detail=False, methods=['get'])
    def exportar_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ambientes.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Código', 'Descrição', 'Responsável'])
        for ambiente in self.get_queryset():
            writer.writerow([
                ambiente.sig,
                ambiente.descricao,
                ambiente.responsavel
            ])
        return response



class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'tipo': ['exact'],
        'status': ['exact'],
        'ambiente__sig': ['exact'],
        'mac_address': ['exact']
    }

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def importar_dados(self, request):
        file = request.FILES['arquivo']
        df = pd.read_excel(file)
        
        for _, row in df.iterrows():
            sensor, _ = Sensor.objects.update_or_create(
                mac_address=row['mac_address'],
                defaults={
                    'tipo': row['sensor'],
                    'latitude': row['latitude'],
                    'longitude': row['longitude'],
                    'status': row['status'],
                    'ambiente': Ambiente.objects.get(sig=row['ambiente_sig'])  # Supondo que a planilha tem essa coluna
                }
            )
        return Response({"status": f"{len(df)} sensores importados"})


class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'sensor__id': ['exact'],
        'timestamp': ['gte', 'lte'],  # Filtro por intervalo de datas
        'sensor__tipo': ['exact'],
        'sensor__ambiente__sig': ['exact']
    }

    @action(detail=False, methods=['get'])
    def exportar_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="historicos.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Sensor', 'Tipo', 'Valor', 'Unidade', 'Data', 'Ambiente'])
        
        for historico in self.filter_queryset(self.get_queryset()):
            writer.writerow([
                historico.sensor.mac_address,
                historico.sensor.tipo,
                historico.valor,
                historico.unidade_medida,
                historico.timestamp,
                historico.sensor.ambiente.sig
            ])
        
        return response

class AutenticacaoViewSet(viewsets.ViewSet):
    serializer_class = AutenticacaoSerializer  

    @action(detail=False, methods=['post'], permission_classes=[])
    def registrar_usuario(self, request):
        serializer = self.get_serializer(data=request.data)
        

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        nome_completo = serializer.validated_data['nome'].strip()
        matricula = serializer.validated_data['matricula'].strip()

        username = matricula
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'erro': 'Matrícula já registrada'},
                status=status.HTTP_400_BAD_REQUEST
            )

        partes_nome = nome_completo.split()
        primeiro_nome = unidecode(partes_nome[0].lower()) if partes_nome else ''
        sobrenome = ' '.join(partes_nome[1:]) if len(partes_nome) > 1 else ''

        try:
            User.objects.create_user(
                username=username,
                password=matricula,
                first_name=primeiro_nome,
                last_name=sobrenome
            )
            return Response(
                {'mensagem': 'Usuário criado com sucesso!'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'erro': f'Erro interno: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )