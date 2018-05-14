import logging
from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from ..models import Alumno, AlumnoMateria, Materia, PlanMateria
from .common import BaseUserTestCase


logging.disable(logging.CRITICAL)


class HomePageViewTestCase(BaseUserTestCase):

    def test_home(self):
        response = self.client.get(reverse('facultad:home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Plan 2012')
        self.assertContains(response,
                            '<a href="/facultad/materias/cocky_perlman00/?'
                            'show=todas" class="fiuba-minilogo"><span>cocky_'
                            'perlman</span><br />')
        self.assertContains(response,
                            '<span class="small">Namlrep Ykcoc</span><br />')
        self.assertContains(response,
                            '<span class="small">Plan 2000</span></a></li>')
        self.assertContains(response,
                            '<a class="" href="/facultad/materia/9501/"')
        self.assertContains(response, '95.01')
        self.assertContains(response, 'sleepy_pani')

    def test_home_no_carrera(self):
        self.user = self.make_user('user2')

        self.client.force_login(self.user)
        assert self.user.is_authenticated

        response = self.client.get(reverse('facultad:home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response,
                            '<span>No estás cursando ninguna materia.</span>')
        self.assertContains(response,
                            '<a href="/facultad/carreras/add/">'
                            '¿Qué carrera cursás?</a>')


class PlanCarreraViewTestCase(BaseUserTestCase):

    def test_plancarrera(self):
        response = self.client.get(reverse('facultad:materias-carrera',
                                           args=['cocky_perlman12']))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response,
                            '<a href="/facultad/materia/9501/">\n'
                            '					95.01\n'
                            '					sleepy_pani\n'
                            '				</a>\n'
                            '			</td>\n'
                            '			<td>\n'
                            '			  <span class="small">Cursando</span>')

    def test_plancarrera_cursando(self):
        response = self.client.get(reverse('facultad:materias-carrera',
                                           args=['cocky_perlman12']) +
                                   '?show=cursando')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response,
                            '<a href="/facultad/materia/9501/">\n'
                            '					95.01\n'
                            '					sleepy_pani\n'
                            '				</a>\n'
                            '			</td>\n'
                            '			<td>\n'
                            '			  <span class="small">Cursando</span>')

    def test_plancarrera_para_cursar(self):
        response = self.client.get(reverse('facultad:materias-carrera',
                                           args=['cocky_perlman12']) +
                                   '?show=para_cursar')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response,
                            '<tr class="paracursar">\n'
                            '			<td class="icono">\n'
                            '				<img src="/static/images/facultad/materia_cursar.png"' # noqa
                            ' alt="" title="Disponible para cursar" />\n'
                            '			</td>\n'
                            '			<td class="margin-left">\n'
                            '				<a name="02"></a>\n'
                            '				<a href="/facultad/materia/9502/">\n'
                            '					95.02\n'
                            '					nostalgic_bell\n'
                            '				</a>')

    def test_plancarrera_faltan_correl(self):
        response = self.client.get(reverse('facultad:materias-carrera',
                                           args=['cocky_perlman12']) +
                                   '?show=faltan_correl')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response,
                            '<tr class="paracursar">\n'
                            '			<td class="icono">\n'
                            '				<img src="/static/images/facultad/materia_cursar.png"' # noqa
                            ' alt="" title="Disponible para cursar" />\n'
                            '			</td>\n'
                            '			<td class="margin-left">\n'
                            '				<a name="02"></a>\n'
                            '				<a href="/facultad/materia/9502/">\n'
                            '					95.02\n'
                            '					nostalgic_bell\n'
                            '				</a>')

    def test_plancarrera_aprobadas(self):
        response = self.client.get(reverse('facultad:materias-carrera',
                                           args=['cocky_perlman12']) +
                                   '?show=aprobadas')
        self.assertEqual(response.status_code, 200)

    def test_plancarrera_todas(self):
        response = self.client.get(reverse('facultad:materias-carrera',
                                           args=['cocky_perlman12']) +
                                   '?show=todas')
        self.assertEqual(response.status_code, 200)

    def test_plancarrera_404(self):
        response = self.client.get(reverse('facultad:materias-carrera',
                                           args=['cocky_perlman12']) +
                                   '?show=bad')
        self.assertEqual(response.status_code, 404)


