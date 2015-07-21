# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.generic import list_detail
from django.contrib.auth.models import User
from profiles.forms import ProfileForm, UploadPhotoForm, LinkSocialNetworkForm, LinkInstantMessengerForm, LinkWebsiteForm
from profiles.models import Profile, Photo, LinkInstantMessenger, LinkSocialNetwork, LinkWebsite
from openmate.core.log import logger

dict_data = {}
RESULTS_PER_PAGE = 10

@login_required
def show(request, username=None):
    # Get user
    try:
        if username:
            user = User.objects.get(username__iexact=username, is_active=True)
            if user.username != username:
                return HttpResponseRedirect(reverse('member-profile_show', args=[user.username]))
        else:
            user = request.user
    except User.DoesNotExist:
        raise Http404
    # Get profile and other info
    dict_data['member'] = user
    dict_data['profile'], created = Profile.objects.get_or_create(user=user)
    dict_data['sn_list'] = user.linksocialnetwork_set.all()
    dict_data['im_list'] = user.linkinstantmessenger_set.all()
    dict_data['w_list'] = user.linkwebsite_set.all()
    try:
        from groups.models import Member
        dict_data['group_list'] = Member.objects.filter(user=user).order_by('?')[0:20]
    except:
    	pass
    dict_data['carrera_list'] = dict_data['profile'].get_carrera()
    return render_to_response('profiles/show_profile.html', dict_data,
                              context_instance=RequestContext(request))

@login_required
def edit(request):
    """
    Edits profile data.
    """
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save(profile)
            logger.info("%s - profile-edit: user '%s', form %s" % (request.META.get('REMOTE_ADDR'), request.user, form.cleaned_data))
            request.user.message_set.create(message=_('Profile updated.'))
            return HttpResponseRedirect(reverse('profile-show'))
    form = ProfileForm(profile.get_init_data())
    dict_data['form'] = form
    return render_to_response('profiles/edit_form.html', dict_data,
                              context_instance=RequestContext(request))

@login_required
def photo_edit(request):
    # Upload a new photo
    if request.FILES:
        form = UploadPhotoForm(request.POST, request.FILES)  
        if form.is_valid() and request.FILES.has_key('avatar'):
            if Photo.objects.upload_file(request.user, request.FILES['avatar']):
                request.user.message_set.create(message=_('Photo updated.'))
            else:
                request.user.message_set.create(message=_('Ocurrió un error.'))
            logger.info("%s - profile-photo_edit: user '%s', form %s" % (request.META.get('REMOTE_ADDR'), request.user, form.cleaned_data))
    else:
        form = UploadPhotoForm()
    profile = Profile.objects.get(user=request.user)
    photo_list = Photo.objects.filter(user=request.user).order_by('id')
    dict_data.update({ 'form' : form, 'profile' : profile, 'photo_list' : photo_list })
    return render_to_response('profiles/photo_form.html', dict_data,
                              context_instance=RequestContext(request))
        
@login_required
def photo_delete(request, id):
    try:
        Photo.objects.delete_photo(id, request.user)
        request.user.message_set.create(message=_('Photo deleted.'))
        return HttpResponseRedirect(reverse('profile-photo_edit'))
    except:
        raise Http404

@login_required
def photo_set_main(request, id):
    try:
        photo = Photo.objects.get(id=id, user=request.user)
        profile = Profile.objects.get(user=request.user)
        profile.photo = photo
        profile.save()
        request.user.message_set.create(message=_('Foto seleccionada.'))
        return HttpResponseRedirect(reverse('profile-photo_edit'))
    except:
        raise Http404

@login_required
def links(request, callback=None):
    if request.method == 'POST':
        form_name = request.POST.get('form_name', '')
        if form_name == 'sn_form':
            form = LinkSocialNetworkForm(request.POST)
        elif form_name == 'im_form':
            form = LinkInstantMessengerForm(request.POST)
        elif form_name == 'w_form':
            form = LinkWebsiteForm(request.POST)
        else:
            form = None
        if form and form.is_valid():
            logger.info("%s - profile-links: user '%s', form %s" % (request.META.get('REMOTE_ADDR'), request.user, form.cleaned_data))
            form.save(request.user)
            request.user.message_set.create(message=_('Profile added.'))
            
    dict_data.update({ 'sn_form' : LinkSocialNetworkForm(), 
        'im_form' : LinkInstantMessengerForm(), 'w_form' : LinkWebsiteForm(), 
    })
    return render_to_response('profiles/links_form.html', dict_data, 
                              context_instance=RequestContext(request))
    
@login_required
def links_delete(request, type, id):
    """
    Deletes profile links.
    """
    try:
        if type == 'sn':
            link = LinkSocialNetwork.objects.get(user=request.user, id=id)
        elif type == 'im':
            link = LinkInstantMessenger.objects.get(user=request.user, id=id)
        elif type == 'w':
            link = LinkWebsite.objects.get(user=request.user, id=id)
        link.delete()
        request.user.message_set.create(message=_('Perfil borrado.'))
    except:
        request.user.message_set.create(message=_('Perfil no encontrado.'))
    return HttpResponseRedirect(reverse('profile-links'))
    
@login_required
def notifications(request):
    return render_to_response('profiles/notifications_form.html',
                            context_instance=RequestContext(request))
@login_required
def list_users(request):
    """Lists users"""
    page = request.GET.get('p', 1)
    return list_detail.object_list(
      request,
      queryset = Profile.objects.get_all_users(),
      paginate_by = RESULTS_PER_PAGE,
      page = page,
      extra_context = { 'object' : _(u'user') },
    )

@login_required
def search(request):
    dict_data = {}
    page = int(request.GET.get('p', 1))
    search_query = request.GET.get('q', None)
    if request.GET.has_key('q'):
        if len(search_query) > 1:
            # Set query set
            query_set = Profile.objects.search(search_query)
            query_string = '&q=' + search_query
            # Calculate begin-end page results
            num_results = query_set.count()
            search_begin = (page - 1)*RESULTS_PER_PAGE + 1
            if page*RESULTS_PER_PAGE < num_results:
                search_end = page*RESULTS_PER_PAGE
            else:
                search_end = num_results
            dict_data.update({ 'num_results' : num_results, 
                'search_begin' : search_begin, 'search_end' : search_end,
                'search_query' : search_query, 'query_string' : query_string, 
                'object' : _(u'user')
            })
            return list_detail.object_list(
              request,
              queryset = query_set,
              paginate_by = RESULTS_PER_PAGE,
              page = page,
              extra_context = dict_data,
              template_name = 'profiles/search_users.html',
            )
        else:
            dict_data.update({ 'form_errors' : _(u'Ingresar al menos dos caracteres.'),
                'search_query' : search_query,
            })
    else:
        dict_data['form_errors'] = None
    return render_to_response('profiles/search_users.html', dict_data,
                            context_instance=RequestContext(request))
