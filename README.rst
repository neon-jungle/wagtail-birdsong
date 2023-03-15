.. image:: docs/birdsong.svg
    :width: 400
    :alt: Birdsong Logo

A plugin for wagtail that allows you to create, send, preview, edit and test email campaigns from within Wagtail.
Campaign templates are created using `mjml <https://mjml.io/>`_.

.. image:: docs/birdsong-admin-menu.png
    :width: 379
    :alt: Birdsong Admin Menu



Basic usage
===========

Install Birdsong:

.. code-block:: shell
    
    pip install wagtail-birdsong


Add the following to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'mjml',
        'birdsong',
        'wagtail.contrib.modeladmin',
        ...
    ]

Make a new app e.g. ``email``, create a ``models.py`` with a model that extends the included ``Campaign`` model. Some compatible mjml streamfield blocks are included in birdsong for convenience.

``models.py``

.. code-block:: python

    from birdsong.blocks import DefaultBlocks
    from birdsong.models import Campaign
    from django.db import models
    from wagtail.admin.edit_handlers import StreamFieldPanel
    from wagtail.core.fields import StreamField

    class SaleCampaign(Campaign):
        body = StreamField(DefaultBlocks())

        panels = Campaign.panels + [
            StreamFieldPanel('body'),
        ]

Then in the same app, create a ``wagtail_hooks.py`` if it doesn't exist, this is where the admin is created
for content editors to create/edit/send campaigns.

``wagtail_hooks.py``

.. code-block:: python

    from birdsong.wagtail_hooks import (
        CampaignAdmin, ContactAdmin, BirdsongAdminGroup, modeladmin_re_register
    )
    from .models import SaleCampaign

    class CampaignAdmin(CampaignAdmin):
        campaign = SaleCampaign

    @modeladmin_re_register
    class BirdsongAdminGroup(BirdsongAdminGroup):
        items = (CampaignAdmin, ContactAdmin)

:information_source: The ``CampaignAdmin`` is just an extension of Wagtail's ``ModelAdmin`` class so most of the same options are available for overriding functionality.
:information_source: ``BirdsongAdminGroup`` can be disabled with ``BIRDSONG_ADMIN_GROUP`` setting if you want to ``modeladmin_register`` your ``CampaignAdmin`` directly.


Create your campaign template in ``{app_folder}/templates/mail/{model_name}.html`` e.g. ``email/templates/mail/sale_campaign.html``,
alternatively override the ``get_template`` method on your campaign model.

:information_source: Campaign templates use django-mjml for responsive, well designed emails. To read up how to setup django-mjml you can read the docs 
`here <https://github.com/liminspace/django-mjml>`_. There is a base template included in Birdsong that can be extended.

``sale_campaign.html``

.. code-block:: html

    {% extends "birdsong/mail/base_email.html" %}

    {% block email_body %}
    <mj-section>
        <mj-column>
            <mj-text>Hello {{ contact.email }}!</mj-text>
            {% for b in self.body %}
                {{ b }}
            {% endfor %}
        </mj-column>
    </mj-section>
    {% endblock email_body %}


You're now ready to go!

.. image:: docs/birdsong-preview.png
    :width: 900
    :alt: Birdsong Preview



Custom Contact model
=====================

By default the included ``Contact`` model is used for every campaign, but you may want to store extra data, like names and preferences. 
You can override the default ``Contact`` model by setting an option on the admin for your campaign:

``models.py``

.. code-block:: python

    from birdsong.models import Contact
    from django.db import models

    class ExtendedContact(Contact):
        first_name = models.CharField(max_length=255)
        last_name = models.CharField(max_length=255)
        location = models.CharField(max_length=255)


``wagtail_hooks.py``

.. code-block:: python

    from birdsong.wagtail_hooks import (
        CampaignAdmin, ContactAdmin, BirdsongAdminGroup, modeladmin_re_register
    )
    from .models import SaleCampaign, ExtendedContact # NOTE: Import your custom Contact model

    class CampaignAdmin(CampaignAdmin):
        campaign = SaleCampaign
        contact_class = ExtendedContact # NOTE: Teach CampaignAdmin to use your custom Contact model

    class ContactAdmin(ContactAdmin): # NOTE: Overload ContactAdmin to list/edit/add your Contacts
        model = ExtendedContact
        list_diplay = ('email', 'first_name', 'last_name', 'location')

    @modeladmin_re_register
    class BirdsongAdminGroup(BirdsongAdminGroup):
        items = (CampaignAdmin, ContactAdmin)


``base.py``

.. code-block:: python

    # You may want to enrich the test contact (used in previews) with your new fields
    BIRDSONG_TEST_CONTACT = {
        'first_name': 'Wagtail', # new ExtendedContact field
        'last_name': 'Birdsong', # new ExtendedContact field
        'email': 'birdsong@example.com',
        'location': 'us', # new ExtendedContact field
    }



Filtering on contact properties
===============================

You might want to only send a campaign to a subset of your ``Contact`` models. Creating a filter using `django-filter <https://django-filter.readthedocs.io/en/main/>`_ and adding it to the ``CampaignAdmin`` allows users to filter on any property.

``filters.py``

.. code-block:: python

    from django_filters import FilterSet
    from django_filters.filters import AllValuesFilter

    from .models import ExtendedContact

    class ContactFilter(FilterSet):
        location = AllValuesFilter()

        class Meta:
            model = ExtendedContact
            fields = ('location',)


``wagtail_hooks.py``

.. code-block:: python

    from birdsong.wagtail_hooks import (
        CampaignAdmin, ContactAdmin, BirdsongAdminGroup, modeladmin_re_register
    )
    from .models import SaleCampaign, ExtendedContact
    from .filters import ContactFilter # NOTE: Import your custom Contact filter

    class CampaignAdmin(CampaignAdmin):
        campaign = SaleCampaign
        contact_class = ExtendedContact
        contact_filter_class = ContactFilter # NOTE: Use your custom Contact filter

    class ContactAdmin(ContactAdmin):
        model = ExtendedContact
        list_diplay = ('email', 'first_name', 'last_name', 'location')

    @modeladmin_re_register
    class BirdsongAdminGroup(BirdsongAdminGroup):
        items = (CampaignAdmin, ContactAdmin)


Users will now be able to send campaigns to a subset of contacts based on location.



Unsubscribe url
===============

Included in birdsong is a basic way for contacts to unsubscribe, just include the url configuration and add the unsubscribe url to your email template.

``urls.py``

.. code-block:: python

    from birdsong import urls as birdsong_urls
    from django.urls import include, path

    urlpatterns = [
        ...
        path('mail/', include(birdsong_urls)),
        ...
    ]

``sale_campaign.html``

.. code-block:: html

    {% extends "birdsong/mail/base_email.html" %}

    {% block email_body %}
    <mj-section>
        <mj-column>
            <mj-text>Hello {{ contact.email }}!</mj-text>
            {% for b in self.body %}
                {{ b }}
            {% endfor %}
        </mj-column>
    </mj-section>
    <mj-section>
        <mj-column>
            <mj-text align="center">
                Click <a href="{{ site.full_url }}{% url 'birdsong:unsubscribe' contact.id %}">here</a> to unsubscribe.
            </mj-text>
        </mj-column>
    </mj-section>
    {% endblock email_body %}



Future features
===============

- More tests!
- Proper docs
- Backends other thans SMTP for sending emails so analytics can be gathered (email opened, bounced etc)
- Reloading the preview on edit
- Broader permissions for campaigns (send, preview, test send)
