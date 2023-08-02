from allauth.account.views import SignupView, LoginView
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from crispy_forms.utils import render_crispy_form
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.urls import reverse

from .forms import UserRegisterForm


class SignUpView(SignupView):
    """
    Creates new employee
    """
    template_name = 'account/registration.html'
    form_class = UserRegisterForm

    def get(self, request, *args, **kwargs):
        # Use RequestContext instead of render_to_response from 3.0
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            # complete_signup(request, user, app_settings.EMAIL_VERIFICATION, "/")
            messages.success(request, 'Successfully Account Created.')
            return redirect('account_login')

        return render(request, self.template_name, {'form': form})


class HtmxLoginView(LoginView):
    template_name = 'account/login.html'
    htmx = True

    # def form_valid(self, form):
    #     if self.request.htmx:
    #         print('htmx')
    #         return HTTPResponseHXRedirect('/')

    # def form_invalid(self, form):
    #     ctx = {}
    #     ctx.update(csrf(self.request))
    #     form_html = render_crispy_form(form, context=ctx)
    #     print(form_html)
    #     return HttpResponse(form_html)


# def login(request):
#     # TODO: make this function prevent logged-in accounts from entering 'login' page
#     if request.user.is_authenticated:
#         return redirect('homepage')
#     else:
#         return redirect('login')


# def logout(request):
#     # TODO: make this function prevent guests from entering 'logout' page
#     if request.user.is_authenticated:
#         return redirect('logout')
#     else:
#         return redirect('homepage')


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def profile(request):
    context = {
        'accounts': request.user
    }
    return render(request, 'account/profile.html', context=context)


def check_email(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form)
        context = {
            'field': as_crispy_field(form['email']),
            'valid': not form['email'].errors
        }
        return render(request, 'partials/field.html', context)
    else:
        # If it's a GET request, return an empty form
        form = UserRegisterForm()
        context = {
            'field': as_crispy_field(form['email']),
            'valid': True
        }
        return render(request, 'partials/field.html', context)


def check_email(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form)
        context = {
            'field': as_crispy_field(form['email']),
            'valid': not form['email'].errors
        }
        return render(request, 'partials/field.html', context)
    else:

        form = UserRegisterForm()
        context = {
            'field': as_crispy_field(form['email']),
            'valid': True
        }
        return render(request, 'partials/field.html', context)


def check_phone_number(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        context = {
            'field': as_crispy_field(form['phone_number']),
            'valid': not form['phone_number'].errors
        }
        return render(request, 'partials/field.html', context)
    else:

        form = UserRegisterForm()
        context = {
            'field': as_crispy_field(form['phone_number']),
            'valid': True
        }
        return render(request, 'partials/field.html', context)
