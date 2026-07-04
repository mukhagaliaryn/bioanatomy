from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.forms.subjects import SubjectAdminForm, LessonAdminForm
from core.models import Subject, Lesson, LessonDocs
from django_summernote.admin import SummernoteModelAdmin, SummernoteModelAdminMixin
from core.models.tasks import Task


# Subject admin
# ----------------------------------------------------------------------------------------------------------------------
# Lesson Tab
class LessonTab(SummernoteModelAdminMixin, admin.TabularInline):
    model = Lesson
    fields = ('order', 'title', 'view_link', )
    extra = 0
    readonly_fields = ('view_link', )

    def view_link(self, obj):
        if obj.pk:
            url = reverse('admin:core_lesson_change', args=[obj.pk])
            return format_html('<a href="{}" class="view-link">Толығырақ</a>', url)
        return '-'

    view_link.short_description = _('Сабақ сілтемесі')


# Subject admin
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_at', 'last_update')
    search_fields = ('name', 'author', 'description', )
    inlines = (LessonTab, )
    form = SubjectAdminForm


# Lesson admin
# ----------------------------------------------------------------------------------------------------------------------
# LessonDocs Tab
class LessonDocsTab(admin.TabularInline):
    model = LessonDocs
    extra = 0


# Task Tab
class TaskTab(SummernoteModelAdminMixin, admin.TabularInline):
    model = Task
    fields = ('order', 'task_type', 'rating', 'duration', 'view_link', )
    extra = 0
    readonly_fields = ('view_link',)

    def view_link(self, obj):
        if obj.pk:
            url = reverse('admin:core_task_change', args=[obj.pk])
            return format_html('<a href="{}" class="view-link">Толығырақ</a>', url)
        return '-'

    view_link.short_description = _('Тапсырма сілтемесі')


# Lesson admin
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'order', )
    search_fields = ('title', 'subject', 'description', )
    list_filter = ('subject', )
    ordering = ('order', )
    inlines = (LessonDocsTab, TaskTab, )
    readonly_fields = ('subject_link', )
    form = LessonAdminForm

    def subject_link(self, obj):
        if obj.subject:
            url = reverse('admin:core_subject_change', args=[obj.subject.id])
            return format_html('<a href="{}" class="view-link">🔗 {}</a>', url, obj.subject.name)
        return '-'

    subject_link.short_description = 'Пәнге сілтеме'
