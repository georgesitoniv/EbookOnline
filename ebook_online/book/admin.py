from django.contrib import admin

from . import models

class BookAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "date_published"]
    search_fields = ["name", "author", "category"]

class SearchNameAdmin(admin.ModelAdmin):
    search_fields = ["name"]


admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Author, SearchNameAdmin)
admin.site.register(models.Category, SearchNameAdmin)
admin.site.register(models.BookShelf)
admin.site.register(models.Review)
