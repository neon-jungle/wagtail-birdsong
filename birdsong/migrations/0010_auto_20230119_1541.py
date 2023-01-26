# Generated by Django 3.2.16 on 2023-01-19 14:41

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('wagtailcore', '0078_referenceindex'),
        ('birdsong', '0009_auto_20221222_1737'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Kontakt', 'verbose_name_plural': 'Kontakte'},
        ),
        migrations.AlterModelOptions(
            name='doubleoptinsettings',
            options={'verbose_name': 'Double-opt-in-Einstellungen'},
        ),
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(help_text='Name der Kampagne', max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='receipts',
            field=models.ManyToManyField(through='birdsong.Receipt', to='birdsong.Contact', verbose_name='receipts'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sent_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='sent date'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.IntegerField(choices=[(0, 'unsent'), (1, 'sending'), (2, 'sent'), (3, 'failed')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='subject',
            field=models.TextField(verbose_name='Betreff'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='confirmed_at',
            field=models.DateTimeField(null=True, verbose_name='confirmed at'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Erstellt am'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='e-mail'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='is confirmed'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='birdsong.ContactTag', to='taggit.Tag', verbose_name='Schlagwörter'),
        ),
        migrations.AlterField(
            model_name='doubleoptinsettings',
            name='campaign_confirmation_redirect',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Umleitung nach Bestätigung der Kampagnen-Registrierung'),
        ),
        migrations.AlterField(
            model_name='doubleoptinsettings',
            name='campaign_signup_redirect',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Umleitung nach Kampagnen-Registrierung'),
        ),
        migrations.AlterField(
            model_name='doubleoptinsettings',
            name='campaign_unsubscribe_success',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Umleitung nach erfolgreicher Abmeldung'),
        ),
        migrations.AlterField(
            model_name='doubleoptinsettings',
            name='confirmation_email_body',
            field=wagtail.fields.RichTextField(default='Klicke auf den folgenden Link, wenn du dich für unseren Newsletter anmelden willst. Ansonsten ist keine Handlung nötig.', help_text='Dieser Text ist Inhalt der E-Mail, die nach der Kampagnen-Registrierung versendet wird.', verbose_name='Inhalt der Bestätigungs-E-Mail'),
        ),
        migrations.AlterField(
            model_name='doubleoptinsettings',
            name='confirmation_email_subject',
            field=models.CharField(default='Bestätige Newsletterregistrierung', max_length=150, verbose_name='Betreff der Bestätigungs-E-Mail'),
        ),
    ]
