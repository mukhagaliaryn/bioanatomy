from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Lesson, UserSubject, UserLesson


@receiver(post_save, sender=Lesson)
def create_user_lessons_on_new_lesson(sender, instance, created, **kwargs):
    if not created:
        return

    for user_subject in UserSubject.objects.filter(subject=instance.subject):
        UserLesson.objects.get_or_create(
            user=user_subject.user,
            user_subject=user_subject,
            lesson=instance
        )
