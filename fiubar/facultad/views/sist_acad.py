# -*- coding: utf-8 -*-
import datetime
import logging
import re

from django.core.exceptions import ObjectDoesNotExist

from ..models import AlumnoMateria, Materia


# Get an instance of a logger
logger = logging.getLogger('fiubar')

re_infoacad = re.compile(r"""^\s*
    (?P<cod_materia>\d+)\s+
    (?P<description>.+)\s+
    (?P<nota>\d+)\s+
    (?P<creditos>\d+\s-\s\w+)\s+
    (?P<condicion>\w+)\s+
    (?P<final_date>\d+-\d+-\d+)\s*
    (?P<libro>\d*)\s*
    (?P<folio>\d*)\s*
    (?P<correlativas>.*)$
""", re.X)


def parse_materias_aprobadas(paste, request):
    lines = paste.split("\n")
    materia_list = []
    notfound_list = []
    for l in lines:
        match = re_infoacad.match(l)
        if match:
            # Line matched regex
            dict_materia = match.groupdict()
            try:
                # Find materia
                cod_materia = dict_materia.setdefault('cod_materia', '0')
                materia = Materia.objects.get(id=cod_materia)
                nota = dict_materia.setdefault('nota', 0)
                day, month, year = dict_materia\
                    .setdefault('final_date', '0-0-0').split('-')
                final_date = datetime.date(int(year), int(month), int(day)) \
                    if year != '0' else None
                AlumnoMateria.objects.create_or_update(request.user,
                                                       materia, final_date,
                                                       nota)
                logger.info("%s - cargar_materias: user '%s', "
                            "materia '%s', fecha '%s', nota '%s'" %
                            (request.META.get('REMOTE_ADDR'),
                             request.user, materia.id, final_date, nota))
                materia_list.append([materia, final_date, nota])
            except ObjectDoesNotExist:
                # Materia not found
                notfound_list.append(l)
                logger.error("%s - cargar_materias: user '%s', "
                             "materia 'NOT FOUND', line '%s'" %
                             (request.META.get('REMOTE_ADDR'),
                              request.user, l))
        else:
            # Not matched
            notfound_list.append(l)
            logger.error("%s - cargar_materias: user '%s', "
                         "line NOT MATCH '%s'" %
                         (request.META.get('REMOTE_ADDR'),
                          request.user, l))
    dict_result = {'text_paste': "\n".join(notfound_list),
                   'materia_list': materia_list,
                   'materia_list_count': len(materia_list)
                   }
    return dict_result
