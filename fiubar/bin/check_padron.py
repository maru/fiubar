# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("latin1")

import re
import fiubar
from django.utils.translation import ugettext as _

def check_padron(padron, first_name, last_name):
    return [ None, 'FOUND']
