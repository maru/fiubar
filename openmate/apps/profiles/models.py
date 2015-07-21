# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _ 
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime, dateutil.relativedelta as relativedelta
from openmate.core.image import rescale_upload
import md5, os

class ProfileManager(models.Manager):

    def create_profile(self, user):
    	""" Create profile if user doesn't have one!"""
        if self.filter(user=user).count() == 0:
            p = self.create(user=user)
        else:
            p = self.get(user=user)
        return p
        
    def get_last(self, last, last_login=None):
        """Get last profiles ordered by date updated"""
        list = self.get_all_users().order_by('-user__date_joined')
        if last_login:
            list = list.filter(user__date_joined__gte=last_login)
        return list[:last]
        
    def get_all_users(self):
        user_list = self.exclude(user__is_superuser=True)\
                        .exclude(user__is_active=False)\
                        .order_by('-user__id')
        return user_list
        
    def search(self, query):
        user_list = self.get_all_users()
        search_list = self.none()
        for q in query.split():
            u_list = user_list.filter(user__username__icontains=q)
            f_list = user_list.filter(user__first_name__icontains=q)
            l_list = user_list.filter(user__last_name__icontains=q)
            search_list = search_list | u_list | f_list | l_list
        return search_list
        
class Profile(models.Model):

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )

    user = models.ForeignKey(User, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    photo = models.ForeignKey('Photo', null=True, blank=True, related_name='main_photo')
    date_updated = models.DateTimeField(auto_now=True)
    
    objects = ProfileManager()
    
    def __unicode__(self):
        return self.user.__unicode__()

    def age(self):
        TODAY = datetime.date.today()
        return _(u'%s años') % relativedelta.relativedelta(TODAY, self.birthdate).years
    
    def adjetive_gender(self):
        if self.gender == 'M':
            return _('o')
        elif self.gender == 'F':
            return _('a')
        return _('o/a')
    
    def gender_icon(self):
        if self.gender == 'M':
            return 'male.png'
        if self.gender == 'F':
            return 'female.png'
        return ''
        
    def get_nickname(self):
        if self.nickname and len(self.nickname) > 0:
            return self.nickname
        elif len(self.user.get_full_name()) > 0:
            return self.user.get_full_name()
        return self.user.username

    def url_profile(self):
        return '/user/%s/' % self.user.username
    
    def get_full_name(self):
        return self.user.get_full_name()
        
    def date_joined(self):
        return self.user.date_joined
        
    def get_carrera(self):
        try:
            return self.user.alumno_set.order_by('carrera')
        except:
            return None
        
    def get_init_data(self):
        """
        Returns a dictionary with the initial data for a ProfileForm.
        """
        init_data = { 'email' : self.user.email, 'nickname' : self.nickname,
            'gender' : self.gender, 'location' : self.location,
            'interests' : self.interests, 'username' : self.user.username,
        }
        if self.birthdate:
            init_data.update({'birthdate_day' : self.birthdate.day,
                'birthdate_month' : self.birthdate.month, 'birthdate_year' : self.birthdate.year, 
            })                
        return init_data
    
    def is_empty(self):
        return (self.nickname == '' or self.gender == '' or self.location == '' 
             or self.interests == '' or self.birthdate == '')
        
    class Meta:
        verbose_name = 'Profile'
        ordering = ['-user__date_joined']
        
    class Admin(admin.ModelAdmin):
        list_display = ('user', 'gender', 'nickname', 'birthdate', 'location', 'interests', 'date_updated')        
        list_filter = ['gender', 'location']
        search_fields = ['nickname', 'location', 'interests']
admin.site.register(Profile, Profile.Admin)  
      
class PhotoManager(models.Manager):
    
    def upload_file(self, user, picture):
        # Get picture md5
        picture.open()
        md5sum = md5.new(picture.read()).hexdigest()

        # Build path
        username = user.username
        path = self.build_photo_path(username, md5sum)

        # Create images
        for size in [ 's', 'm', 'l' ]:
            picture.open()
            rescale_upload(picture.read(), path % size, Photo.AVATAR_SIZE[size])

        for size in [ 'xs', 's' ]:
            picture.open()
            rescale_upload(picture.read(), path % ('box_' + size), Photo.AVATAR_SIZE[size], canvas='box')
            
        # Save photo
        photo = Photo.objects.create(user=user, avatar=picture, md5sum=md5sum)
        profile = Profile.objects.get(user=user)
        profile.photo = photo
        profile.save()
        return photo
        
    def build_photo_path(self, username, md5sum):
        path = '%s/%s' % (settings.AVATARS_USERS_DIR, username[0])
        if not os.path.exists(path):
            os.mkdir(path)
        path = '%s/%s' % (path, username[1])
        if not os.path.exists(path):
            os.mkdir(path)
        path = '%s/%s' % (path, username)
        if not os.path.exists(path):
            os.mkdir(path)
        path = '%s/%s_%%s.jpg' % (path, md5sum)
        return path 
        
    def delete_photo(self, id, user):
        try:
            photo = self.get(id=id, user=user)
            # Delete profile photo, if it's the main one.
            profile = user.profile_set.all()[0]
            if profile.photo == photo:
                profile.photo = None
                profile.save()
        except:
            import sys
            print sys.exc_info()
            raise Photo.DoesNotExist

        try:
            # Delete photo from filesystem and db
            path = self.build_photo_path(user.username, photo.md5sum)
            for size in [ 'box_xs', 'box_s', 's', 'm', 'l' ]:
                file_path = path % size
                os.unlink(file_path)
            photo.delete()
        except:
            pass

class Photo(models.Model):
    AVATAR_SIZE_L = 360, 360
    AVATAR_SIZE_M = 160, 160
    AVATAR_SIZE_S = 50, 50
    AVATAR_SIZE_XS = 24, 24
    
    AVATAR_SIZE = { 'xs' : AVATAR_SIZE_XS, 's' : AVATAR_SIZE_S, 
        'm' : AVATAR_SIZE_M, 'l' : AVATAR_SIZE_L,
    }
    
    user = models.ForeignKey(User)
    avatar = models.ImageField(upload_to='avatar/users/')  
    md5sum = models.CharField(max_length=32)
    upload_date = models.DateTimeField(auto_now_add=True)
        
    objects = PhotoManager()
    
    def __unicode__(self):
        return _('Profile Photo for %s' % self.user)

    def url_delete(self):
        return reverse('profile-photo_delete', args=[self.id])
    
    def url_set_main(self):
        return reverse('profile-photo_set_main', args=[self.id])
    
    def get_html_path(self, size='box_s'):
        username = self.user.username
        return '/media/avatars/users/%s/%s/%s/%s_%s.jpg' % \
                    (username[0], username[1], username, self.md5sum, size)
            
    class Meta:
        verbose_name = 'Photo'
        
    class Admin(admin.ModelAdmin):
        list_display = ('user', 'avatar')
        list_filter = ['avatar']
admin.site.register(Photo, Photo.Admin)        

class ServiceInstantMessengerManager(models.Manager):
    def choices(self):
        return [(im.slug, im.name) for im in self.all()]

class ServiceInstantMessenger(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    
    objects = ServiceInstantMessengerManager()
    
    def __unicode__(self):
        return self.slug
        
    class Meta:
        verbose_name = 'Service: Instant Messenger'
        ordering = ('name', 'slug')
        
    class Admin(admin.ModelAdmin):
        list_display = ('slug', 'name', 'active')
# admin.site.register(ServiceInstantMessenger, ServiceInstantMessenger.Admin)
    
class ServiceSocialNetworkManager(models.Manager):
    def choices(self):
        return [(web.slug, web.name) for web in self.all()]

class ServiceSocialNetwork(models.Model):
    slug = models.SlugField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    objects = ServiceSocialNetworkManager()
    
    def __unicode__(self):
        return self.slug
        
    class Meta:
        verbose_name = 'Service: Social Network'
        ordering = ('name', 'slug')
        
    class Admin(admin.ModelAdmin):
        list_display = ('slug', 'name', 'link', 'active')
# admin.site.register(ServiceSocialNetwork, ServiceSocialNetwork.Admin)

class LinkInstantMessenger(models.Model):
    user = models.ForeignKey(User)
    service = models.ForeignKey(ServiceInstantMessenger)
    account = models.CharField(max_length=200)

    def get_deletion_url(self):
        return reverse('profile-links_delete', args=['im', self.id])
        
    class Meta:
        verbose_name = 'Link: Instant Messenger'

    class Admin(admin.ModelAdmin):
        list_display = ('user', 'service', 'account')
admin.site.register(LinkInstantMessenger, LinkInstantMessenger.Admin)

class LinkSocialNetwork(models.Model):
    user = models.ForeignKey(User)
    service = models.ForeignKey(ServiceSocialNetwork)
    account = models.CharField(max_length=200)

    def get_account(self):
        return (self.service.link % self.account)
        
    def get_deletion_url(self):
        return reverse('profile-links_delete', args=['sn', self.id])
        
    class Meta:
        verbose_name = 'Link: Social Network'

    class Admin(admin.ModelAdmin):
        list_display = ('user', 'service', 'account')
admin.site.register(LinkSocialNetwork, LinkSocialNetwork.Admin)

class LinkWebsite(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)

    def get_deletion_url(self):
        return reverse('profile-links_delete', args=['w', self.id])
        
    class Meta:
        verbose_name = 'Link: Website'

    class Admin(admin.ModelAdmin):
        list_display = ('user', 'name', 'url')
admin.site.register(LinkWebsite, LinkWebsite.Admin)

#class Notification(models.Model):
#    # Notificarme por nuevos Mensajes Privados:     
#    pass

