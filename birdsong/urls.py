from django.urls import path
from .views import unsubscribe


app_name = 'birdsong'

urlpatterns = [
    path('unsubscribe/<uuid:user_id>/', unsubscribe.unsubscribe_user, name='unsubscribe')
]
