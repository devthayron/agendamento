# Generated by Django 5.2 on 2025-04-29 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0004_alter_agendamento_data_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamento',
            name='data_hora',
            field=models.DateTimeField(),
        ),
    ]
