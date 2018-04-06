# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django import template
from django.utils.dates import MONTHS
from ..models.models import PlanMateria, Alumno, Carrera, AlumnoMateria, Materia

register = template.Library()

@register.simple_tag(takes_context=True)
def get_carreras(context):
    user = context.get('user')
    if user.is_authenticated:
        carreras = Alumno.objects.select_related('carrera').filter(user=user).order_by('plancarrera')
        context['list_carreras'] = carreras
    return ''

@register.filter
def display_row_materia(context, planmateria):
	materia = planmateria.materia
	user = context['user']
	m = None
	fecha_aprobada = ''
	nota = '-'
	falta_cuat = ''
	list_correl = context.get('lista_materias_a_cursar', None)
	try:
		m = AlumnoMateria.objects.get(user=user, materia=materia)
		if m.aprobada() or m.equivalencia():
			icon_file = 'materia_ap.png'
			title = 'Materia aprobada'
			link_class = 'final'
			falta_cuat = 'Aprobada'
			fecha_aprobada = m.get_aprobada_cuat()
			if m.equivalencia():
				nota = 'Equivalencia'
			else:
				nota = m.nota
		elif m.falta_final():
			icon_file = 'materia_f.png'
			title = 'Cursada aprobada'
			link_class = 'cursada'
			falta_cuat = 'Falta final'
		elif m.cursando():
			icon_file = 'materia_c.png'
			title = 'Cursando'
			link_class = 'cursando'
			falta_cuat = 'Cursando'
	except:
		# Materia todavia no cursada
		icon_file = 'materia_notyet.png'
		title = 'Faltan correlativas'
		link_class = 'correlativa'

		# Verificar que haya aprobado las correlativas
		if list_correl:
			for m in list_correl:
				if m.materia == materia:
					title = 'Disponible para cursar'
					link_class = 'paracursar'
					icon_file = 'materia_cursar.png'
					break
		else:
			title = 'Disponible para cursar'
			link_class = 'paracursar'
			icon_file = 'materia_cursar.png'

		"""
		# falta_cuat = context.get('list_falta_cuat', None)
		# if falta_cuat:
		#	falta_cuat = context['list_falta_cuat'].get(codigo, None)
		"""

	# Marcar las aprobadas
	try:
		l = planmateria.correlativas.split('-')
	except:
		l = []
	new_l = []
	for m in l:
		try:
			m_name = Materia.objects.get(id=m.replace('.', '')).name
		except:
			m_name = ''
		if m == 'CBC':
			new_m = ('small chelp lt', m, m)
		elif AlumnoMateria.objects.filter(user=user, materia=m.replace('.', '')).exclude(state='C').exclude(state='F'):
			new_m = ('small chelp lt', m, m + ' - ' + m_name)
		else:
			new_m = ('small chelp', m, m + ' - ' + m_name)
		new_l.append(new_m)
	planmateria.correlativas = new_l

	tab_selected = 'tab_' + context.get('tab_selected', 'cursando')

	return {
		'icon_file'	: icon_file,
		'title'		: title,
		'materia'	  : materia,
		'planmateria'  : planmateria,
		'link_class'   : link_class,
		'list_correl'  : list_correl,
		'falta_cuat'   : falta_cuat,
		'fecha_aprobada' : fecha_aprobada,
		'nota'		 : nota,
		tab_selected   : True,
	}
register.inclusion_tag('facultad/plancarrera_materia.html', takes_context=True)(display_row_materia)

from django.contrib.humanize.templatetags import humanize
@register.filter
def apnumber(value):
	retvalue = '-'
	try:
		value = int(value)
		if value > 1 and value < 10:
			retvalue = ('%s (' + humanize.apnumber(value) + ')') % value
		elif value == 10:
			retvalue = '10 (' + _('diez') + ')'
	except:
		retvalue = value
	return retvalue

@register.filter
def carreras_cloud(context):
	from django.db import connection
	cursor = connection.cursor()
	cursor.execute("""
		SELECT c.short_name, a.carrera_id, COUNT(a.*) AS carrera_count
		from _alumno a, facultad_carrera c
		WHERE c.id = a.carrera_id
		GROUP BY a.carrera_id, c.short_name
		ORDER BY carrera_count DESC""")
	carreras_count_list = []
	for row in cursor.fetchall():
		p = Carrera.objects.model(id=row[1], short_name=row[0])
		p.carrera_count = row[2]
		carreras_count_list.append(p)

	# Get min and max
	c_count = len(carreras_count_list)
	c_min = carreras_count_list[c_count - 1].carrera_count
	c_max  = carreras_count_list[0].carrera_count
	font_min = 8
	font_max = 14
	for c in carreras_count_list:
		c.font_size = font_min + ((c.carrera_count - c_min) * (font_max - font_min)) / (c_max - c_min)
	return { 'carrera_list' : carreras_count_list.order_by('short_name') }
register.inclusion_tag('facultad/plugins/carreras_cloud.html', takes_context=True)(carreras_cloud)

@register.filter
def last_news_facultad(context):
	"""Plugin: shows last alumnos in materias and carreras"""
	last_login = context.get('last_login', None)
	new_alu_carrera = Alumno.objects.count_new(context['user'], last_login)
	new_alu_materia = AlumnoMateria.objects.count_new(context['user'], last_login)
	carrera = Alumno.objects.filter(user=context['user'])
	materias = AlumnoMateria.objects.filter(user=context['user'])
	utils.close_plugin(context)
	return { 'new_alu_carrera' : new_alu_carrera,
			 'new_alu_materia' : new_alu_materia,
			 'carrera' : carrera, 'materias' : materias,
	}
register.inclusion_tag('facultad/plugins/last_news_facultad.html', takes_context=True)(last_news_facultad)

@register.filter
def last_events_facultad(context):
	"""Plugin: shows next facultad events"""
	event_list = EventMateria.objects.list_event_materia_cursando(context['user'])
	if event_list: utils.close_plugin(context)
	return { 'event_list' : event_list, }
register.inclusion_tag('facultad/plugins/last_events_facultad.html', takes_context=True)(last_events_facultad)

def facultad_user_menu(context):
	"""Menu Plugin"""
	carrera = Alumno.objects.filter(user=context['user'])
	return { 'carrera' : carrera, }
register.inclusion_tag('facultad/plugins/facultad_user_menu.html', takes_context=True)(facultad_user_menu)

from datetime import date, timedelta
@register.filter
def future_dates_only(the_date):
	dd, mm, yy = the_date.split('/')
	if not dd or not mm or not yy:
		dd = mm = yy = 1
	the_date = date(int(yy), int(mm), int(dd))
	if the_date - date.today() >= timedelta(days=-6):
		return True
	else:
		return False
