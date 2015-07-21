# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

#from about.forms import BugsForm, IdeasForm, ContactForm
#from about.models import Bug, Idea

dict_data = {}

def bugs(request):
    if request.method == 'POST':
        form = BugsForm(request.POST)
        if form.is_valid():
            Bug.objects.create(user=request.user,
                               subject=form.cleaned_data['subject'],
                               description=form.cleaned_data['description'],)

            # Send email
            _send_mail((u'Error - %s' % form.cleaned_data['subject']), \
                       form.cleaned_data['description'], request.user)

            if request.POST.get('xhr'):
                return HttpResponse(content='OK')
            dict_data['form'] = None
        else:
            if request.POST.get('xhr'):
                return HttpResponse(status=404)
            dict_data['form'] = form
    else:
        dict_data['form'] = BugsForm()
    return render_to_response('about/bugs_form.html', dict_data,
                              context_instance=RequestContext(request))

@login_required
def ideas(request):
    if request.method == 'POST':
        form = IdeasForm(request.POST)
        if form.is_valid():
            Idea.objects.create(user=request.user,
                               category=form.cleaned_data['category'],
                               subject=form.cleaned_data['subject'],
                               description=form.cleaned_data['description'],)
            # Send email
            subject = _(u'Sugerencia - ') + form.cleaned_data['subject'] + \
                      ' (' + Idea.IDEAS_CATEGORIES[int(form.cleaned_data['category'])][1] + ')'
            _send_mail(subject, form.cleaned_data['description'],    \
                       request.user, request.user.get_full_name(),   \
                       request.user.email)

            if request.POST.get('xhr'):
                return HttpResponse(content='OK')
            dict_data['form'] = None
        else:
            if request.POST.get('xhr'):
                return HttpResponse(status=404)
            dict_data['form'] = form
    else:
        dict_data['form'] = IdeasForm()
    return render_to_response('about/ideas_form.html',
                              dict_data,
                              context_instance=RequestContext(request))

def contact_form(request, subject=_(u'Contacto'),
                 description=_(u'Razón del contacto:'), page_title=_(u'Contacto')):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            _send_mail(subject, form.cleaned_data['description'], \
                       request.user, form.cleaned_data['name'],   \
                       form.cleaned_data['email'])
            form = None
    else:
        form = ContactForm()
        if request.user.is_authenticated():
            form.fields['name'].initial = request.user.get_full_name()
            form.fields['email'].initial = request.user.email

    if form:
        form.fields['description'].label = description
    dict_data['page_title'] = page_title
    dict_data['form'] = form
    return render_to_response('about/contact_form.html',
                              dict_data,
                              context_instance=RequestContext(request))

def participate_form(request):
    return contact_form(request, subject=_(u'¡Quiero participar!'), \
                        description=_(u'Contanos que te gustaría hacer:'),   \
                        page_title=_(u'¡Quiero participar!'))

def _send_mail(subject, message, user, name='Anonymous', email='no@email'):
    from django.core.mail import send_mail
    from django.conf import settings

    if user.is_authenticated():
        name += ' (%s)' % user.username
    from_email = '"%s" <%s>' % (name, email)
    subject = '[Fiubar] ' +  subject
    send_mail(subject, message, from_email, [a[1] for a in settings.MANAGERS])

