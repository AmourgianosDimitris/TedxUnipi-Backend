from django.db import models
from django.utils import timezone

# from tinymce import models as tinymce_models
from ckeditor.fields import RichTextField
from .models_extras import *


################# general ################
class Social(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)
    url = models.URLField(verbose_name='url')
    logo = models.CharField(verbose_name='Logo', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'socials'
        verbose_name = 'Social'
        verbose_name_plural = 'Socials'

    def __str__(self):
        admin_show = self.name
        return admin_show


class Team(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'teams'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    def __str__(self):
        admin_show = self.name
        return admin_show


class Role(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)
    team = models.ForeignKey(Team, verbose_name='Team', related_name='roles', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        admin_show = self.name
        return admin_show


class Partner(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)
    type = models.CharField(verbose_name='Type', max_length=8, choices=Partner_Choices, blank=True, null=True)
    logo_url = models.ImageField(verbose_name='Logo URL')
    brand_url = models.URLField(verbose_name='Brand URL')
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'partners'
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        admin_show = self.name
        return admin_show


class Member(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    email = models.EmailField(verbose_name='Email Address')
    slug = models.SlugField(verbose_name='Slug', max_length=9, unique=False, validators=[member_slug], default=default_year())
    description = models.CharField(verbose_name='Description', max_length=100, blank=True, null=True)
    photo_url = models.ImageField(verbose_name='Photo URL')
    team = models.ForeignKey(Team, verbose_name='Team', related_name='members', on_delete=models.CASCADE, blank=True, null=True, )
    role = models.ForeignKey(Role, verbose_name='Role', related_name='members', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'members'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        admin_show = self.name
        return admin_show


################# Events #################
class Event(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    slug = models.SlugField(verbose_name='Slug', max_length=8, unique=True, validators=[event_slug], default='')
    air_date = models.DateField(verbose_name='Air Date')
    published = models.BooleanField(verbose_name='Published', default=False)
    location = models.CharField(max_length=255)
    banner_url = models.ImageField(verbose_name='Banner URL', max_length=255, null=True)
    description = models.TextField(blank=True)
    form = models.BooleanField(verbose_name='Form', default=False)
    form_capacity = models.IntegerField(verbose_name='Form Capacity', default=0)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-air_date']

    def __str__(self):
        admin_show = self.name
        return admin_show


class EventPhoto(models.Model):
    event = models.ForeignKey(Event, verbose_name='Event', related_name='photos', on_delete=models.CASCADE)
    url = models.ImageField(verbose_name='URL', max_length=255)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'event_photos'
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'


class EventVideo(models.Model):
    event = models.ForeignKey(Event, verbose_name='Event', related_name='videos', on_delete=models.CASCADE)
    url = models.URLField(verbose_name='URL', max_length=255)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'event_videos'
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, verbose_name='Event', related_name='participants', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Name', max_length=255)
    air_date_time = models.DateTimeField(verbose_name='Air Date & Time', blank=True, null=True)
    occupation = models.CharField(verbose_name='Occupation', max_length=255)
    type = models.CharField(verbose_name='Type', max_length=20, choices=Participant_Type_Choices, default='Speaker')
    category = models.CharField(verbose_name='Category', max_length=20, choices=Participant_Category_Choices, default='Technology', blank=True, null=True)
    photo_url = models.ImageField(verbose_name='Photo URL', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    website_url = models.URLField(verbose_name='Website URL', blank=True, null=True)
    facebook_url = models.URLField(verbose_name='Facebook URL', blank=True, null=True)
    twitter_url = models.URLField(verbose_name='Twitter URL', blank=True, null=True)
    instagram_url = models.URLField(verbose_name='Instagram URL', blank=True, null=True)
    linkedin_url = models.URLField(verbose_name='LinkedIn URL', blank=True, null=True)
    youtube_url = models.URLField(verbose_name='Youtube URL', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'event_participants'
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        ordering = ['-air_date_time']

    def __str__(self):
        admin_show = self.name
        return admin_show


class EventWorkshop(models.Model):
    event = models.ForeignKey(Event, verbose_name='Event', related_name='workshops', on_delete=models.CASCADE, )
    name = models.CharField(verbose_name='Name', max_length=255)
    slug = models.SlugField(verbose_name='Slug', max_length=255, unique=True, default='')
    air_date_time = models.DateTimeField(verbose_name='Air Date & Time', blank=True, null=True)
    banner_url = models.ImageField(verbose_name='Banner URL', max_length=255, blank=True)
    description = models.TextField(verbose_name='Description', blank=True)
    website_url = models.URLField(verbose_name='Website URL', blank=True, null=True)
    facebook_url = models.URLField(verbose_name='Facebook URL', blank=True, null=True)
    twitter_url = models.URLField(verbose_name='Twitter URL', blank=True, null=True)
    instagram_url = models.URLField(verbose_name='Instagram URL', blank=True, null=True)
    linkedin_url = models.URLField(verbose_name='LinkedIn URL', blank=True, null=True)
    youtube_url = models.URLField(verbose_name='Youtube URL', blank=True, null=True)
    form = models.BooleanField(verbose_name='Form', default=False)
    form_capacity = models.IntegerField(verbose_name='Form Capacity', default=0)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'event_workshops'
        verbose_name = 'Workshop'
        verbose_name_plural = 'Workshops'
        ordering = ['-air_date_time']

    def __str__(self):
        admin_show = self.name
        return admin_show


################# Forms ##################
class EventAnswer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="Event")
    firstname = models.CharField(verbose_name='First Name', max_length=255)
    lastname = models.CharField(verbose_name='Last Name', max_length=255)
    email = models.EmailField(verbose_name='Email Address')
    country = models.CharField(max_length=255, choices=Country_Choices, default='GR')
    address = models.CharField(verbose_name='Address', max_length=255)
    city = models.CharField(verbose_name='City', max_length=255)
    region = models.CharField(verbose_name='Region', max_length=255)
    zip_code = models.IntegerField(verbose_name='ZIP Code')
    phone = models.CharField(verbose_name='Phone', max_length=25)
    notes = models.TextField(verbose_name='Notes', blank=True, null=True)
    consent = models.BooleanField(verbose_name='Data processing consent given', default=False)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'event_answers'
        verbose_name = 'Event Answer'
        verbose_name_plural = 'Event Answers'
        ordering = ['event']
        unique_together = ('event', 'email')

    def __str__(self):
        admin_show = f'{self.firstname} {self.lastname} ({self.email})'
        return admin_show


class EventWorkshopAnswer(models.Model):
    workshop = models.ForeignKey(EventWorkshop, on_delete=models.CASCADE, related_name="Workshop")
    firstname = models.CharField(verbose_name='First Name', max_length=255)
    lastname = models.CharField(verbose_name='Last Name', max_length=255)
    email = models.EmailField(verbose_name='Email Address')
    consent = models.BooleanField(verbose_name='Data processing consent given', default=False)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'event_workshops_answers'
        verbose_name = 'Workshop Answer'
        verbose_name_plural = 'Workshop Answers'
        ordering = ['-workshop']
        unique_together = ('workshop', 'email',)

    def __str__(self):
        admin_show = f'{self.firstname} {self.lastname} ({self.email})'
        return admin_show

#################### Blog #########################
class Blog(models.Model):
    title = models.CharField(verbose_name='Title', max_length=200, unique=True)
    slug = models.SlugField(verbose_name='Slug', max_length=200, unique=True)
    banner = models.URLField(verbose_name='Banner', max_length = 255, null=True)
    article = RichTextField(verbose_name='Article')
    category = models.CharField(verbose_name='Category', max_length=13, choices=Blog_Choices, default='Technology', blank=False, null=False)
    likes = models.IntegerField(verbose_name='Likes', default=0)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'Blogs'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'
        ordering = ['-created_at']

    def __str__(self):
        admin_show = self.title
        return admin_show

#################### Contact Form #########################
class ContactForm(models.Model):
    firstname = models.CharField(verbose_name='First Name', max_length=255)
    lastname = models.CharField(verbose_name='Last Name', max_length=255)
    email = models.EmailField(verbose_name='Email Address')
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'contact_form'
        verbose_name = 'Contact Form'
        ordering = ['created_at']

    def __str__(self):
        admin_show = f'{self.firstname} {self.lastname} ({self.email})'
        return admin_show

#################### Guess The Theme #########################
class GuessTheTheme(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="EventTheme")
    firstname = models.CharField(verbose_name='First Name', max_length=255)
    lastname = models.CharField(verbose_name='Last Name', max_length=255)
    email = models.EmailField(verbose_name='Email Address')
    theme = models.TextField(verbose_name='Theme', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Creation Date', default=timezone.now)

    class Meta:
        db_table = 'guess_the_theme'
        verbose_name = 'Guess the Theme'
        ordering = ['event', 'created_at']

    def __str__(self):
        admin_show = f'{self.firstname} {self.lastname} ({self.email})'
        return admin_show