class MateriaViewTestCase(BaseUserTestCase):

    def test_materia_cursando_check(self):
        response = self.client.get(reverse('facultad:materia', args=['9501']))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'C')

    def test_materia_cursando(self):
        response = self.client.get(reverse('facultad:materia', args=['9502']))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.02 '
                                      'nostalgic_bell</h3>')

        form = response.context['form']
        self.assertIsNone(form.initial.get('state'))

        response = self.client.post(
            reverse('facultad:materia', args=['9502']),
            {'state': 'C', 'cursada_cuat': '1', 'cursada_year': '2015'},
            follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.02 '
                                      'nostalgic_bell</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'C')
        self.assertEqual(form.initial['cursada_cuat'], '1')
        self.assertEqual(form.initial['cursada_year'], '2015')

    def test_materia_cursada_aprobada(self):
        response = self.client.post(
            reverse('facultad:materia', args=['9501']),
            {'state': 'F', 'cursada_cuat': '1', 'cursada_year': '2015'},
            follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'F')
        self.assertEqual(form.initial['cursada_cuat'], '1')
        self.assertEqual(form.initial['cursada_year'], '2015')

        # Check GET
        response = self.client.get(reverse('facultad:materia', args=['9501']))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'F')
        self.assertEqual(form.initial['cursada_cuat'], '1')
        self.assertEqual(form.initial['cursada_year'], '2015')

    def test_materia_aprobada(self):
        response = self.client.post(
            reverse('facultad:materia', args=['9501']),
            {'state': 'A', 'cursada_cuat': '1', 'cursada_year': '2015',
             'nota': '8', 'aprobada_cuat': '2', 'aprobada_year': '2016'},
            follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'A')
        self.assertEqual(form.initial['cursada_cuat'], '1')
        self.assertEqual(form.initial['cursada_year'], '2015')
        self.assertEqual(form.initial['aprobada_cuat'], '2')
        self.assertEqual(form.initial['aprobada_year'], '2016')
        self.assertEqual(form.initial['nota'], 8)

        # Check GET
        response = self.client.get(reverse('facultad:materia', args=['9501']))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'A')
        self.assertEqual(form.initial['cursada_cuat'], '1')
        self.assertEqual(form.initial['cursada_year'], '2015')
        self.assertEqual(form.initial['aprobada_cuat'], '2')
        self.assertEqual(form.initial['aprobada_year'], '2016')
        self.assertEqual(form.initial['nota'], 8)

    def test_materia_equivalencia(self):
        response = self.client.post(
            reverse('facultad:materia', args=['9501']),
            {'state': 'E'},
            follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')
        # <div class="alert alert-success fade in">
        #     <a href="#" class="close" data-dismiss="alert"
        # aria-label="close">&times;</a>
        #     Cambios guardados.
        #   </div>
        #

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'E')

        # Check GET
        response = self.client.get(reverse('facultad:materia', args=['9501']))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'E')
        self.assertIsNone(form.initial.get('cursada_cuat'))

    def test_materia_cursada_aprobada_bad(self):
        response = self.client.post(
            reverse('facultad:materia', args=['9501']),
            {'state': 'F', 'cursada_cuat': '1'},
            follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'C')
        self.assertIsNone(form.initial.get('cursada_cuat'))
        self.assertEqual(form.data['state'], 'F')
        self.assertEqual(form.data['cursada_cuat'], '1')

        # Check GET
        response = self.client.get(reverse('facultad:materia', args=['9501']))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'C')
        self.assertIsNone(form.initial.get('cursada_cuat'))

    def test_materia_cursada_aprobada_date(self):
        response = self.client.post(
            reverse('facultad:materia', args=['9501']),
            {'state': 'F', 'cursada_cuat': '1', 'cursada_year': '2015',
             'cursada_date': '2015-03-01'},
            follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'F')
        self.assertEqual(form.initial['cursada_cuat'], '1')
        self.assertEqual(form.initial['cursada_year'], '2015')

        # Check GET
        response = self.client.get(reverse('facultad:materia', args=['9501']))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertEqual(form.initial['state'], 'F')
        self.assertEqual(form.initial['cursada_cuat'], '1')
        self.assertEqual(form.initial['cursada_year'], '2015')

    def test_materia_delete(self):
        response = self.client.post(
            reverse('facultad:materia', args=['9501']),
            {'state': '-'},
            follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertIsNone(form.initial.get('state'))
        self.assertIsNone(form.initial.get('cursada_cuat'))
        self.assertIsNone(form.initial.get('cursada_year'))

        # Check GET
        response = self.client.get(reverse('facultad:materia', args=['9501']))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3 class="panel-title">95.01 '
                                      'sleepy_pani</h3>')

        form = response.context['form']
        self.assertIsNone(form.initial.get('state'))
        self.assertIsNone(form.initial.get('cursada_cuat'))
        self.assertIsNone(form.initial.get('cursada_year'))

        m = Materia.objects.get(id='9501')
        with self.assertRaises(ObjectDoesNotExist):
            AlumnoMateria.objects.get(user=self.user, materia=m)


