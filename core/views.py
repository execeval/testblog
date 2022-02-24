from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.views import LogoutView
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import permission_classes
from core.permissions import IsStaffOrReadOnly
from core.serializers import MakePostSerializer, PostSerializer
from core.services import build_context
from rest_framework.views import APIView

from core import services
from django.views.generic import TemplateView

__all__ = ['Auth', 'Main', 'LogoutView', 'LoginView', 'registration_post_form', 'login_post', 'logout_post']

from core.api.serializers import APIRegisterUserSerializer
from core.forms import AccountAuthForm


class ServicedView(TemplateView):
    services = tuple()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for service in self.services:
            service_context = service(self.request).execute()
            print(service_context)
            context.update(service_context)

        return context


class Main(APIView):
    def get(self, request):
        services_list = (services.BasicService, services.GETMainService)
        template_name = 'testblog/main.html'

        context = build_context(services_list, request)

        return render(request, template_name, context=context)

    @permission_classes([IsStaffOrReadOnly])
    def post(self, request):
        make_post_serializer = MakePostSerializer(data=request.data, context={'user': request.user})
        make_post_serializer.is_valid(raise_exception=True)
        new_post = make_post_serializer.save()
        return JsonResponse(PostSerializer(new_post).data)


class Auth(TemplateView):
    template_name = 'testblog/auth.html'


class Registration(ServicedView):
    template_name = 'testblog/registration.html'
    services = (services.BasicService, services.RegistrationService)


class LoginView(ServicedView):
    template_name = 'testblog/login.html'
    services = (services.BasicService, services.LoginService)


def registration_post_form(request):
    if request.method == 'POST':
        serialized_user_data = APIRegisterUserSerializer(data=request.POST)
        if not serialized_user_data.is_valid():
            return JsonResponse(serialized_user_data.errors)

        serialized_user_data.create(serialized_user_data.validated_data)

        return redirect('home')

    else:
        raise SuspiciousOperation('This request method is not supported')


def logout_post(request):
    logout(request)
    return redirect('home')


def login_post(request):
    if request.method == 'POST':
        form = AccountAuthForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'error': form.errors['__all__'][0]})

        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])

        if user:
            login(request, user)

        return redirect('home')

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
