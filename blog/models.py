from django.db import models
from django.utils.html import format_html
from django.utils import timezone
from extensions.utils import jalali_converter

#my manager
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')
    
class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)



class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیر دسته')
    title = models.CharField(max_length = 150, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length = 100, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')
    position = models.IntegerField(verbose_name='موقیعت')
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id', '-status']
    
    
    def __str__(self):
        return self.title
    
    objects = CategoryManager()
    


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
    )
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='articles')
    title = models.CharField(max_length = 255, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length = 100, unique=True, verbose_name='آدرس مقاله')
    description = models.TextField(verbose_name='محتوا')
    image = models.ImageField(upload_to='images', verbose_name='تصویر مقاله')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length = 1, choices=STATUS_CHOICES, verbose_name='وضیعت')
    
    class Meta:
        verbose_name = 'مقاله',
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']
    
    
    def __str__(self):
        return self.title
    
    
    def Jpublish(self):
        return jalali_converter(self.publish)
    Jpublish.short_description = 'زمان انتشار'
    
    
    def category_published(self):
        return self.category.filter(status=True)
    
    def image_tag(self):
        return format_html("<img width='100' heigth='75' style='border-radius: 5px' src='{}'>".format(self.image.url))
    image_tag.short_description = 'تصویر'
    
    objects = ArticleManager()
    
    
    
    
    
    
    
