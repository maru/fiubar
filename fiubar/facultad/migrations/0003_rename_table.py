from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        # This migration should depend on the previous migration in our app
        ('facultad', '0002_auto_20180502_1135'),
    ]

    operations = [
        migrations.AlterModelTable(name='Alumno', table='alumnos_plancarrera'),
        migrations.AlterModelTable(name='AlumnoMateria', table='alumnos_materia'),
    ]
