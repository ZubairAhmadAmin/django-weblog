from account.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, Category
from account.mixins import AuthorAccessMixin
from django.db.models import Q

# Class Base View
class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 5
 
class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)

        ip_address = self.request.user.ip_address

        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article


class ArticlePreView(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


class CategoryList(ListView):
    paginate_by = 5
    template_name = 'blog/category_list.html'
    
    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context
    
    
class AuthorList(ListView):
    paginate_by = 5
    template_name = 'blog/author_list.html'
    
    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()
    
    def get_context_data(self, **kwargs):
        # slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
    

class SearchList(ListView):
    paginate_by = 5
    template_name = 'blog/search_list.htl'

    def get_queryset(self):
        search = self.request.GET.get('q')
        return Article.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context
    
    
    




# Function Base View
    
# def home(request, page=1):
#     articles_list = Article.objects.published()
#     paginator = Paginator(articles_list, 2)
#     articles = paginator.get_page(page)
#     context = {
#         'articles': articles,
#         # 'articles': Article.objects.filter(status='p').order_by('-publish')[:1] -> instead we  defined ordering in models
#         # 'articles': Article.objects.filter(status='p'), -> instead we use manager
#         # 'articles': Article.objects.published(), #-> get published articles from database
#         # 'categories': Category.objects.filter(status=True) -> instead we use template tags
#     }
#     return render(request, 'blog/home.html', context)


# def detail(request, slug):
#     context = {
#         # 'article': get_object_or_404(Article, slug=slug, status='p'), -> instead we use manager
#         'article': get_object_or_404(Article.objects.published(), slug=slug),
#         # 'categories': Category.objects.filter(status=True)-> instead we use template tags

#     }
#     return render(request, 'blog/detail.html', context)


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list, 2)
#     articles = paginator.get_page(page)
#     context = {
#         "category": category,
#         "articles": articles
#     }
#     return render(request, 'blog/category.html', context)