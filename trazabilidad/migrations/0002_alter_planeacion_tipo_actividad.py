# Generated by Django 5.0.3 on 2024-03-05 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trazabilidad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planeacion',
            name='tipo_actividad',
            field=models.CharField(choices=[('estimacion', 'Estimación'), ('diseno_cp', 'Diseño CP'), ('ejecucion', 'Ejecución'), ('finalizado', 'Finalizado')], max_length=20),
        ),
    ]