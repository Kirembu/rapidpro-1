# Generated by Django 2.1.8 on 2019-06-06 20:36

import django.utils.timezone
from django.db import migrations, models


def drop_non_resthook_events(apps, schema_editor):
    WebHookEvent = apps.get_model("api", "WebHookEvent")
    _, num_deleted = WebHookEvent.objects.filter(resthook=None).delete()
    if num_deleted:
        print(f"Deleted {num_deleted} old non-resthook webhook events")


class Migration(migrations.Migration):

    dependencies = [("api", "0027_auto_20190208_2126")]

    operations = [
        migrations.RunPython(drop_non_resthook_events),
        migrations.RemoveField(model_name="webhookevent", name="channel"),
        migrations.RemoveField(model_name="webhookevent", name="next_attempt"),
        migrations.RemoveField(model_name="webhookevent", name="run"),
        migrations.AlterField(
            model_name="webhookevent", name="event", field=models.CharField(max_length=16, null=True)
        ),
        migrations.AlterField(
            model_name="webhookevent", name="status", field=models.CharField(max_length=1, null=True)
        ),
        migrations.AlterField(model_name="webhookevent", name="try_count", field=models.IntegerField(null=True)),
        migrations.AlterField(
            model_name="webhookevent", name="created_on", field=models.DateTimeField(default=django.utils.timezone.now)
        ),
        migrations.AlterField(
            model_name="webhookevent",
            name="resthook",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="api.Resthook"),
        ),
    ]