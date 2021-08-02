from django.contrib import admin
from .models import Blogs, Comment

class BlogAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Blogs, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