class CargarMateriasViewTestCase(BaseUserTestCase):

    def test_cargar_materias_get(self):
        response = self.client.get(reverse('facultad:cargar-materias'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context.get('text_paste'), '')
        self.assertEqual(response.context.get('materia_list'), '')
        self.assertEqual(response.context.get('materia_list_count'), 0)

    def test_cargar_materias_post_good_lines(self):
        from .test_views_sist_acad import GOOD_LINES

        creditos = Alumno.objects.filter(user=self.user).\
            order_by('plancarrera')

        response = self.client.post(reverse('facultad:cargar-materias'),
                                    {'text_paste': GOOD_LINES})
        self.assertEqual(response.status_code, 200)

        d = response.context
        self.assertEqual(d['text_paste'], '')
        self.assertEqual(d['materia_list_count'], 5)
        self.assertEqual(len(d['materia_list']), 5)

        for m in d['materia_list']:
            plan_materias = PlanMateria.objects.filter(materia=m[0])
            for pm in plan_materias:
                pc = pm.plancarrera
                try:
                    c = creditos.get(plancarrera=pc)
                    c.creditos += pm.creditos
                except ObjectDoesNotExist:
                    pass

        alumnos = Alumno.objects.filter(user=self.user).order_by('plancarrera')
        for i in range(len(creditos)):
            self.assertEqual(creditos[i].get_creditos(),
                             alumnos[i].get_creditos())

    def test_cargar_materias_post_empty_lines(self):
        from .test_views_sist_acad import EMPTY_LINES
        response = self.client.post(reverse('facultad:cargar-materias'),
                                    {'text_paste': EMPTY_LINES})
        self.assertEqual(response.status_code, 200)

        d = response.context
        self.assertEqual(d['text_paste'], EMPTY_LINES)
        self.assertEqual(d['materia_list_count'], 0)
        self.assertEqual(d['materia_list'], [])

    def test_cargar_materias_post_bad_lines(self):
        from .test_views_sist_acad import BAD_LINES
        response = self.client.post(reverse('facultad:cargar-materias'),
                                    {'text_paste': BAD_LINES})
        self.assertEqual(response.status_code, 200)

        d = response.context
        self.assertEqual(d['text_paste'], BAD_LINES)
        self.assertEqual(d['materia_list_count'], 0)
        self.assertEqual(d['materia_list'], [])

    def test_cargar_materias_post_line_not_materia(self):
        from .test_views_sist_acad import NOT_MATERIA_LINES
        response = self.client.post(reverse('facultad:cargar-materias'),
                                    {'text_paste': NOT_MATERIA_LINES})
        self.assertEqual(response.status_code, 200)

        d = response.context
        self.assertEqual(d['text_paste'], NOT_MATERIA_LINES)
        self.assertEqual(d['materia_list_count'], 0)
        self.assertEqual(d['materia_list'], [])

    def test_cargar_materias_post_materias_aprobadas(self):
        from .test_views_sist_acad import MATERIA_APROBADA_LINES
        response = self.client.post(reverse('facultad:cargar-materias'),
                                    {'text_paste': MATERIA_APROBADA_LINES})
        self.assertEqual(response.status_code, 200)

        d = response.context
        self.assertEqual(d['text_paste'], '')
        self.assertEqual(d['materia_list_count'], 1)
        self.assertEqual(len(d['materia_list']), 1)

        self.assertEqual(
            d['materia_list'][0],
            [Materia.objects.get(id='9503'), date(2012, 2, 23), '7'])
