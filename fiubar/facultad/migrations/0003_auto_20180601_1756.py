# Generated by Django 2.0.4 on 2018-06-01 20:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facultad', '0002_auto_20180523_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='begin_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='plancarrera',
            name='carrera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plancarreras', to='facultad.Carrera'),
        ),
        migrations.AlterField(
            model_name='planmateria',
            name='plancarrera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planmaterias', to='facultad.PlanCarrera'),
        ),
    ]