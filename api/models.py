from django.db import models

class Ambiente(models.Model):
    sig = models.CharField("Código SIG", max_length=10, unique=True)  # Equivalente ao codigo_sig do requisito
    nome = models.CharField("Nome", max_length=100, default="Ambiente")  # Campo obrigatório do requisito
    localizacao = models.CharField("Localização", max_length=255, default="SENAI Mange")  # Campo obrigatório do requisito
    descricao = models.CharField("Descrição", max_length=100, blank=True, null=True)  # Da planilha
    ni = models.CharField("NI", max_length=20, blank=True, null=True)  # Da planilha
    responsavel = models.CharField("Responsável", max_length=50)  # Da planilha

    def __str__(self):
        return f"{self.sig} - {self.nome}"

class Sensor(models.Model):
    TIPOS_SENSOR = (
        ('temperatura', 'Temperatura (°C)'),
        ('luminosidade', 'Luminosidade (lux)'),
        ('umidade', 'Umidade (%)'),
        ('contador', 'Contador (num)'),
    )
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    )
    
    ambiente = models.ForeignKey(Ambiente, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField("Tipo", max_length=12, choices=TIPOS_SENSOR)
    mac_address = models.CharField("Endereço MAC", max_length=17, unique=True)
    latitude = models.FloatField("Latitude")
    longitude = models.FloatField("Longitude")
    status = models.CharField("Status", max_length=7, choices=STATUS_CHOICES, default='ativo')

    def __str__(self):
        return f"{self.tipo} ({self.mac_address})"

class Historico(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='historicos')
    valor = models.FloatField("Valor", default=0)
    timestamp = models.DateTimeField("Data/Hora")
    unidade_medida = models.CharField("Unidade", max_length=10, default="")  # Nova coluna baseada nas planilhas

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sensor.tipo} - {self.valor}{self.unidade_medida} ({self.timestamp})"