import logging
from datetime import date

from ..models import Materia
from ..views.sist_acad import parse_materias_aprobadas
from .common import BaseUserTestCase


logging.disable(logging.CRITICAL)

GOOD_LINES = '6108  Analisis Matematico II    9    8 - ocho  OBL  20-2-2012   1234  12345   6103\n' # noqa
GOOD_LINES += '6103  Algebra II    7    8 - ocho OBL  20-2-2012   1234  12345   6103\n' # noqa
GOOD_LINES += '6109  Probabilidad I    8    8 - ocho OBL  20-2-2012   1234  12345   6103-6108\n' # noqa
GOOD_LINES += '6202  Fisica II    5    6 - seis OBL  20-2-2012   1234  12345   6201\n' # noqa
GOOD_LINES += '6205  Fisica V    5    6 - seis OBL  20-2-2012   1234  12345   6201\n' # noqa

EMPTY_LINES = '\n\n\n\n'
BAD_LINES = '6108  Analisis Matematico II    9    '

NOT_MATERIA_LINES = '6178  Analisis Matematico II    9    8 - ocho OBL  20-2-2012   1234  12345   6103\n' # noqa

MATERIA_APROBADA_LINES = '9503  loving_perlman    7    6 - seis  OBL  23-2-2012   1234  12345   \n' # noqa


class SistAcadTestCase(BaseUserTestCase):

    def setUp(self):
        super(SistAcadTestCase, self).setUp()
        self.remote_addr = '1.2.3.4'

    def test_parse_materias_aprobadas_none(self):
        d = parse_materias_aprobadas(self.user, None, self.remote_addr)
        self.assertEqual(d, {})

    def test_parse_materias_aprobadas_empty(self):
        d = parse_materias_aprobadas(self.user, '', self.remote_addr)
        self.assertEqual(d, {'materia_list': [], 'materia_list_count': 0,
                             'text_paste': ''})

        d = parse_materias_aprobadas(self.user, EMPTY_LINES, self.remote_addr)
        self.assertEqual(d, {'materia_list': [], 'materia_list_count': 0,
                             'text_paste': EMPTY_LINES})

    def test_parse_materias_aprobadas_good_lines(self):
        d = parse_materias_aprobadas(self.user, GOOD_LINES, self.remote_addr)

        self.assertEqual(len(d['materia_list']), 5)
        self.assertEqual(d['materia_list_count'], 5)
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
        d = parse_materias_aprobadas(self.user, BAD_LINES, self.remote_addr)
        self.assertEqual(d, {'materia_list': [],
                             'materia_list_count': 0,
                             'text_paste': BAD_LINES})

    def test_parse_materias_aprobadas_not_materia(self):
        d = parse_materias_aprobadas(self.user, NOT_MATERIA_LINES,
                                     self.remote_addr)
        self.assertEqual(d, {'materia_list': [],
                             'materia_list_count': 0,
                             'text_paste': NOT_MATERIA_LINES})

    def test_parse_materias_aprobadas_materia_aprobada(self):
        d = parse_materias_aprobadas(self.user, MATERIA_APROBADA_LINES,
                                     self.remote_addr)

        self.assertEqual(len(d['materia_list']), 1)
        self.assertEqual(d['materia_list_count'], 1)
        self.assertEqual(d['text_paste'], '')

        self.assertEqual(
            d['materia_list'][0],
            [Materia.objects.get(id='9503'), date(2012, 2, 23), '7'])
