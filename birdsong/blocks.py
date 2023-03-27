from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks


class UnwrappedStreamBlock(blocks.StreamBlock):
    """Removes the surrounding divs around streamblocks."""
    def render_basic(self, value, context=None):
        return mark_safe('\n'.join(
            child.render(context=context) for child in value))


class DefaultBlocks(UnwrappedStreamBlock):
    rich_text = blocks.RichTextBlock(
        template='birdsong/mail/blocks/richtext.html',
        features=['h3', 'h4', 'bold', 'italic', 'link', 'ul', 'ol', 'document-link'])


class NewsletterSubscriptionBlock(blocks.StructBlock):
    """streamfield block for newsletter subscription on wagtail pages."""

    headline = blocks.CharBlock(verbose_name=_('Headline'), max_length=80)
    subtext = blocks.CharBlock(
        verbose_name=_('Subtext'), max_length=150, required=False
    )
    button_label = blocks.CharBlock(label=_('Button label'), max_length=50)
    privacy_text = blocks.RichTextBlock(
        label=_('Privacy Disclaimer'), max_length=500,
        features=[
            'bold',
            'italic',
            'link',
        ]
    )


    class Meta:
        template = 'birdsong/site/blocks/signup.html'
        icon = 'mail'
        label = _('Newsletter subscription')
