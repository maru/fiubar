fiubar
======

Administrador de materias para FIUBA.

De manera simple y ordenada, podés organizar tu carrera y decidir qué materias cursar.

# Para acceder a fiubar: http://fiubar.tk/


Instalación
===========

$ git clone https://github.com/maru/fiubar.git
$ ls

    fiubar  LICENSE  openmate  README.md
    
$ wget 'https://www.djangoproject.com/m/releases/1.2/Django-1.2.7.tar.gz'
$ tar zxf Django-1.2.7.tar.gz
$ cd fiubar/
$ python manage.py syncdb

	(crea las tablas en la base de datos y un usuario administrador)

$ python manage.py loaddata ../fiubar.json

    Installing json fixture '../fiubar' from absolute path.
    Installed 4362 object(s) from 1 fixture(s)
	
$ python manage.py runserver

... y abrir el navegador en http://127.0.0.1:8000/ :)