from csvexport.actions import csvexport
from django.contrib import admin

from .models import *

admin.site.site_header = 'TEDxUniversityofPiraeus Admin'
admin.site.site_title = "TEDxUniversityofPiraeus - Admin Site"
admin.site.index_title = "TEDxUniversityofPiraeus - Site administration"


class SocialAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    ordering = ('name',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


class RoleAdmin(admin.ModelAdmin):
    list_filter = ('team',)
    list_display = ('name', 'team')
    ordering = ('name',)


class PartnerAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('name', 'brand_url', 'type',)
    ordering = ('name',)


class MemberAdmin(admin.ModelAdmin):
    list_filter = ('team', 'role',)
    list_display = ('name', 'email', 'team', 'role')
    fields = ('name', 'email', 'slug', 'description', 'photo_url', 'team', 'role',)
    ordering = ('name',)


################# Events #################

class PhotoInline(admin.TabularInline):
    model = EventPhoto
    extra = 0


class VideoInline(admin.TabularInline):
    model = EventVideo
    extra = 0


class ParticipantInline(admin.StackedInline):
    model = EventParticipant
    extra = 0


class WorkshopInline(admin.StackedInline):
    model = EventWorkshop
    extra = 0


def activate_forms(modeladmin, request, queryset):
    queryset.update(form=True)


activate_forms.short_description = 'Set Forms as active on selected entries'


def inactivate_forms(modeladmin, request, queryset):
    queryset.update(form=False)


inactivate_forms.short_description = 'Set Forms as inactive on selected entries'


class EventAdmin(admin.ModelAdmin):
    list_filter = ('published', 'form', 'air_date', 'location')
    list_display = ('name', 'slug', 'air_date', 'location', 'published', 'form',)
    inlines = [PhotoInline, VideoInline, ParticipantInline, WorkshopInline]
    actions = [activate_forms, inactivate_forms]


class EventPhotoAdmin(admin.ModelAdmin):
    list_filter = ('event',)
    list_display = ('event', 'url')
    ordering = ('event',)


class EventVideoAdmin(admin.ModelAdmin):
    list_filter = ('event',)
    list_display = ('event', 'url')
    ordering = ('event',)


class EventParticipantAdmin(admin.ModelAdmin):
    list_filter = ('type', 'category')
    list_display = ('event', 'name', 'air_date_time')
    ordering = ('event', 'name',)


#
# @admin.action(description='Set forms as active')
# def active_forms(modeladmin, request, queryset):
#     # short_description='Set forms as active'
#     queryset.update(forms=True)

class EventWorkshopAdmin(admin.ModelAdmin):
    list_filter = ('form',)
    list_display = ('event', 'name', 'slug', 'form')
    ordering = ('event', 'name', 'form')
    actions = [activate_forms, inactivate_forms]


################# Forms ##################
class EventAnswerAdmin(admin.ModelAdmin):
    list_filter = ('event',)
    list_display = ('event', 'firstname', 'lastname', 'email', 'country', 'address', 'city', 'region', 'zip_code', 'phone')
    ordering = ('event', 'email')
    actions = [csvexport]


class EventWorkshopAnswerAdmin(admin.ModelAdmin):
    list_filter = ('workshop',)
    list_display = ('workshop', 'firstname', 'lastname', 'email')
    ordering = ('workshop', 'email')
    actions = [csvexport]

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)

#################### Contact Form #########################
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email')
    ordering = ('email',)
    actions = [csvexport]

admin.site.register(ContactForm, ContactFormAdmin)

#################### Guess The Theme #########################
class GuessTheThemeAdmin(admin.ModelAdmin):
    list_filter = ('event',)
    list_display = ('event', 'firstname', 'lastname', 'email')
    ordering = ('event', 'firstname', 'lastname')
    actions = [csvexport]

admin.site.register(GuessTheTheme, GuessTheThemeAdmin)

admin.site.register(Blog, BlogAdmin)

admin.site.register(Member, MemberAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Social, SocialAdmin)
admin.site.register(Team, TeamAdmin)

################# Events #################
admin.site.register(Event, EventAdmin)
admin.site.register(EventPhoto, EventPhotoAdmin)
admin.site.register(EventVideo, EventVideoAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
admin.site.register(EventWorkshop, EventWorkshopAdmin)

################# Forms ##################
admin.site.register(EventAnswer, EventAnswerAdmin)
admin.site.register(EventWorkshopAnswer, EventWorkshopAnswerAdmin)
