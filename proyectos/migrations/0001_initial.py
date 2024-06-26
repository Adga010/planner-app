# Generated by Django 5.0.3 on 2024-03-04 22:03

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuracion', '0002_rename_guid_cliente_id_rename_guid_linea_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('tarea_tw', models.URLField()),
                ('desarrollador', models.CharField(max_length=100)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.cliente')),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('linea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.linea')),
                ('proceso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.proceso')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.tipo')),
            ],
        ),
    ]
