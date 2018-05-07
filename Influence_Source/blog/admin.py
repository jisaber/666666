from django.contrib import admin
from blog.models import BlogsPost,Exchange_record,Infect_source

class BlogsPostAdmin(admin.ModelAdmin):
    list_display = ['title','body','timestamp','timestamp_s']

class Blogs_context(admin.ModelAdmin):
    list_display = ['context','timestamp','timestamp_s']

class Infect_s(admin.ModelAdmin):
    list_display = ['infect_id','timestamp']

admin.site.register(BlogsPost,BlogsPostAdmin)
admin.site.register(Exchange_record,Blogs_context)
admin.site.register(Infect_source,Infect_s)

# Register your models here.
