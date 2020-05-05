# Wagtail Birdsong

A plugin for wagtail that allows you to create, send, preview, edit and test email campaigns from within Wagtail.
Campaign templates are created using [mjml](https://mjml.io/).

## Basic usage

Install birdsong:

```shell
pip install wagtail-birdsong
```

Add the following to your installed apps:

```python
'mjml',
'birdsong',
'wagtail.contrib.modeladmin',
```

Make a new app e.g. `email`, create a `models.py` with a model that extends the included `Campaign` model. Some compatible mjml streamfield blocks are included in birdsong for convenience.

```python
from birdsong.blocks import DefaultBlocks
from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField


class SaleEmail(Campaign):
    body = StreamField(DefaultBlocks())

    panels = Campaign.panels + [
        StreamFieldPanel('body'),
    ]

```

Then in the same app, create a `wagtail_hooks.py` if it doesn't exist, this is where the admin is created
for content editors to create/edit/send campaigns.

The `CampaignAdmin` is just an extension of Wagtail's `ModelAdmin` class so most of the same options are available for overriding functionality.

```python
from wagtail.contrib.modeladmin.options import modeladmin_register
from birdsong.options import CampaignAdmin

from .models import SaleEmail


@modeladmin_register
class SaleEmailAdmin(CampaignAdmin):
    campaign = SaleEmail
    menu_label = 'Sale Email'
    menu_icon = 'mail'
    menu_order = 200

```

Create your campaign template in `{app_folder}/templates/{app_name}/mail/{model_name}.html` eg `email/templates/email/mail/sale_email.html`,
alternatively override the `get_template` method on your campaign model.

Campaign templates us django-mjml for responsive, well designed emails. To read up how to setup django-mjml you can read the docs [here](https://github.com/liminspace/django-mjml). There is a base template included in Birdsong that can be extended.

```
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
```

## Custom Contact models

By default the included `Contact` model is used for every campaign, sometimes you may want to store extra data, like names and preferences. 
You can override the default `Contact` model by setting an option on the admin for your campaign:

`models.py`
```python

from birdsong.models import Contact
from django.db import models

class ExtendedContact(Contact):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

```

`wagtail_hooks.py`
```python
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from birdsong.options import CampaignAdmin

from .models import ExtendedContact, SaleEmail


@modeladmin_register
class SaleEmailAdmin(CampaignAdmin):
    campaign = SaleEmail
    menu_label = 'Sale Email'
    menu_icon = 'mail'
    menu_order = 200
    contact_class = ExtendedContact


# You may want to add your own modeladmin here to list/edit/add contacts
@modeladmin_register
class ContactAdmin(ModelAdmin):
    model = ExtendedContact
    menu_label = 'Contacts'
    menu_icon = 'user'
    list_diplay = ('email', 'first_name', 'last_name', 'location')

```

## Filtering on contact properties

You might want to only send a campaign to a subset of you `Contact` models. Creating a filter using [django-filter](https://django-filter.readthedocs.io/en/master/) and adding it to the `CampaignAdmin` allows users to filter on any property.

`filters.py`
```python
from django_filters import FilterSet
from django_filters.filters import AllValuesFilter

from .models import ExtendedContact


class ContactFilter(FilterSet):
    location = AllValuesFilter()

    class Meta:
        model = ExtendedContact
        fields = ('location',)
```

`wagtail_hooks.py`
```python
from wagtail.contrib.modeladmin.options import modeladmin_register
from birdsong.options import CampaignAdmin

from .filters import ContactFilter
from .models import ExtendedContact, SaleEmail


@modeladmin_register
class SaleEmailAdmin(CampaignAdmin):
    campaign = SaleEmail
    menu_label = 'Sale Email'
    menu_icon = 'mail'
    menu_order = 200
    contact_class = ExtendedContact
    contact_filter_class = ContactFilter
```

Users will now be able to send campaigns to a subset of contacts base on location.

## Future features:

- Tests!
- Backends other thans SMTP for sending emails so analytics can be gathered (email opened, bounced etc)
- In place previewing of email templates like [wagtail-livepreview](https://github.com/KalobTaulien/wagtail-livepreview)