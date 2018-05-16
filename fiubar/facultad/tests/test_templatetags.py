from django.template import Context, Template
from django.test import SimpleTestCase

from ..models import Alumno, PlanMateria
from .common import BaseUserTestCase


class GetCarrerasTagTest(BaseUserTestCase):

    TEMPLATE = Template("{% load facultad_tags %}{% get_carreras %}")

    def test_user_carreras(self):
        c = Context({'user': self.user})
        rendered = self.TEMPLATE.render(c)
        self.assertEqual(rendered, '')

        carreras = Alumno.objects.select_related('carrera')\
            .filter(user=self.user).order_by('plancarrera')

        context = c.dicts[1]
        self.assertCountEqual(context['list_carreras'], carreras)

    def test_user_no_carreras(self):
        user = self.make_user('user3')

        c = Context({'user': user})
        rendered = self.TEMPLATE.render(c)
        self.assertEqual(rendered, '')

        context = c.dicts[1]
        self.assertEqual(context['list_carreras'].count(), 0)


class DisplayRowMateriaTagTest(BaseUserTestCase):

    TEMPLATE = Template("{% load facultad_tags %}"
                        "{% display_row_materia planmateria %}")

    def test_show_cursar_futuro_todas(self):
        pm = self.plan_materias[5]
        lista_materias = PlanMateria.objects\
            .list_materias_para_cursar(self.user, pm.plancarrera)

        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'todas',
                     'lista_materias_a_cursar': lista_materias})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('6109', rendered)
        self.assertIn('materia_notyet.png', rendered)
        self.assertIn('61.09 Probabilidad', rendered)
        self.assertIn('<span id="materia-correlativas">\n'
                      '			    <span class="small chelp" title="61.03 - Algebra II">61.03</span> - \n' # noqa
                      '			    <span class="small chelp lt" title="61.08 - Analisis Matematico II">61.08</span>\n' # noqa
                      '			  </span>', rendered)

    def test_show_disponible_para_cursar(self):
        pm = self.plan_materias[4]
        lista_materias = PlanMateria.objects\
            .list_materias_para_cursar(self.user, pm.plancarrera)

        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'para_cursar',
                     'lista_materias_a_cursar': lista_materias})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('6103', rendered)
        self.assertIn('materia_cursar.png', rendered)
        self.assertIn('61.03 Algebra II', rendered)
        self.assertIn('<td><span id="materia-creditos">8</span></td>',
                      rendered)

    def test_show_disponible_todas(self):
        pm = self.plan_materias[4]
        lista_materias = PlanMateria.objects\
            .list_materias_para_cursar(self.user, pm.plancarrera)

        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'todas',
                     'lista_materias_a_cursar': lista_materias})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('6103', rendered)
        self.assertIn('materia_cursar.png', rendered)
        self.assertIn('61.03 Algebra II', rendered)
        self.assertIn('<span id="materia-correlativas">\n'
                      '			    <span class="small chelp lt" title="CBC">CBC</span>\n' # noqa
                      '			  </span>', rendered)

    def test_show_cursando_cursando(self):
        pm = self.plan_materias[2]
        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'cursando'})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('9503', rendered)
        self.assertIn('95.03 loving_perlman', rendered)
        self.assertIn('materia_c.png', rendered)
        self.assertIn('<span id="materia-falta_cuat" class="small">'
                      'Cursando</span>', rendered)

    def test_show_cursando_todas(self):
        pm = self.plan_materias[2]
        lista_materias = PlanMateria.objects\
            .list_materias_para_cursar(self.user, pm.plancarrera)

        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'todas',
                     'lista_materias_a_cursar': lista_materias})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('9503', rendered)
        self.assertIn('95.03 loving_perlman', rendered)
        self.assertIn('materia_c.png', rendered)
        self.assertIn('<span id="materia-falta_cuat">'
                      'Cursando</span>', rendered)

    def test_show_final_cursando(self):
        pm = self.plan_materias[1]
        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'cursando'})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('9502', rendered)
        self.assertIn('95.02 nostalgic_bell', rendered)
        self.assertIn('materia_f.png', rendered)
        self.assertIn('<span id="materia-falta_cuat" class="small">'
                      'Falta final</span>', rendered)

    def test_show_final_todas(self):
        pm = self.plan_materias[1]
        lista_materias = PlanMateria.objects\
            .list_materias_para_cursar(self.user, pm.plancarrera)

        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'todas',
                     'lista_materias_a_cursar': lista_materias})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('9502', rendered)
        self.assertIn('95.02 nostalgic_bell', rendered)
        self.assertIn('materia_f.png', rendered)
        self.assertIn('<span id="materia-falta_cuat">'
                      'Falta final</span>', rendered)
        self.assertIn('<span id="materia-correlativas">\n'
                      '			    <span class="small chelp lt" title="9501 - sleepy_pani">9501</span>\n' # noqa
                      '			  </span>', rendered)

    def test_show_aprobada_aprobadas(self):
        pm = self.plan_materias[0]
        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'aprobadas'})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('9501', rendered)
        self.assertIn('95.01 sleepy_pani', rendered)
        self.assertIn('materia_ap.png', rendered)
        self.assertIn('<span id="materia-fecha_aprobada">-</span>', rendered)
        self.assertIn('<span id="materia-nota">7 (siete)</span>', rendered)

    def test_show_aprobada_todas(self):
        pm = self.plan_materias[0]
        lista_materias = PlanMateria.objects\
            .list_materias_para_cursar(self.user, pm.plancarrera)

        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'todas',
                     'lista_materias_a_cursar': lista_materias})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('9501', rendered)
        self.assertIn('95.01 sleepy_pani', rendered)
        self.assertIn('materia_ap.png', rendered)
        self.assertIn('<span id="materia-falta_cuat">Aprobada</span>',
                      rendered)
        self.assertIn('<span id="materia-correlativas">\n'
                      '			  </span>', rendered)

    def test_show_equivalencia_aprobadas(self):
        pm = self.plan_materias[3]
        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'aprobadas'})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('6108', rendered)
        self.assertIn('61.08 Analisis Matematico II', rendered)
        self.assertIn('<tr class="final">', rendered)
        self.assertIn('materia_ap.png', rendered)
        self.assertIn('Equivalencia', rendered)
        self.assertIn('<span id="materia-fecha_aprobada">-</span>', rendered)
        self.assertIn('<span id="materia-nota">-</span>', rendered)

    def test_show_equivalencia_todas(self):
        pm = self.plan_materias[3]
        lista_materias = PlanMateria.objects\
            .list_materias_para_cursar(self.user, pm.plancarrera)

        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'todas',
                     'lista_materias_a_cursar': lista_materias})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('6108', rendered)
        self.assertIn('61.08 Analisis Matematico II', rendered)
        self.assertIn('<tr class="final">', rendered)
        self.assertIn('materia_ap.png', rendered)
        self.assertIn('<span id="materia-falta_cuat">Aprobada</span>',
                      rendered)

    def test_show_invalid_todas(self):
        pm = None
        c = Context({'user': self.user, 'planmateria': pm,
                     'tab_selected': 'todas'})
        rendered = self.TEMPLATE.render(c)

        self.assertIn('materia_notyet.png', rendered)


class ApnumberTagTest(SimpleTestCase):

    TEMPLATE = Template("{% load facultad_tags %}{{ nota|apnumber }}")

    def test_nota_valid(self):
        c = Context({'nota': 5})
        rendered = self.TEMPLATE.render(c)
        self.assertEqual(rendered, '5 (cinco)')

        c = Context({'nota': '10'})
        rendered = self.TEMPLATE.render(c)
        self.assertEqual(rendered, '10 (diez)')

    def test_nota_empty(self):
        c = Context({})
        rendered = self.TEMPLATE.render(c)
        self.assertEqual(rendered, '-')

    def test_nota_invalid(self):
        c = Context({'nota': 0})
        rendered = self.TEMPLATE.render(c)
        self.assertEqual(rendered, '-')

        c = Context({'nota': '20'})
        rendered = self.TEMPLATE.render(c)
        self.assertEqual(rendered, '-')

        c = Context({'nota': 'ocho'})
        rendered = self.TEMPLATE.render(c)
        self.assertEqual(rendered, '-')
