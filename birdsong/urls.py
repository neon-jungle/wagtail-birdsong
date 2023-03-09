from django.urls import path

from .views import unsubscribe, confirm, signup

app_name = "birdsong"

urlpatterns = [
    path('unsubscribe/<uuid:user_id>/', unsubscribe.unsubscribe_user, name='unsubscribe'),
    path('confirm/<uuid:token>/', confirm.confirm_contact, name='confirm'),
    path('signup/', signup.SignUpView.as_view(), name='signup'),
]
