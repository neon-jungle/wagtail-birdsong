# Example

Add the following to your installed apps:

```
'mjml',
'wagtailbirdsong',
```

Make a new app eg `email` and create a file called `models.py` with the following:

```
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField

from wagtailbirdsong.blocks import DefaultBlocks
from wagtailbirdsong.models import BaseEmail


class SaleEmail(BaseEmail):
    subject = models.TextField()
    body = StreamField(DefaultBlocks())

    panels = [
        FieldPanel('subject'),
        StreamFieldPanel('body'),
    ]
```

In your `wagtail_hooks.py` add something like:

```
from wagtail.contrib.modeladmin.options import modeladmin_register
from wagtailbirdsong.options import CustomModelAdmin

from .models import SaleEmail


@modeladmin_register
class SaleEmailAdmin(CustomModelAdmin):
    model = SaleEmail
    menu_label = 'SaleEmail'
    menu_icon = 'pilcrow'
    menu_order = 200
```

Create your email template in `{app_folder}/templates/{app_name}/mail/{model_name}.html` eg `email/templates/email/mail/sale_email.html`:

```
{% extends "wagtailbirdsong/mail/base_email.html" %}

{% block email_body %}
<mj-section>
    <mj-column>
        <mj-text>Hello world! {{ self.subject }}</mj-text>
        {% for b in self.body %}
            <mj-text>{{ b }}</mj-text>
        {% endfor %}
    </mj-column>
</mj-section>
{% endblock email_body %}
```
