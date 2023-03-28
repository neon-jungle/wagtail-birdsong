from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.module_loading import import_string
from django.views.generic.edit import FormView
from wagtail.models import Site

from birdsong.forms import ContactForm
from birdsong.models import Contact, BirdsongSettings
from birdsong.views import actions


class SignUpView(FormView):
    template_name = getattr(
        settings,
        'BIRDSONG_SIGNUP_TEMPLATE',
        'signup.html'
    )
    form_class = ContactForm
    contact_model = Contact

    def form_valid(self, form):
        birdsong_settings = BirdsongSettings.load(request_or_site=self.request)
        contact, created = self.contact_model.objects.get_or_create(email=form.cleaned_data["email"])
        
        if birdsong_settings.double_opt_in_enabled:
            from birdsong.options import BIRDSONG_DEFAULT_BACKEND

            site = Site.find_for_request(self.request)
            url = (
                site.root_url
                + reverse("birdsong:confirm", args=[contact.token])
            )

            backend_class = import_string(
                getattr(settings, "BIRDSONG_BACKEND", BIRDSONG_DEFAULT_BACKEND)
            )

            actions.send_confirmation(backend_class(), self.request, contact, url)
        
        if birdsong_settings.campaign_signup_redirect:
            redirect_url = birdsong_settings.campaign_signup_redirect.get_url()
            return redirect(redirect_url)
        else:
            site = Site.find_for_request(self.request)
            return render(
                self.request, 'signup_success.html', context={
                    'contact_email': contact.email,
                }
            )
