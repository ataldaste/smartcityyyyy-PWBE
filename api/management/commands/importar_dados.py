import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Ambiente, Sensor, Historico
from django.utils.timezone import make_aware
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / 'data'

class Command(BaseCommand):
    help = 'Importa dados das planilhas Excel para o banco'

    def handle(self, *args, **options):
        self.importar_ambientes()
        self.importar_sensor_tipo('temperatura')
        self.importar_sensor_tipo('umidade')
        self.importar_sensor_tipo('luminosidade')
        self.importar_sensor_tipo('contador')

    def importar_ambientes(self):
        try:
            df = pd.read_excel(BASE_DIR / 'Ambientes.xlsx')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler Ambientes.xlsx: {e}'))
            return

        for _, row in df.iterrows():
            ambiente, created = Ambiente.objects.get_or_create(
                sig=row['sig'],
                defaults={
                    'nome': row.get('descricao', 'Ambiente'),
                    'descricao': row.get('descricao', ''),
                    'ni': row.get('ni', ''),
                    'responsavel': row.get('responsavel', ''),
                    'localizacao': "Local não informado"
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Ambiente criado: {ambiente.sig}'))
            else:
                self.stdout.write(f'Ambiente já existe: {ambiente.sig}')

    def importar_sensor_tipo(self, tipo):
        filename = f"{tipo}.xlsx"
        file_path = BASE_DIR / filename
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Arquivo {filename} não encontrado. Pulando...'))
            return

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler {filename}: {e}'))
            return

        for _, row in df.iterrows():
            ambiente = Ambiente.objects.filter(sig=row['sig']).first()
            if not ambiente:
                self.stdout.write(self.style.WARNING(f"Ambiente '{row['sig']}' não encontrado. Pulando sensor {row['mac_address']}"))
                continue

            sensor, _ = Sensor.objects.get_or_create(
                mac_address=row['mac_address'],
                defaults={
                    'tipo': tipo,
                    'latitude': row.get('latitude'),
                    'longitude': row.get('longitude'),
                    'status': row.get('status', 'ativo'),
                    'ambiente': ambiente
                }
            )

            try:
                timestamp = make_aware(pd.to_datetime(row['timestamp']))
            except:
                timestamp = None

            Historico.objects.create(
                sensor=sensor,
                valor=row['valor'],
                timestamp=timestamp,
                unidade_medida=row.get('unidade_medida', '')
            )

        self.stdout.write(self.style.SUCCESS(f'Dados de {tipo} importados com sucesso.'))
