from django.db import migrations, models
import django.db.models.deletion


def fill_lesson_subject_from_chapter(apps, schema_editor):
    Lesson = apps.get_model('core', 'Lesson')
    for lesson in Lesson.objects.filter(subject__isnull=True).select_related('chapter__subject'):
        if lesson.chapter and lesson.chapter.subject:
            lesson.subject = lesson.chapter.subject
            lesson.save(update_fields=['subject'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_usersimulator_simulator_and_more'),
    ]

    operations = [
        # 1. Lesson.subject null → subject from chapter
        migrations.RunPython(fill_lesson_subject_from_chapter, migrations.RunPython.noop),

        # 2. Make Lesson.subject non-nullable
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='lessons',
                to='core.subject',
                verbose_name='Пән',
            ),
        ),

        # 3. Remove UserChapter model (CASCADE will clean FK rows)
        migrations.DeleteModel(name='UserChapter'),

        # 4. Remove Lesson.chapter FK
        migrations.RemoveField(model_name='lesson', name='chapter'),

        # 5. Remove Chapter model
        migrations.DeleteModel(name='Chapter'),
    ]
