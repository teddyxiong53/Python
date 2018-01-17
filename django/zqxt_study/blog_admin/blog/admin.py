from django.contrib import admin
from .models import Article, Author
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'update_time',)
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'join_time',)

    

admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, AuthorAdmin)
