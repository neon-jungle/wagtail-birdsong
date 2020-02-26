from django.conf.urls import url

from .views import editor, mail

app_name = 'wagtailbirdsong'
urlpatterns = [
    url(r'^view_draft/(?P<emailcampaign_pk>.*)/$', editor.view_draft,
        name='view_draft'),
    url(r'^send/(?P<emailcampaign_pk>.*)/$', mail.send,
        name='send'),
]