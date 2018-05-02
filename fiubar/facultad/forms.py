# -*- coding: utf-8 -*-
from datetime import date

from django import forms
from django.utils.dates import MONTHS
from django.utils.translation import ugettext as _

from .models import PlanCarrera

from fiubar.alumnos.models import Materia as AlumnoMateria


class SelectCarreraForm(forms.Form):
    plancarrera = forms.ModelChoiceField(queryset=PlanCarrera.objects.all(),
                                         empty_label=None)
    cuatrimestre = forms.ChoiceField(choices=[
                                     (1, _('1° Cuatrimestre')),
                                     (2, _('2° Cuatrimestre'))])
    year = forms.ChoiceField(choices=[
                             (i, i) for i in
                             range(date.today().year, 1940, -1)])
    begin_date = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ['plancarrera', 'cuatrimestre', 'year']:
            self.fields[f].widget.attrs.update({'class': 'form-control'})

    def clean_begin_date(self):
        if 'cuatrimestre' not in self.cleaned_data or \
           'year' not in self.cleaned_data:
            raise forms.ValidationError(
                _('La fecha de ingreso a FIUBA es obligatoria'))
        month = 5 * int(self.cleaned_data['cuatrimestre']) - 2
        year = int(self.cleaned_data['year'])
        return date(year, month, 1)


class GraduadoForm(forms.Form):
    plancarrera = forms.CharField(widget=forms.HiddenInput)
    month = forms.ChoiceField(choices=MONTHS.items(), label=_('Month'))
    year = forms.ChoiceField(label=_('Year'),
                             choices=[(i, i) for i in
                             range(date.today().year, 1940, -1)])
    graduado_date = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ['month', 'year']:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['graduado_date']\
            .widget.attrs.update({'class': 'form-control'})

    def clean_graduado_date(self):
        if 'month' not in self.cleaned_data or \
           'year' not in self.cleaned_data:
            raise forms.ValidationError(
                _('La fecha de egreso de FIUBA es obligatoria'))
        month = int(self.cleaned_data['month'])
        year = int(self.cleaned_data['year'])
        return date(year, month, 1)


class CursadaForm(forms.Form):
    CURSADA_CHOICES = (
        ('-', _('No estoy cursando esta materia')),
        ('C', _('Cursando')),
        ('F', _('Cursada Aprobada')),
        ('A', _('Materia Aprobada')),
        ('E', _('Equivalencia')),
    )

    CUAT_CURSADA = (
        ('', _('Cuatrimestre')),
        ('1', _('1° Cuatrimestre')),
        ('2', _('2° Cuatrimestre')),
        ('V', _('Curso de Verano')),
    )

    CUAT_APROBADA = (
        ('', _('Cuatrimestre')),
        ('1', _('1° Cuatrimestre')),
        ('2', _('2° Cuatrimestre')),
    )

    YEAR_CHOICES = [('0', _('Año'))] + \
                   [(year, year) for year in
                    range(date.today().year, 1940, -1)]

    state = forms.ChoiceField(initial='-', widget=forms.RadioSelect(),
                              label=_('Estado'), choices=CURSADA_CHOICES)

    # Cuatrimestre en el que cursó la materia
    cursada_cuat = forms.ChoiceField(label='', choices=CUAT_CURSADA,
                                     required=False)
    cursada_year = forms.ChoiceField(label='', choices=YEAR_CHOICES,
                                     required=False)
    cursada_date = forms.CharField(widget=forms.HiddenInput, required=False)
    materia_curso = forms.ChoiceField(choices=[('-', '-')], required=False)

    # Cuatrimestre en el que aprobó la materia
    aprobada_cuat = forms.ChoiceField(label='', choices=CUAT_CURSADA,
                                      required=False)
    aprobada_year = forms.ChoiceField(label='', choices=YEAR_CHOICES,
                                      required=False)
    aprobada_date = forms.CharField(widget=forms.HiddenInput, required=False)
    # aprobada_same = forms.BooleanField(label='Mismo cuatrimestre que cursada.') # noqa

    NOTA_CHOICES = [('0', '----')] + \
                   [(nota, nota) for nota in range(10, 3, -1)] + [(2, 2)]
    nota = forms.ChoiceField(required=False, choices=NOTA_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ['cursada_cuat', 'cursada_year', 'aprobada_cuat',
                  'aprobada_year', 'nota']:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['state'].widget.attrs.update({'class': 'list-unstyled'})

    def clean_cursada_date(self):
        return self._calculate_date('cursada')

    def clean_aprobada_date(self):
        return self._calculate_date('aprobada')

    def _calculate_date(self, field_prefix):
        if self.cleaned_data[field_prefix + '_cuat'] == '' or \
           self.cleaned_data[field_prefix + '_year'] == '0':
            if self.cleaned_data[field_prefix + '_cuat'] == '' and \
               self.cleaned_data[field_prefix + '_year'] == '0':
                # Not entered.
                return None
            # Just one field.
            raise forms.ValidationError(
                _('Completar con cuatrimestre y año.'))
        if not self.cleaned_data[field_prefix + '_date']:
            return None
        return self.cleaned_data[field_prefix + '_date']

    def save(self, user, materia):
        materia_cursada = AlumnoMateria.objects.get_or_none(user=user,
                                                            materia=materia)
        state = self.cleaned_data['state']
        if (state != '-' or materia_cursada):
            # No estoy cursando esta materia
            if state == '-':
                materia_cursada.delete()
            # Cursando
            else:
                if not materia_cursada:
                    materia_cursada = AlumnoMateria()
                materia_cursada.update(user, materia, self.cleaned_data)
                materia_cursada.save()
        return materia_cursada
