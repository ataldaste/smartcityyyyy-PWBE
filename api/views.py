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

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def importar_ambientes_xlsx(self, request):
        df = pd.read_excel(request.FILES['arquivo'], engine='openpyxl')
        
        for _, row in df.iterrows():
            Ambiente.objects.create(
                sig=row['sig'],
                descricao=row['descricao'],
                responsavel=row['responsavel']
            )
        
        return Response({"mensagem": f"{len(df)} ambientes importados!"})

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [  
        'id', 
        'tipo', 
        'status', 
        'timestamp', 
        'ambiente__sig',
        'latitude',
        'longitude'
    ]

    @action(detail=False, methods=['get'])
    def exportar_dados(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sensores.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Tipo', 'Valor', 'Localização', 'Status', 'Ambiente'])
        for sensor in self.get_queryset():
            writer.writerow([
                sensor.get_tipo_sensor_display(),
                sensor.valor,
                f"{sensor.latitude}, {sensor.longitude}",
                sensor.get_status_display(),
                sensor.ambiente.sig
            ])
        return response

# No SensorViewSet
@action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
def importar_sensores_xlsx(self, request):
    df = pd.read_excel(request.FILES['arquivo'], engine='openpyxl')
    
    for _, row in df.iterrows():
        # 1. Obter ou criar o Sensor
        sensor, created = Sensor.objects.get_or_create(
            mac_address=row['mac_address'],
            defaults={
                'tipo': row['sensor'],  # Ex: 'contador', 'luminosidade'
                'status': row['status'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                # Ambiente (ajuste necessário - veja observação abaixo)
                'ambiente': Ambiente.objects.get(sig='AMB_SIG_AQUI')  # Substituir por lógica real
            }
        )
        
        # 2. Criar histórico
        Historico.objects.create(
            sensor=sensor,
            valor=row['valor'],
            timestamp=row['timestamp']
        )
    
    return Response({"mensagem": f"{len(df)} leituras importadas!"})

class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sensor__id', 'timestamp', 'sensor__ambiente__sig']

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