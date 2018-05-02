from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facultad', '0003_rename_table'),
    ]

    state_operations = [
        migrations.DeleteModel('Alumno'),
        migrations.DeleteModel('AlumnoMateria'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
