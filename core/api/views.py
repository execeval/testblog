import core.serializers.account
import core.serializers.category
import core.serializers.comment
import core.serializers.post
import core.serializers.reaction
import core.serializers.utils
import core.permissions
import core.models

from django.contrib.auth import get_user_model, authenticate, login, logout
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from account.models import Account

from core.api.utils import limit_filter

UserModel = get_user_model()


class AccountViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = core.serializers.account.ReadAccountSerializer
    queryset = Account.objects.order_by('-date_joined')
    filter_backend = [DjangoFilterBackend]
    filter_fields = ('username', 'email', 'is_active', 'is_admin', 'is_staff')
    permission_classes = [core.permissions.AccountPermission]

    def is_self_lookup(self):
        return self.kwargs.get(self.lookup_field) == 'me'

    def filter_queryset(self, queryset):
        user = self.request.user
        if user.is_anonymous or not user.is_staff:
            queryset = queryset.filter(is_active=True)
        queryset = limit_filter(self.request, queryset)
        has_profile_picture_kwarg = self.request.GET.get('has_profile_picture', None)
        if isinstance(has_profile_picture_kwarg, str):
            if has_profile_picture_kwarg.lower() == 'true':
                queryset = queryset.exclude(profile_picture='')
            elif has_profile_picture_kwarg.lower() == 'false':
                queryset = queryset.filter(profile_picture='')

        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        action = self.action
        user = self.request.user

        if action == 'list':
            if user.is_staff:
                return core.serializers.account.ReadAccountPrivilegedSerializer
            return self.serializer_class
        elif action == 'retrieve':
            self.retrieve_object = self.get_object()

            if user.is_anonymous:
                return self.serializer_class
            elif user.is_staff:
                return core.serializers.account.ReadAccountPrivilegedSerializer

            if self.retrieve_object == user:
                return core.serializers.account.ReadAccountPrivilegedSerializer

            return self.serializer_class

        elif action in ('create', 'partial_update'):
            if user.is_staff:
                return core.serializers.account.CreateAccountPrivilegedSerializer
            else:
                return core.serializers.account.CreateAccountSerializer

        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(self.retrieve_object)

        return Response(serializer.data)

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)

    def perform_update(self, serializer):
        user = serializer.save()
        if self.is_self_lookup():
            login(self.request, user)

    def get_object(self):
        if self.is_self_lookup():
            user = self.request.user
            if user.is_anonymous:
                self.permission_denied(self.request)
            return user
        else:
            return super().get_object()

    def user_login(self, request):
        login_data_serializer = core.serializers.account.UserLoginSerializer(data=request.GET)
        login_data_serializer.is_valid(raise_exception=True)

        user = authenticate(**login_data_serializer.validated_data)

        if user is not None:
            user_serializer = core.serializers.account.CreateAccountPrivilegedSerializer(user)
            login(request, user)
            return Response(user_serializer.data)
        else:
            return Response({'detail': 'Wrong authenticate data'}, 403)

    def user_logout(self, request):
        user = request.user

        if user.is_anonymous:
            return Response({'detail': 'Not logged-in to logout'}, 403)

        logout(request)
        return Response({}, 204)


class PostViewSet(ModelViewSet):

    lookup_field = 'id'
    serializer_class = core.serializers.post.PostSerializer
    queryset = core.models.Post.objects.order_by('-date')
    filter_backend = [DjangoFilterBackend]
    filter_fields = ('title', 'is_active', 'author__username', 'author', 'date')
    permission_classes = [core.permissions.PostPermission]

    def full_partial_update(self, request):
        instances = core.models.Post.objects.filter(author=request.user)

        serializer = core.serializers.utils.IsActiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instances.update(**serializer.validated_data)

        return Response({'count': len(instances)})

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def filter_queryset(self, queryset):
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        queryset = limit_filter(self.request, queryset)

        return super().filter_queryset(queryset)


class CommentViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = core.serializers.comment.CommentSerializer
    queryset = core.models.PostComment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['author', 'post']
    permission_classes = [core.permissions.PostCommentPermission]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return core.serializers.comment.CommentChangeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=serializer.validated_data.get('post'))

    def filter_queryset(self, queryset):
        queryset = limit_filter(self.request, queryset)
        return super().filter_queryset(queryset)


class ReactionsViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = core.serializers.reaction.ReactionSerializer
    queryset = core.models.PostReaction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['author', 'post', 'reaction']
    permission_classes = [core.permissions.PostReactionPermission]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return core.serializers.reaction.ReactionChangeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        duplicate = core.models.PostReaction.objects.filter(author=self.request.user,
                                                            post=serializer.validated_data.get('post'))

        if duplicate.exists():
            raise ValidationError('Reaction to this post already exist')

        serializer.save(author=self.request.user)


class PostCategoryViewSet(ModelViewSet):
    serializer_class = core.serializers.category.PostCategorySerializer
    lookup_field = 'id'
    queryset = core.models.PostCategory.objects.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = [core.permissions.PostCategoryPermission]
    filter_fields = ['name', 'id']
