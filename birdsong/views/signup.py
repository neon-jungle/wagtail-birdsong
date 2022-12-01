from ..forms import ContactForm
from birdsong.models import Contact, DoubleOptInSettings
from birdsong.views import actions
from django.shortcuts import redirect
from django.utils.module_loading import import_string
from django.views.generic.edit import FormView
from django.urls import reverse
from django.conf import settings


class SignUpView(FormView):
    template_name = "site/signup.html"
    form_class = ContactForm

    def form_valid(self, form):
        from birdsong.options import BIRDSONG_DEFAULT_BACKEND

        double_opt_in_settings = DoubleOptInSettings.load(request_or_site=self.request)
        contact = Contact.objects.create(email=form.cleaned_data["email"])

        url = self.request.get_host() + reverse(
            "birdsong:confirm", args=[contact.token]
        )

        backend_class = import_string(
            getattr(settings, "BIRDSONG_BACKEND", BIRDSONG_DEFAULT_BACKEND)
        )

        actions.send_confirmation(backend_class(), self.request, contact, url)

        redirect_url = "/"
        if double_opt_in_settings.campaign_signup_redirect:
            redirect_url = double_opt_in_settings.campaign_signup_redirect.get_url()

        return redirect(redirect_url)
