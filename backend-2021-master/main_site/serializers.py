from rest_framework import serializers

from .models import *

'''
https://medium.com/@rushic24/creating-nested-serializers-in-django-rest-framework-5110c6674fba

https://docs.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line
'''


############################ general #############################
class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = [
            'id',
            'name',
            'url',
            'logo',
        ]


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = [
            'id',
            'name',
            'type',
            'logo_url',
            'brand_url',
        ]


class MemberSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(many=False, slug_field='name', read_only=True)
    role = serializers.SlugRelatedField(many=False, slug_field='name', read_only=True)

    class Meta:
        model = Member
        fields = [
            'id',
            'name',
            'email',
            'slug',
            'description',
            'photo_url',
            'team',
            'role',
        ]


################ Events ################
class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPhoto
        fields = [
            'id',
            'url'
        ]


class EventVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventVideo
        fields = [
            'id',
            'url'
        ]


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = [
            'id',
            'name',
            'air_date_time',
            'occupation',
            'type',
            'category',
            'photo_url',
            'description',
            'website_url',
            'facebook_url',
            'youtube_url',
            'twitter_url',
            'instagram_url',
            'linkedin_url',
        ]


class EventParticipantPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = [
            'id',
            'name',
            'occupation',
            'type',
            'category',
            'photo_url',
        ]


class EventWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventWorkshop
        fields = [
            'id',
            'name',
            'slug',
            'air_date_time',
            'banner_url',
            'form',
            'description',
            'website_url',
            'facebook_url',
            'twitter_url',
            'instagram_url',
            'linkedin_url',
        ]


class EventWorkshopPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventWorkshop
        fields = [
            'id',
            'name',
            'slug',
            'banner_url',
            'form'
        ]


class EventListSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    participants = EventParticipantPreviewSerializer(many=True, read_only=True)
    workshops = EventWorkshopPreviewSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'slug',
            'air_date',
            'location',
            'banner_url',
            'form',
            'description',
            'photos',
            'participants',
            'workshops'
        ]

    def get_photos(self, event: Event):
        query = event.photos.all()[:10]
        return EventPhotoSerializer(query, many=True, read_only=True).data


class EventSerializer(serializers.ModelSerializer):
    photos = EventPhotoSerializer(many=True, read_only=True)
    videos = EventVideoSerializer(many=True, read_only=True)
    participants = EventParticipantSerializer(many=True, read_only=True)
    workshops = EventWorkshopSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'slug',
            'air_date',
            'location',
            'banner_url',
            'form',
            'description',
            'photos',
            'videos',
            'participants',
            'workshops'
        ]


################# Forms ##################
class FormEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'slug',
            'air_date',
            'location',
            'banner_url',
            'description',
        ]


class FormWorkshopSerializer(serializers.ModelSerializer):
    event_banner_url = serializers.SerializerMethodField()

    class Meta:
        model = EventWorkshop
        fields = [
            'id',
            'name',
            'slug',
            'air_date_time',
            'banner_url',
            'event_banner_url',
            'description'
        ]

    def get_event_banner_url(self, workshop: EventWorkshop):
        return workshop.event.banner_url.url


class EventAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAnswer
        fields = [
            'id',
            'event',
            'firstname',
            'lastname',
            'email',
            'country',
            'address',
            'city',
            'region',
            'zip_code',
            'phone',
            'notes',
            'consent',
        ]

    def create(self, validated_data):
        return EventAnswer.objects.create(**validated_data)

    def validate_phone(self, phone: str):
        if not re.match("^[0-9+)(]*$", phone):
            raise serializers.ValidationError("Phone number must only contain digits, '(', ')' or '+'.")

        if not any(i.isdigit() for i in phone):
            raise serializers.ValidationError("Phone number must contain at least one digit.")

        return phone

    def validate_consent(self, consent: bool):
        if not consent:
            raise serializers.ValidationError("Data processing consent must be given in order to continue.")

        return consent


class EventWorkshopAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventWorkshopAnswer
        fields = [
            'id',
            'workshop',
            'firstname',
            'lastname',
            'email',
            'consent',
        ]

    def create(self, validated_data):
        return EventWorkshopAnswer.objects.create(**validated_data)

    def validate_consent(self, consent: bool):
        if not consent:
            raise serializers.ValidationError("Data processing consent must be given in order to continue.")

        return consent

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)
