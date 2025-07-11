# Generated by Django 5.2.2 on 2025-06-05 04:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VisionAI', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='documento',
        ),
        migrations.CreateModel(
            name='DocumentoFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(help_text='Archivo de la factura (PDF, JPG, PNG, …)', upload_to='facturas/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='VisionAI.factura')),
            ],
        ),
    ]
