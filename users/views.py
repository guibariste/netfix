from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer
from django.views.decorators.csrf import csrf_protect


def register(request):
    return render(request, 'users/register.html')


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
       
    #    a confirmer
        user.is_customer = 1
        user.is_company = 0

        # a confirmer
        user.save()
        birth = form.cleaned_data.get('date_of_birth')
        customer = Customer.objects.create(user_id=user.id,birth=birth)
      

        customer.save()
        login(self.request, user)
        return redirect('/')
    # est ce que form c'est form_class?



class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_customer = 0
        user.is_company = 1
        user.save()
        field = form.cleaned_data.get('field')
        company = Company.objects.create(user_id=user.id,field=field)
        company.save()
       

       

        login(self.request, user)
        return redirect('/')
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # connecter l'utilisateur
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})
# il faut aussi que il n'y a plus que logout et que profil aparraisse dans la navbar
