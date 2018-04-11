"""
Extra HTML Widget classes
"""

import datetime

from django.forms.widgets import Select, Widget
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


__all__ = ('SelectDateWidget',)

class SelectDateWidget(Widget):
    """
    A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    month_field = '%s_month'
    day_field = '%s_day'
    year_field = '%s_year'

    def __init__(self, attrs=None, days=None, months=None, years=None):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}

        if days:
            self.months = days
        else:
            self.days = range(1, 32)
            
        if months:
            self.months = months
        else:
            self.months = MONTHS.items()
            self.months.sort()
            
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)
    
    def render(self, name, value, attrs=None):
        try:
            value = datetime.date(*map(int, value.split('-')))
            year_val, month_val, day_val = value.year, value.month, value.day
        except (AttributeError, TypeError, ValueError):
            year_val = month_val = day_val = None

        output = []

        day_choices = [('', _('Day'))] + [(i, i) for i in self.days]
        select_html = Select(choices=day_choices).render(self.day_field % name, day_val)
        output.append(select_html)

        month_choices = [('', _('Month'))] + self.months
        select_html = Select(choices=month_choices).render(self.month_field % name, month_val)
        output.append(select_html)

        year_choices = [('', _('Year'))] + [(i, i) for i in self.years]
        select_html = Select(choices=year_choices).render(self.year_field % name, year_val)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def value_from_datadict(self, data, files, name):
        y, m, d = data.get(self.year_field % name), data.get(self.month_field % name), data.get(self.day_field % name)
        if y and m and d:
            return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)
