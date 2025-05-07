from django.db import models

class Ambiente(models.Model):
    sig = models.CharField(max_length=10, unique=True)
    descricao = models.CharField(max_length=100)
    ni = models.CharField(max_length=20)
    responsavel = models.CharField(max_length=50)

    def __str__(self):
        return self.sig

class Sensor(models.Model):
    TIPOS_SENSOR = (
        ('temperatura', 'Temperatura (°C)'),
        ('luminosidade', 'Luminosidade (lux)'),
        ('umidade', 'Umidade (%)'),
        ('contador', 'Contador (num)'),
    )
    TIPOS_STATUS = (('ativo', 'Ativo'), ('inativo', 'Inativo'))
    
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE, related_name='sensores')
    tipo = models.CharField(max_length=12, choices=TIPOS_SENSOR)
    mac_address = models.CharField(max_length=17, unique=True)
    valor = models.CharField(max_length=10) 
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=7, choices=TIPOS_STATUS, default='ativo')
    timestamp = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.tipo} ({self.mac_address})"

class Historico(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='historicos')
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE, related_name='historicos')
    observacoes = models.TextField()  
    timestamp = models.CharField(max_length=20)

    def __str__(self):
        return f"Histórico {self.id}"