# -*- coding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags import humanize
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

from ..models import Alumno, AlumnoMateria, Materia


register = template.Library()


@register.simple_tag(takes_context=True)
def get_carreras(context):
    user = context.get('user')
    if user.is_authenticated:
        carreras = Alumno.objects.select_related('carrera')\
            .filter(user=user).order_by('plancarrera')
        context['list_carreras'] = carreras
    return ''


@register.filter
# C901: is too complex
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
    except ObjectDoesNotExist:
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

    # Marcar las aprobadas
    try:
        lm = planmateria.correlativas.split('-')
    except AttributeError:
        lm = []
    new_l = []
    for m in lm:
        try:
            m_name = Materia.objects.get(id=m.replace('.', '')).name
        except ObjectDoesNotExist:
            m_name = ''
        if m == 'CBC':
            new_m = ('small chelp lt', m, m)
        else:
            new_m = ('small chelp', m, m + ' - ' + m_name)

            if AlumnoMateria.objects\
               .filter(user=user, materia=m.replace('.', ''))\
               .exclude(state='C').exclude(state='F'):
                    new_m = ('small chelp lt', m, m + ' - ' + m_name)
        new_l.append(new_m)
    planmateria.correlativas = new_l

    tab_selected = 'tab_' + context.get('tab_selected', 'cursando')

    return {
        'icon_file': icon_file,
        'title': title,
        'materia': materia,
        'planmateria': planmateria,
        'link_class': link_class,
        'list_correl': list_correl,
        'falta_cuat': falta_cuat,
        'fecha_aprobada': fecha_aprobada,
        'nota': nota,
        tab_selected: True,
    }


register.inclusion_tag('facultad/plancarrera_materia.html',
                       takes_context=True)(display_row_materia)


@register.filter(is_safe=True)
def apnumber(value):
    retvalue = '-'
    try:
        value = int(value)
        if value > 1 and value < 10:
            retvalue = ('%s (' + humanize.apnumber(value) + ')') % value
        elif value == 10:
            retvalue = '10 (' + _('diez') + ')'
    except ValueError:
        retvalue = value
    return retvalue
