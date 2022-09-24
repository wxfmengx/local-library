from django.contrib import admin
from .models import Genre, Language, Author, Book, BookInstance

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookInstance)

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )