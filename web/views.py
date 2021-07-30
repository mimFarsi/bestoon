from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied

from .models import Expense, Income, Token, User
from json import JSONEncoder
from .forms import CustomUserCreationForm
from datetime import datetime
from .token import account_activation_token

# Create your views here.

@csrf_exempt
def submit_expense(request):
    """submit an expense"""

    #TODO: validate data: token, amount & date might be fake ...
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()
    Expense.objects.create(user = this_user, amount = request.POST['amount'], text = request.POST['text'], date = date)

    return JsonResponse({
        'status': 'ok',
    }, encoder = JSONEncoder )

@csrf_exempt
def submit_income(request):
    """submit an income"""

    #TODO: validate data: token, amount & date mighy be fake ...
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()
    Income.objects.create(user = this_user, amount = request.POST['amount'], text = request.POST['text'], date = date)

    return JsonResponse({
        'status': 'ok',
    }, encoder = JSONEncoder )


    #################### index#######################################
def index(request):
    return render(request, 'web/base.html', {'title':'index'})
  


########### Signup here #####################################

class RegisterView(View):
    def get(self, request):
        return render(request, 'web/register.html', { 'form': UserCreationForm() })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))

        return render(request, 'web/register.html', { 'form': form })


################ Login View ###################################################

class LoginView(View):
    def get(self, request):
        return render(request, 'web/login.html', { 'form':  AuthenticationForm })

    # low level but, using AuthenticationForm.clean for authentication
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                form.clean()
            except ValidationError:
                return render(
                    request,
                    'web/login.html',
                    { 'form': form, 'invalid_creds': True }
                )

            login(request, form.get_user())

            return redirect(reverse('profile'))

        return render(request, 'web/login.html', { 'form': form })



################ Profile View ###################################################

class ProfileView(LoginRequiredMixin, View):
    template_name = 'web/profile.html'
    context_object_name = 'expenses_list'
    model = Expense

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'incomes_list': Income.objects.order_by('name'),
            'more_context': Model.objects.all(),
        })
        return context

    def get_queryset(self):
        return Expense.objects.order_by('name')

    