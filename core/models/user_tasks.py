from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import Task, Option, UserLesson, Video, Question, Theory, MatchingPair


# UserTask model
# ----------------------------------------------------------------------------------------------------------------------
class UserTask(models.Model):
    user_lesson = models.ForeignKey(
        UserLesson, on_delete=models.CASCADE,
        related_name='user_tasks', verbose_name=_('Қолданушының сабағы')
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE,
        related_name='user_tasks', verbose_name=_('Тапсырма')
    )
    submitted_at = models.DateTimeField(_('Жіберілген уақыты'), auto_now_add=True)
    rating = models.PositiveSmallIntegerField(_('Жалпы бағасы'), default=0)
    percentage = models.DecimalField(_('Пайыздық мөлшері'), default=0, max_digits=5, decimal_places=2)
    is_completed = models.BooleanField(_('Орындалды'), default=False)

    class Meta:
        verbose_name = _('Қолданушының тапсырмасы')
        verbose_name_plural = _('Қолданушының тапсырмалары')

    def __str__(self):
        return f'{self.user_lesson.user} | {self.task}'


# UserTheory model
# ----------------------------------------------------------------------------------------------------------------------
class UserTheory(models.Model):
    user_task = models.ForeignKey(
        UserTask, on_delete=models.CASCADE,
        related_name='user_theories', verbose_name=_('Қолданушының тапсырмасы')
    )
    theory = models.ForeignKey(
        Theory, on_delete=models.CASCADE,
        related_name='user_theories', verbose_name=_('Теория')
    )
    is_completed = models.BooleanField(_('Оқылды'), default=False)

    class Meta:
        verbose_name = _('Қолданушының теориясы')
        verbose_name_plural = _('Қолданушының теориялары')

    def __str__(self):
        return f'{self.user_task} | {self.theory}'


# UserVideo model
# ----------------------------------------------------------------------------------------------------------------------
class UserVideo(models.Model):
    user_task = models.ForeignKey(
        UserTask, on_delete=models.CASCADE,
        related_name='user_videos', verbose_name=_('Қолданушының тапсырмасы')
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE,
        related_name='user_videos', verbose_name=_('Видеосабақ')
    )
    watched_seconds = models.PositiveIntegerField(_('Қараған уақыт (сек)'), default=0)
    is_completed = models.BooleanField(_('Аяқталған'), default=False)

    class Meta:
        verbose_name = _('Қолданушының видеосабағы')
        verbose_name_plural = _('Қолданушының видеосабақтары')


# Test model
# ----------------------------------------------------------------------------------------------------------------------
# UserAnswer model
class UserAnswer(models.Model):
    user_task = models.ForeignKey(
        UserTask, on_delete=models.CASCADE, null=True,
        related_name='user_options', verbose_name=_('Қолданушы тапсырмасы')
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True,
        related_name='user_options', verbose_name=_('Жауап')
    )
    options = models.ManyToManyField(Option, related_name='user_answers', verbose_name=_('Таңдалған жауаптар'))

    class Meta:
        verbose_name = _('Таңдалған жауап')
        verbose_name_plural = _('Таңдалған жауаптар')


# UserMatchingAnswer model
# ----------------------------------------------------------------------------------------------------------------------
class UserMatchingAnswer(models.Model):
    user_task = models.ForeignKey(
        UserTask, on_delete=models.CASCADE,
        related_name='user_matching_answers', verbose_name=_('Қолданушының тапсырмасы')
    )
    pair = models.ForeignKey(
        MatchingPair, on_delete=models.CASCADE,
        related_name='user_matching_answers', verbose_name=_('Сәйкестендіру жұбы')
    )
    selected_right = models.TextField(_('Таңдалған оң жақ мәтін'), blank=True, default='')

    class Meta:
        verbose_name = _('Сәйкестендіру жауабы')
        verbose_name_plural = _('Сәйкестендіру жауаптары')

    def __str__(self):
        return f'{self.user_task} | {self.pair}'