from django.contrib import admin
from .models import Post,CommentModel


# Register your models here.


# -------- Ravesh Aval ------------
class PostAdmin(admin.ModelAdmin):
    list_display=('title','user','slug','updated')
    search_fields=('title',)
    list_filter=('title','updated')
    prepopulated_fields={'slug':('title',)}
    raw_id_fields=('user',)

admin.site.register(Post,PostAdmin)


# -------- Ravesh Dovom ------------
@admin.register(CommentModel)
class CommentModelAdmin(admin.ModelAdmin):
    list_display=('user','post','body','created','is_reply')
    search_fields=('user','post','body')
    list_filter=('user','post','body')
    raw_id_fields=('user','post','reply')