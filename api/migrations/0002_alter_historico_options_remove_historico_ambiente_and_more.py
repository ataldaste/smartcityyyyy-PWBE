# Generated by Django 5.1.1 on 2025-05-09 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historico',
            options={'ordering': ['-timestamp']},
        ),
        migrations.RemoveField(
            model_name='historico',
            name='ambiente',
        ),
        migrations.RemoveField(
            model_name='historico',
            name='observacoes',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='valor',
        ),
        migrations.AddField(
            model_name='ambiente',
            name='localizacao',
            field=models.CharField(default='SENAI Mange', max_length=255, verbose_name='Localização'),
        ),
        migrations.AddField(
            model_name='ambiente',
            name='nome',
            field=models.CharField(default='Ambiente', max_length=100, verbose_name='Nome'),
        ),
        migrations.AddField(
            model_name='historico',
            name='unidade_medida',
            field=models.CharField(default='', max_length=10, verbose_name='Unidade'),
        ),
        migrations.AddField(
            model_name='historico',
            name='valor',
            field=models.FloatField(default=0, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='ambiente',
            name='descricao',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='ambiente',
            name='ni',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='NI'),
        ),
        migrations.AlterField(
            model_name='ambiente',
            name='responsavel',
            field=models.CharField(max_length=50, verbose_name='Responsável'),
        ),
        migrations.AlterField(
            model_name='ambiente',
            name='sig',
            field=models.CharField(max_length=10, unique=True, verbose_name='Código SIG'),
        ),
        migrations.AlterField(
            model_name='historico',
            name='timestamp',
            field=models.DateTimeField(verbose_name='Data/Hora'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='latitude',
            field=models.FloatField(verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='longitude',
            field=models.FloatField(verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='mac_address',
            field=models.CharField(max_length=17, unique=True, verbose_name='Endereço MAC'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='status',
            field=models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=7, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='tipo',
            field=models.CharField(choices=[('temperatura', 'Temperatura (°C)'), ('luminosidade', 'Luminosidade (lux)'), ('umidade', 'Umidade (%)'), ('contador', 'Contador (num)')], max_length=12, verbose_name='Tipo'),
        ),
    ]
