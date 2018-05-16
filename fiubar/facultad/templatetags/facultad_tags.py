# -*- coding: utf-8 -*-
from django import template
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


@register.inclusion_tag('facultad/plancarrera_materia.html',
                        takes_context=True)
def display_row_materia(context, planmateria):
    d = {
        '-': {  # A cursar en el futuro, faltan correlativas
            'icon_file': 'materia_notyet.png',
            'title': 'Faltan correlativas',
            'link_class': 'correlativa',
            'falta_cuat': '',
            'fecha_aprobada': '',
            'nota': '-',
        },
        'C': {  # Cursando
            'icon_file': 'materia_c.png',
            'title': 'Cursando',
            'link_class': 'cursando',
            'falta_cuat': 'Cursando',
            'fecha_aprobada': '',
            'nota': '-',
        },
        'F': {  # Falta final
            'icon_file': 'materia_f.png',
            'title': 'Cursada aprobada',
            'link_class': 'cursada',
            'falta_cuat': 'Falta final',
            'fecha_aprobada': '',
            'nota': '-',
        },
        'A': {  # Aprobada
            'icon_file': 'materia_ap.png',
            'title': 'Materia aprobada',
            'link_class': 'final',
            'falta_cuat': 'Aprobada',
        },
        'E': {  # Equivalencia
            'icon_file': 'materia_ap.png',
            'title': 'Equivalencia',
            'link_class': 'final',
            'falta_cuat': 'Aprobada',
            'nota': '-',
        },
        'D': {  # Disponible para cursar
            'icon_file': 'materia_cursar.png',
            'title': 'Disponible para cursar',
            'link_class': 'paracursar',
            'falta_cuat': '',
            'fecha_aprobada': '',
            'nota': '-',
        },
    }

    state = '-'
    user = context['user']
    lista_correl = context.get('lista_materias_a_cursar', [])
    lista_materias_a_cursar = [m.materia for m in lista_correl]

    try:
        materia = planmateria.materia
    except AttributeError:
        return d[state]

    # Alumno anotado en materia?
    try:
        m = AlumnoMateria.objects.get(user=user, materia=materia)

        state = m.state
        d[state].update({'fecha_aprobada': m.get_aprobada_cuat()})
        d[state].update({'nota': m.nota})

    # Materia todavia no cursada
    except ObjectDoesNotExist:
        # Verificar que haya aprobado las correlativas
        if materia in lista_materias_a_cursar:
            state = 'D'

    d[state].update({'materia': materia})

    # Mostrar solo las materias no aprobadas en la lista de correlativas
    correlativas_str = planmateria.correlativas.split('-')
    correlativas = [c.replace('.', '') for c in correlativas_str]
    new_l = []  # lista de correlativas, con formato

    mat_correl = Materia.objects.filter(id__in=correlativas)
    mat_aprob = [m.materia for m in
                 AlumnoMateria.objects.filter(user=user, state__in=['A', 'E'])]
    for m in mat_correl:
        idx = correlativas.index(m.id)
        m_codigo = correlativas_str[idx]
        if m in mat_aprob:
            new_m = ('small chelp lt', m_codigo, m_codigo + ' - ' + m.name)
        else:
            new_m = ('small chelp', m_codigo, m_codigo + ' - ' + m.name)
        new_l.append(new_m)

    if 'CBC' in correlativas:
        new_m = ('small chelp lt', 'CBC', 'CBC')
        new_l.append(new_m)
    planmateria.correlativas = new_l

    tab_selected = 'tab_' + context.get('tab_selected', 'cursando')

    d[state].update({
        'planmateria': planmateria,
        'list_correl': lista_correl,
        tab_selected: True,
    })

    return d[state]


@register.filter(is_safe=True)
def apnumber(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return '-'
    if not 0 < value <= 10:
        return '-'
    txt = (_('uno'), _('dos'), _('tres'), _('cuatro'), _('cinco'),
           _('seis'), _('siete'), _('ocho'), _('nueve'), _('diez'))[value - 1]
    return ('%s (%s)') % (value, txt)
