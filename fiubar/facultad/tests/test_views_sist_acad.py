import logging
from datetime import date

from test_plus.test import TestCase

from ..models import Departamento, Materia
from ..views.sist_acad import parse_materias_aprobadas


logging.disable(logging.CRITICAL)


class Request(object):

    META = {}

    def __init__(self, user, remote_addr):
        self.user = user
        self.META['REMOTE_ADDR'] = remote_addr


class TestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.request = Request(self.user, '1.2.3.4')

        d = Departamento(codigo='61', name='Matematica')
        d.save()

        m = Materia(id='6108', departamento=d,
                    codigo='08', name='Analisis Matematico II')
        m.save()

        m = Materia(id='6103', departamento=d,
                    codigo='03', name='Algebra II')
        m.save()

        m = Materia(id='6109', departamento=d,
                    codigo='09', name='Probabilidad')
        m.save()

        d = Departamento(codigo='62', name='Fisica')
        d.save()

        m = Materia(id='6202', departamento=d,
                    codigo='02', name='Fisica II')
        m.save()

    def test_parse_materias_aprobadas_none(self):
        d = parse_materias_aprobadas(None, self.request)
        self.assertEqual(d, {})

    def test_parse_materias_aprobadas_empty(self):
        d = parse_materias_aprobadas('', self.request)
        self.assertEqual(d, {'materia_list': [], 'materia_list_count': 0,
                             'text_paste': ''})

        d = parse_materias_aprobadas('\n\n\n\n', self.request)
        self.assertEqual(d, {'materia_list': [], 'materia_list_count': 0,
                             'text_paste': '\n\n\n\n'})

    def test_parse_materias_aprobadas_good_lines(self):
        goodlines = '6108  Analisis Matematico II    9    8 - ocho  OBL  20-2-2012   1234  12345   6103\n' # noqa
        goodlines += '6103  Analisis Matematico II    7    8 - ocho OBL  20-2-2012   1234  12345   6103\n' # noqa
        goodlines += '6109  Analisis Matematico II    8    8 - ocho OBL  20-2-2012   1234  12345   6103-6108\n' # noqa
        goodlines += '6202  Fisica II    5    6 - seis OBL  20-2-2012   1234  12345   6201\n' # noqa

        d = parse_materias_aprobadas(goodlines, self.request)

        self.assertEqual(len(d['materia_list']), 4)
        self.assertEqual(d['materia_list_count'], 4)
        self.assertEqual(d['text_paste'], '')

        self.assertEqual(
            d['materia_list'][0],
            [Materia.objects.get(id='6108'), date(2012, 2, 20), '9'])
        self.assertEqual(
            d['materia_list'][1],
            [Materia.objects.get(id='6103'), date(2012, 2, 20), '7'])
        self.assertEqual(
            d['materia_list'][2],
            [Materia.objects.get(id='6109'), date(2012, 2, 20), '8'])
        self.assertEqual(
            d['materia_list'][3],
            [Materia.objects.get(id='6202'), date(2012, 2, 20), '5'])

    def test_parse_materias_aprobadas_bad_lines(self):
        badlines = '6108  Analisis Matematico II    9    '

        d = parse_materias_aprobadas(badlines, self.request)
        self.assertEqual(d, {'materia_list': [],
                             'materia_list_count': 0,
                             'text_paste': badlines})

    def test_parse_materias_aprobadas_not_materia(self):
        notmateria = '6178  Analisis Matematico II    9    8 - ocho OBL  20-2-2012   1234  12345   6103\n' # noqa

        d = parse_materias_aprobadas(notmateria, self.request)
        self.assertEqual(d, {'materia_list': [],
                             'materia_list_count': 0,
                             'text_paste': notmateria})
