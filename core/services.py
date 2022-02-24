from core import repository
from core.api.serializers import APIRegisterUserSerializer
from core.exceptions import PreferenceMissing, LimitMissing
from core.forms import AccountAuthForm
from django.core.exceptions import ObjectDoesNotExist
from core.models import Post

from core.serializers import MakePostSerializer, PostSerializer


def build_context(services, request):
    """Строит контекст на основе списка сервисов"""
    context = dict()

    for service in services:
        service_context = service(request).execute()
        context.update(service_context)

    return context


def _get_limit(limit_name):
    try:
        limit_value = repository.get_limit(limit_name)
    except ObjectDoesNotExist:
        raise LimitMissing(limit_name)

    return limit_value


def _build_pref_context(pref_list):
    values = repository.get_preferences_unlazy(pref_list)

    if len(pref_list) != len(values):
        raise PreferenceMissing(pref_list)

    context = dict(zip(pref_list, values))
    return context


class ViewService:
    def __init__(self, request=None):
        self.request = request


class BasicService(ViewService):
    def get_context(self):
        pref_list = ('blog_title', 'main_page_title', 'main_page_nav')
        context = _build_pref_context(pref_list)
        context.update({'is_anonymous': self.request.user.is_anonymous})
        return context

    def execute(self):
        return self.get_context()


class GETMainService(ViewService):
    @staticmethod
    def _build_context(username, write_post_serializer, posts):
        return {
            'username': username,
            'write_post_serializer': write_post_serializer,
            'posts': posts
        }

    def execute(self):
        username = self.request.user.username
        write_post_serializer = None

        if self.request.user.is_staff:
            write_post_serializer = MakePostSerializer()
        number_of_posts_to_show = _get_limit('number_of_posts_to_show')

        posts = Post.objects.filter(active=True).order_by('-date')[:number_of_posts_to_show]
        posts_serializer = PostSerializer(posts, many=True)

        return self._build_context(username, write_post_serializer, posts_serializer.data)


class LogoutService(ViewService):
    @staticmethod
    def get_context():
        pref_list = ('logout_message',)
        return _build_pref_context(pref_list)

    def execute(self):
        return self.get_context()


class RegistrationService(ViewService):
    def get_context(self):
        serializer = APIRegisterUserSerializer()
        return {'serializer': serializer}

    def execute(self):
        return self.get_context()


class LoginService(ViewService):
    def get_context(self):
        context = {'is_anonymous': self.request.user.is_anonymous, 'login_form': AccountAuthForm()}
        return context

    def execute(self):
        return self.get_context()
