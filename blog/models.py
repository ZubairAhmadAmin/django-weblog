from django.db import models
from django.urls import reverse
from account.models import User
from django.utils.html import format_html
from django.utils import timezone
from extensions.utils import jalali_converter
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment

#my manager
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')
    
class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آی پی')


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
        ('d', 'پیش نویس'),          #draft
        ('p', 'منتشر شده'),         #publish
        ('i', 'در حال بررسی'),      #investigation
        ('b', 'بر گشت داده شده'),   #back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name='نویسنده')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='articles')
    title = models.CharField(max_length = 255, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length = 100, unique=True, verbose_name='آدرس مقاله')
    description = models.TextField(verbose_name='محتوا')
    image = models.ImageField(upload_to='images', verbose_name='تصویر مقاله')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    status = models.CharField(max_length = 1, choices=STATUS_CHOICES, verbose_name='وضیعت')
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, through="ArticleHit", blank=True, related_name="hits", verbose_name="بازدیدها")
    
    class Meta:
        verbose_name = 'مقاله',
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']
    
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('account:home')
    
    
    def Jpublish(self):
        return jalali_converter(self.publish)
    Jpublish.short_description = 'زمان انتشار'
    
    
    def image_tag(self):
        return format_html("<img width='100' heigth='75' style='border-radius: 5px' src='{}'>".format(self.image.url))
    image_tag.short_description = 'تصویر'
    
    
    def category_to_str(self):
        return ", ".join([category.title for category in self.category.active()])
    category_to_str.short_description = 'دسته بندی'
    
    objects = ArticleManager()


class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    
        
    
    
    
    
    
    
    
