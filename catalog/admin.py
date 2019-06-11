from django.contrib import admin
from .models import *


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('second_name', 'first_name', 'email', 'date_of_birth', 'date_of_death')
    fields = ('first_name', 'second_name', 'about', 'email', ('date_of_birth', 'date_of_death',), 'photo')


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    verbose_name_plural = "Экземпляры книги"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'display_genre', 'isbn', 'language')
    inlines = [BookInstanceInline]
    sortable_by = ('title', 'language',)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back')
    search_fields = ('book',)
    sortable_by = ('book', 'status', 'due_back', 'borrower',)
    list_filter = ('status', 'due_back',)

    fieldsets = (
        (None,
         {'fields': ('book',)}),
        ('Доступность',
         {'fields': ('status', 'due_back', 'borrower',)}))


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    ordering = ('name',)

admin.site.register(Genre)
admin.site.register(Language)
