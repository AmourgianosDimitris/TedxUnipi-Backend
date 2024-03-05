from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


############################ general #############################
class SocialView(APIView):
    def get(self, request):
        socials = Social.objects.all()
        serializer = SocialSerializer(socials, many=True, read_only=True)
        return Response(serializer.data)


class PartnerView(APIView):
    def get(self, request):
        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True, read_only=True)
        return Response(serializer.data)


class MemberDistinctView(APIView):
    def get(self, request):
        members = get_list_or_404(Member.objects.values_list('slug', flat=True).distinct().order_by('-slug'))
        return JsonResponse(list(members), safe=False)


class MemberView(APIView):
    def get(self, request, slug):
        members = get_list_or_404(Member.objects.filter(slug=slug))
        serializer = MemberSerializer(members, many=True, read_only=True)
        return Response(serializer.data)


############################ events #############################
class EventListView(APIView):
    def get(self, request):
        events = Event.objects.exclude(published=False)
        serializer = EventListSerializer(events, many=True, read_only=True)
        return Response(serializer.data)


##################### events/(?P<slug>.+) #######################
class EventView(APIView):
    def get(self, request, slug):
        event = get_object_or_404(Event.objects.exclude(published=False), slug=slug)
        serializer = EventSerializer(event, read_only=True)
        return Response(serializer.data)


# class EventPhotoView(APIView):
#     def get(self, request, slug):
#         event = get_object_or_404(Event.objects.exclude(published=False), slug=slug)
#         photos = EventPhoto.objects.filter(event_id=event)
#         serializer = EventPhotoSerializer(photos, many=True, read_only=True)
#         return Response(serializer.data)
#
#
# class EventVideoView(APIView):
#     def get(self, request, slug):
#         event = get_object_or_404(Event.objects.exclude(published=False), slug=slug)
#         videos = EventVideo.objects.filter(event_id=event)
#         serializer = EventVideoSerializer(videos, many=True, read_only=True)
#         return Response(serializer.data)
#
#
# class EventParticipantView(APIView):
#     def get(self, request, slug):
#         event = get_object_or_404(Event.objects.exclude(published=False), slug=slug)
#         participants = EventParticipant.objects.filter(event_id=event)
#         serializer = EventParticipantSerializer(participants, many=True, read_only=True)
#         return Response(serializer.data)
#
#
# class EventWorkshopView(APIView):
#     def get(self, request, slug):
#         event = get_object_or_404(Event.objects.exclude(published=False), slug=slug)
#         workshops = EventWorkshop.objects.filter(event_id=event)
#         serializer = EventWorkshopSerializer(workshops, many=True, read_only=True)
#         return Response(serializer.data)


################# Forms ##################
def check_event_form_capacity(event):
    answer_count = EventAnswer.objects.filter(event=event.id).count()
    if answer_count >= event.form_capacity:
        event.form = False
        event.save()


def check_country_code(cc):
    for val in Country_Choices:
        if cc == val[1]:
            return 0
    return 1


class EventAnswerView(APIView):
    def get(self, request, slug):
        event = get_object_or_404(Event.objects.exclude(published=False).filter(form=True), slug=slug)
        serializer = FormEventSerializer(event, many=False, read_only=True)
        return Response(serializer.data)

    def post(self, request, slug):
        event = get_object_or_404(Event.objects.filter(form=True).exclude(published=False), slug=slug)

        answer = {
            'event': event.id,
            'firstname': request.data.get('firstname'),
            'lastname': request.data.get('lastname'),
            'email': request.data.get('email'),
            'country': request.data.get('country'),
            'address': request.data.get('address'),
            'city': request.data.get('city'),
            'region': request.data.get('region'),
            'zip_code': request.data.get('zip_code'),
            'phone': request.data.get('phone'),
            'notes': request.data.get('notes'),
            'consent': request.data.get('consent'),
        }

        # Create an answer from the above data
        serializer = EventAnswerSerializer(data=answer)
        if serializer.is_valid(raise_exception=True):
            answer_saved = serializer.save()
            check_event_form_capacity(event)
        return Response({"success": True})


def check_workshop_form_capacity(workshop):
    answer_count = EventWorkshopAnswer.objects.filter(workshop=workshop.id).count()
    if answer_count >= workshop.form_capacity:
        workshop.form = False
        workshop.save()


class EventWorkshopAnswerView(APIView):
    def get(self, request, slug):
        workshop = get_object_or_404(EventWorkshop.objects.filter(form=True), slug=slug)
        serializer = FormWorkshopSerializer(workshop, many=False, read_only=True)
        return Response(serializer.data)

    def post(self, request, slug):
        workshop = get_object_or_404(EventWorkshop.objects.filter(form=True), slug=slug)

        answer = {
            'workshop': workshop.id,
            'firstname': request.data.get('firstname'),
            'lastname': request.data.get('lastname'),
            'email': request.data.get('email'),
            'consent': request.data.get('consent'),
        }

        # Create an answer from the above data
        serializer = EventWorkshopAnswerSerializer(data=answer)
        if serializer.is_valid(raise_exception=True):
            answer_saved = serializer.save()
            check_workshop_form_capacity(workshop)
        return Response({"success": True})

################ Blog ################
class BlogViewSet(APIView):
    def get(self, request):
        blog = get_list_or_404(Blog.objects.all())
        serializer = BlogSerializer(blog, many=True, read_only=True)
        return Response(serializer.data)

class SingleArticleViewSet(APIView):
    def get(self, request, slug):
        blog = get_object_or_404(Blog.objects.filter(slug=slug))
        serializer = BlogSerializer(blog, many=False, read_only=True)
        return Response(serializer.data)

class ArticleFilterViewSet(APIView):
    def get(self, request, category):
        category = f'({category.replace("-", "|")})'
        print (category)
        blogFilter = get_list_or_404(Blog.objects.filter(category__regex=category))
        serializer = BlogSerializer(blogFilter, many=True, read_only=True)
        return Response(serializer.data)

class ArticleSearchViewSet(APIView):
    def get(self, request, word):
        searchWord = f"({word})"
        blogSearch = get_list_or_404(Blog.objects.filter(title__regex=searchWord))
        serializer = BlogSerializer(blogSearch, many=True, read_only=True)
        return Response(serializer.data)

class AddLikeBlogViewSet(APIView):
    def get(self, request, slug):
        blog = get_object_or_404(Blog.objects.filter(slug=slug))

        blog.likes = blog.likes + 1
        blog.save()

        serializer = BlogSerializer(blog)
        return Response(serializer.data)

class RemoveLikeBlogViewSet(APIView):
    def get(self, request, slug):
        blog = get_object_or_404(Blog.objects.filter(slug=slug))

        blog.likes = blog.likes - 1
        blog.save()

        serializer = BlogSerializer(blog)
        return Response(serializer.data)

#################### Newsletter #########################
class SubscribersViewSet(APIView):
    def get(self, request):
        subs = get_list_or_404(Subscribers.objects.all())
        serializer = SubscribersSerializer(subs, many=True, read_only=True)
        return Response(serializer.data)
