from django.contrib.auth import get_user_model, authenticate, login, logout
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from account.models import Account

import core.permissions
import core.serializers
import core.models

UserModel = get_user_model()


def limit_filter(request, queryset):
    limit_offset_serializer = core.serializers.LimitOffsetSerializer(data=request.GET)
    limit_offset_serializer.is_valid(raise_exception=True)

    limit = limit_offset_serializer.data.get('limit')
    offset = limit_offset_serializer.data.get('offset')

    if (offset, limit) == (None, None):
        start, end = None, None
    elif offset is None:
        start = None
        end = limit
    elif limit is None:
        start = offset
        end = None
    else:
        start = offset
        end = offset + limit

    return queryset[start:end]


class PostViewSet(ModelViewSet):
    lookup_field = 'pk'
    queryset = core.models.Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = [
        core.permissions.IsBlogOwnerOrReadOnly | core.permissions.IsStaffOrReadOnly]
    filter_fields = ['author__username', 'active', 'categories__name']

    def filter_queryset(self, queryset):
        if not self.request.user.is_staff:
            queryset = queryset.filter(active=True)

        queryset = limit_filter(self.request, queryset)

        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return core.serializers.MakePostSerializer
        elif self.request.method == 'GET':
            return core.serializers.PostSerializer

    def create(self, request, *args, **kwargs):
        create_serializer = self.get_serializer_class()(data=request.data, context={'request': self.request})
        create_serializer.is_valid(raise_exception=True)
        new_post_object = create_serializer.save()
        headers = self.get_success_headers(create_serializer.data)

        show_serializer = core.serializers.PostSerializer(new_post_object)

        return Response(show_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostCategoryViewSet(ModelViewSet):
    serializer_class = core.serializers.PostCategorySerializer
    lookup_field = 'id'
    queryset = core.models.PostCategory.objects.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = [core.permissions.PostCategoryPermission]
    filter_fields = ['name', 'id']


class ReactionsViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = core.serializers.ReactionSerializer
    queryset = core.models.PostReaction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['author', 'post', 'reaction']
    permission_classes = [core.permissions.PostReactionPermission]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return core.serializers.ReactionChangeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        duplicate = core.models.PostReaction.objects.filter(author=self.request.user,
                                                            post=serializer.validated_data.get('post'))

        if duplicate.exists():
            raise ValidationError('Reaction to this post already exist')

        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = core.serializers.CommentSerializer
    queryset = core.models.PostComment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['author', 'post']
    permission_classes = [core.permissions.PostCommentPermission]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return core.serializers.CommentChangeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=serializer.validated_data.get('post'))


class AccountViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = core.serializers.ReadAccountSerializer
    queryset = Account.objects.order_by('-date_joined')
    filter_backend = [DjangoFilterBackend]
    filter_fields = ['username', 'email', 'is_active', 'is_admin', 'is_staff']
    permission_classes = [core.permissions.AccountPermission]

    def filter_queryset(self, queryset):
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        queryset = limit_filter(self.request, queryset)

        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        action = self.action
        user = self.request.user

        if action == 'list':
            if user.is_staff:
                return core.serializers.ReadAccountPrivilegedSerializer
            return self.serializer_class
        elif action == 'retrieve':
            self.retrieve_object = self.get_object()

            if user.is_anonymous:
                return self.serializer_class
            elif user.is_staff:
                return core.serializers.ReadAccountPrivilegedSerializer

            if self.retrieve_object == user:
                return core.serializers.ReadAccountPrivilegedSerializer

            return self.serializer_class

        elif action in ('create', 'partial_update'):
            if user.is_staff:
                return core.serializers.CreateAccountPrivilegedSerializer
            else:
                return core.serializers.CreateAccountSerializer

        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(self.retrieve_object)

        return Response(serializer.data)

    def perform_create(self, serializer):
        login(self.request, serializer.save())

    def get_object(self):
        if self.kwargs[self.lookup_field] == 'me':
            user = self.request.user
            if user.is_anonymous:
                self.permission_denied(self.request)
            return user
        else:
            return super().get_object()

    def user_login(self, request):
        login_data_serializer = core.serializers.UserLoginSerializer(data=request.GET)
        login_data_serializer.is_valid(raise_exception=True)

        user = authenticate(**login_data_serializer.validated_data)

        if user is not None:
            user_serializer = core.serializers.CreateAccountPrivilegedSerializer(user)
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
