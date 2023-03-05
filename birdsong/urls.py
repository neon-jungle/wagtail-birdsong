from django.urls import path

from birdsong.views import unsubscribe, subscribe, activate

app_name = 'birdsong'

urlpatterns = [
    path('unsubscribe/<uuid:user_id>/', unsubscribe.unsubscribe_user, name='unsubscribe'),
    path('subscribe', subscribe.subscribe, name='subscribe'),
    path('subscribe_api', subscribe.subscribe_api, name='subscribe_api'),
    path('activate/<cidb64>/<token>', activate.activate, name='activate'),
]
