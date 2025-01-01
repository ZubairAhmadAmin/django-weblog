from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import User
from .forms import ProfileForm
from .mixins import FieldMixin, FormValidMixin, AuthorAccessMixin, SuperUserAccessMixin, AuthorsAccessMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from blog.models import Article

# from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes

# from django.core.mail import send_mail
# from django.core.mail import EmailMessage
from django.http import HttpResponse
from .tokens import account_activation_token
# from .forms import RegisterForm  # Assuming you have a RegisterForm defined

# from django.contrib.auth import get_user_model


# class base view
class ArticleList(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author = self.request.user)   
        
class ArticleCreate(AuthorsAccessMixin, FieldMixin, FormValidMixin, CreateView):
    model = Article
    template_name = 'registration/article-create-update.html'

class ArticleUpdate(AuthorAccessMixin, FieldMixin, FormValidMixin, UpdateView):
    model = Article
    template_name = 'registration/article-create-update.html'

class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_confirm_delete.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('account:profile')
    form_class = ProfileForm

    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs
    

class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')





# views.py
# class Register(CreateView):
#     form_class = RegisterForm
#     template_name = 'registration/register.html'

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
#         current_site = get_current_site(self.request)
#         mail_subject = 'فعال سازی اکانت'
#         message = render_to_string('registration/activate_account.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#         })
#         to_email = form.cleaned_data.get('email')
#         email = EmailMessage(
#                     mail_subject, message, to=[to_email]
#         )
#         email.send()
#         return HttpResponse('لینک فعال سازی به ایمل شما ارسال شد.<a href="/login">ورود</a>')


# from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
from .forms import SignupForm
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from .tokens import account_activation_token
# from django.contrib.auth.models import User
from django.core.mail import EmailMessage

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('registration/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
        # return HttpResponse('لینک فعال سازی به ایمل شما ارسال شد.<a href="/login">ورود</a>')
        return render(request, 'registration/confirm.html')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):   
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        return HttpResponse('اکانت شما با موفقیت فعال شد. برای ورود <a href="/login">کلیک</a> نماید.')
    else:
        return HttpResponse( 'لینک فعال سازی منقضی شده است. <a href="/registration">روباره امتحان نماید.</a>')


# def activate_account(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#         if user is not None and account_activation_token.check_token(user, token):
#             user.is_active = True
#             user.save()
#             return HttpResponse('اکانت شما با موفقیت فعال شد. برای ورود <a href="/login">کلیک</a> نماید.')
#         else:
#             return HttpResponse( 'لینک فعال سازی منقضی شده است. <a href="/registration">روباره امتحان نماید.</a>')
