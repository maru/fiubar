"""
From https://mikola.by/blog/how-move-model-between-two-django-apps/
"""
from django.db import migrations, models


def update_contentypes(apps, schema_editor):
    """
    Updates content types.
    We want to have the same content type id, when the model is moved and renamed.
    """
    ContentType = apps.get_model('contenttypes', 'ContentType')
    db_alias = schema_editor.connection.alias

    # Move the Alumno model to alumnos and rename to PlanCarrera
    qs = ContentType.objects.using(db_alias).filter(app_label='facultad', model='Alumno')
    qs.update(app_label='alumnos', model='PlanCarrera')

    # Move the AlumnoMateria model to alumnos and rename to Materia
    qs = ContentType.objects.using(db_alias).filter(app_label='facultad', model='AlumnoMateria')
    qs.update(app_label='alumnos', model='Materia')

def update_contentypes_reverse(apps, schema_editor):
    """
    Reverts changes in content types.
    """
    ContentType = apps.get_model('contenttypes', 'ContentType')
    db_alias = schema_editor.connection.alias

    # Move the PlanCarrera model to facultad and rename to Alumno
    qs = ContentType.objects.using(db_alias).filter(app_label='alumnos', model='PlanCarrera')
    qs.update(app_label='facultad', model='Alumno')

    # Move the Materia model to facultad and rename to AlumnoMateria
    qs = ContentType.objects.using(db_alias).filter(app_label='alumnos', model='Materia')
    qs.update(app_label='facultad', model='AlumnoMateria')

class Migration(migrations.Migration):

    dependencies = [
        # We need to run 0003_rename_table form facultad first,
        # because it changes the table of Alumno.
        # Only after that we will update content types and rename the model.
        ('facultad', '0003_rename_table'),
        # This migration also depends on the contenttype app,
        # so we need to specify dependency on 0002_remove_content_type_name.
        # If you use Django < 1.8, you will probably need to specify 0001_initial.
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField()),
                ('graduado_date', models.DateField(null=True)),
                ('creditos', models.IntegerField(default=0)),
                ('promedio', models.FloatField(default=0.0)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AlumnoMateria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('C', 'Cursando'), ('F', 'Cursada Aprobada'), ('A', 'Materia Aprobada'), ('E', 'Equivalencia')], default='C', max_length=1)),
                ('cursada_cuat', models.CharField(blank=True, max_length=10, null=True)),
                ('cursada_date', models.DateField(blank=True, null=True)),
                ('aprobada_cuat', models.CharField(blank=True, max_length=10, null=True)),
                ('aprobada_date', models.DateField(blank=True, null=True)),
                ('nota', models.IntegerField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Alumno',
            new_name='PlanCarrera',
        ),
        migrations.RenameModel(
            old_name='AlumnoMateria',
            new_name='Materia',
        ),
    ]

    database_operations = [
        migrations.RunPython(update_contentypes, update_contentypes_reverse),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations,
            database_operations=database_operations
        ),
    ]
