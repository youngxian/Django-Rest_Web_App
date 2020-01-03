from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, FormView, View
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.http import JsonResponse
from accounts.models import User
from django.db.models import Q
from accounts.forms import SignupForm, LoginForm
from app.decorators import anonymous_view
from django.urls import reverse_lazy
from django.http import Http404
from app.decorators import anonymous_only,anonymous_view, logged_user_view

# Create your views here.

@anonymous_view()
class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:email_verification_confirmation')


    def get_form_kwargs(self):
        ''' Form Initialize '''
        data = super(SignupView, self).get_form_kwargs()
        data.update({'request': self.request})
        return data
    
    def get_context_data(self, **kwargs):
        '''get context '''
        context = super(SignupView, self).get_context_data(**kwargs)
        return context

@anonymous_view()
class LoginView(FormView):
    '''Login view '''
    
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy( 'accounts:dashboard') 

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        if self.request.method=="POST":
            form = LoginForm(self.request.POST)
            if form.is_valid:
                context['email'] = self.request.POST['email']
        return context

    def form_valid(self, form):
        user = form.get_user()
        if form.is_valid():
            try:
                auth_login(self.request, user,backend='django.contrib.auth.backends.ModelBackend')
                response = super(LoginView, self).form_valid(form)
                return response
            except Exception as e:
                pass

@anonymous_view()
class EmailVerificationConfirmationLinkView(TemplateView):
    """
    View shows success page post successful user sign up.
    """
    
    template_name   = 'accounts/email/email-verification-confirmation-link.html'
    
    def get_context_data(self, **kwargs):
        context = super(EmailVerificationConfirmationLinkView, self).get_context_data(**kwargs)
        try:
            context['email'] = self.request.session['user_email']
        except:
            raise Http404()
        return context

@logged_user_view(redirect_to=reverse_lazy('accounts:login'))
class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class UserListView(View):
    
    def get(self, request, data):
        try:
            user = User.objects.get(id=request.user.id)
            users = list(User.objects.filter(Q(email__icontains=data) | Q(first_name__contains=data)).exclude(email=user.email).values('id','email','first_name','last_name'))
            return JsonResponse(users, safe=False)
        except Exception as e:
            return JsonResponse({"errors":str(e)})  
        