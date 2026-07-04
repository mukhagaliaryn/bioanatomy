from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_chapter'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='author',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Автор'),
        ),
    ]
