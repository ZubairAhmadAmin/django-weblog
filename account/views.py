from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from blog.models import Article

# class base view
class ArticleList(LoginRequiredMixin, ListView):
    template_name = 'registration/home.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author = self.request.user)
        
        
        
class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    fields = ["category", "author", "title", "slug", "description", "image", "publish", "status"]
    template_name = 'registration/article-create-update.html'