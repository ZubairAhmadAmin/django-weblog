from account.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, Category
from account.mixins import AuthorAccessMixin
# from django.core.paginator import Paginator

# Class Base View
class ArticleList(ListView):
    # also we can use this lines of code
    
    # model = Article -> #use when we want to get article list without filtering
    # template_name = 'blog/home.html'
    # context_object_name = 'articles'
    queryset = Article.objects.published()
    paginate_by = 2
    
    
class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)


class ArticlePreView(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


class CategoryList(ListView):
    paginate_by = 2
    template_name = 'blog/category_list.html'
    
    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
        # slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context
    
    
class AuthorList(ListView):
    paginate_by = 2
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