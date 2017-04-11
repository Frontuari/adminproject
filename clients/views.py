from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from forms import LoginForm,CreateUserForm
from django.contrib.auth import authenticate,login as login_django,logout as logout_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,DetailView,CreateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
# Create your views here.
class ShowView(DetailView):
    model = User
    template_name = 'show.html'
    slug_field = 'username' # Campo de la BD
    slug_url_kwarg = 'username_url' # Nombre del parametro de la URL

class LoginView(View):
    form = LoginForm()
    message = None
    template = 'login.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('clients:dashboard')
        return render(request,self.template,self.get_context())
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = request.POST['username'],password = request.POST['password'])
        if user is not None:
            login_django(request,user)
            return redirect('clients:dashboard')
        else:
            self.message = "Usuario o clave incorrecto"
        return render(request,self.template,self.get_context())
    def get_context(self):
        return {'form': self.form, 'message': self.message}

class DashboardView(LoginRequiredMixin, View):
    login_url = 'clients:login'
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html', {})

@login_required( login_url = 'clients:login')
def logout(request):
    logout_django(request)
    return redirect('clients:login')

class Create(CreateView):
    success_url = reverse_lazy('clients:login')
    model = User
    template_name = 'create.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        self.object = form.save( commit = False)
        self.object.set_password( self.object.password )
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

def create(request):
    form = CreateUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save( commit = False)
            user.set_password( user.password )
            user.save()
            return redirect('clients:login')
    context = {
        'form': form
    }
    return render(request, 'create.html',context)
