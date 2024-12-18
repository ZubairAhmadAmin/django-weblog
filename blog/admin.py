from django.contrib import admin
from .models import Article, Category

admin.site.site_header = 'جنگو ویبلاک'
# remove action from admin panle
# admin.site.disable_action('delete_selected')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    actions = ["make_active", "make_inactive"]
    
    @admin.action(description="فعال ساختن دسته بندی انتخاب شده")
    def make_active(modeladmin, request, queryset):
        rows_updated = queryset.update(status=True)
        if rows_updated == 1:
            message_user = 'فعال شد'
        else:
            message_user = 'فعال شدند'
        modeladmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_user))
        
        
    @admin.action(description="غیر فعال ساختن دسته بندی انتخاب شده")
    def make_inactive(modeladmin, request, queryset):
        rows_updated = queryset.update(status=False)
        if rows_updated == 1:
            message_user = 'غیر فعال شد'
        else:
            message_user = 'غیر قعال شدند'
        modeladmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_user))

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', 'slug', 'author', 'Jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-publish']
    actions = ["make_published", "make_draft"]
    
    # add action to admin panle
    @admin.action(description='انتشار مقالات انتخاب شده')
    def make_published(modeladmin, request, queryset):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_user = 'منتشر شد.'
        else:
            message_user = 'منتشر شدند.'
        modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_user))
        
    @admin.action(description='پیش نویس شدن مقالات انتخاب شده')
    def make_draft(modeladmin, request, queryset):
        rows_updated = queryset.update(status='d')
        if rows_updated == 1:
            message_user = 'پیش نویس شد'
        else:
            message_user = 'پیش نویس شدند'
        modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_user))
    
    
# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)


