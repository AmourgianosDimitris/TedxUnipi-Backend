from django.conf.urls import url

from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^socials/$', SocialView.as_view()),
    url(r'^partners/$', PartnerView.as_view()),
    url(r'^members/(?P<slug>.+)/$', MemberView.as_view()),
    url(r'^members/$', MemberDistinctView.as_view()),
    # url(r'^events/(?P<slug>.+)/photos/$', EventPhotoView.as_view()),
    # url(r'^events/(?P<slug>.+)/videos/$', EventVideoView.as_view()),
    # url(r'^events/(?P<slug>.+)/participants/$', EventParticipantView.as_view()),
    # url(r'^events/(?P<slug>.+)/workshops/$', EventWorkshopView.as_view()),
    url(r'^events/(?P<slug>.+)/$', EventView.as_view()),
    url(r'^events/$', EventListView.as_view()),
    url(r'^forms/workshops/(?P<slug>.+)/$', csrf_exempt(EventWorkshopAnswerView.as_view())),
    url(r'^forms/events/(?P<slug>.+)/$', csrf_exempt(EventAnswerView.as_view())),

    ################ Blogs ################
    url(r'^blog/category/(?P<category>.+)/$', ArticleFilterViewSet.as_view()),
    url(r'^blog/likes/remove/(?P<slug>.+)/$', RemoveLikeBlogViewSet.as_view()),
    url(r'^blog/likes/add/(?P<slug>.+)/$', AddLikeBlogViewSet.as_view()),
    url(r'^blog/(?P<slug>.+)/$', SingleArticleViewSet.as_view()),
    url(r'^blog/$', BlogViewSet.as_view())
]
