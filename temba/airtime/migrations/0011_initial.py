# Generated by Django 2.1.8 on 2019-07-01 21:40

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("channels", "0120_channellog_msg"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orgs", "0055_initial"),
        ("contacts", "0102_contacturn_channel"),
    ]

    operations = [
        migrations.CreateModel(
            name="AirtimeTransfer",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, help_text="Whether this item is active, use this instead of deleting"
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        help_text="When this item was originally created",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        help_text="When this item was last modified",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("P", "Pending"), ("S", "Success"), ("F", "Failed")],
                        default="P",
                        help_text="The state this event is currently in",
                        max_length=1,
                    ),
                ),
                ("recipient", models.CharField(max_length=64)),
                ("amount", models.FloatField()),
                ("denomination", models.CharField(blank=True, max_length=32, null=True)),
                ("data", models.TextField(blank=True, default="", null=True)),
                ("response", models.TextField(blank=True, default="", null=True)),
                (
                    "message",
                    models.CharField(
                        blank=True,
                        help_text="A message describing the end status, error messages go here",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "channel",
                    models.ForeignKey(
                        blank=True,
                        help_text="The channel that this airtime is relating to",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="airtime_transfers",
                        to="channels.Channel",
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        help_text="The contact that this airtime is sent to",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="contacts.Contact",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="The user which originally created this item",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="airtime_airtimetransfer_creations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        help_text="The user which last modified this item",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="airtime_airtimetransfer_modifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "org",
                    models.ForeignKey(
                        help_text="The organization that this airtime was triggered for",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="airtime_transfers",
                        to="orgs.Org",
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]
