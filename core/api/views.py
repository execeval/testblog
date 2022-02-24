from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from core.serializers import GetAccountByNameSerializer, UserSerializer, MakePostSerializer, PostSerializer, \
    PostCategorySerializer, PrivateAccountSerializer, PublicAccountSerializer, CreateAccountSerializer, \
    CreateAccountByOwnerSerializer, ReactionSerializer, ReactionChangeSerializer, CommentSerializer, \
    CommentChangeSerializer
from rest_framework import status
from core.api.serializers import APIRegisterUserSerializer
from rest_framework.viewsets import ModelViewSet
from core.models import Post, PostCategory, PostReaction, PostComment
from django_filters.rest_framework import DjangoFilterBackend
import core.permissions
from account.models import Account
from django.contrib.auth import login

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


class APIRegisterUser(APIView):
    def post(self, request):
        serialized_user_data = APIRegisterUserSerializer(data=request.data)
        serialized_user_data.is_valid(raise_exception=True)

        new_user_object = serialized_user_data.create(serialized_user_data.validated_data)
        serialized_user = UserSerializer(new_user_object)

        return JsonResponse(serialized_user.data)


class PostViewSet(ModelViewSet):
    lookup_field = 'pk'
    queryset = Post.objects.all()
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
            return MakePostSerializer
        elif self.request.method == 'GET':
            return PostSerializer

    def create(self, request, *args, **kwargs):
        create_serializer = self.get_serializer_class()(data=request.data, context={'request': self.request})
        create_serializer.is_valid(raise_exception=True)
        new_post_object = create_serializer.save()
        headers = self.get_success_headers(create_serializer.data)

        show_serializer = PostSerializer(new_post_object)

        return Response(show_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostCategoryViewSet(ModelViewSet):
    serializer_class = PostCategorySerializer
    lookup_field = 'id'
    queryset = PostCategory.objects.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = [core.permissions.PostCategoryPermission]
    filter_fields = ['name', 'id']


class AccountViewSet(ModelViewSet):
    permission_classes = [core.permissions.AccountPermission]
    serializer_class = PublicAccountSerializer
    queryset = Account.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['is_owner', 'is_staff', 'is_admin', 'username']
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.username == request.user.username:
            serializer = self.get_serializer(instance)
        else:
            serializer = PrivateAccountSerializer(instance)

        return Response(serializer.data)

    def get_serializer_class(self):
        special_permission = False
        user = self.request.user
        if not self.request.user.is_anonymous:
            if any([user.is_owner, user.is_staff, user.is_admin]):
                special_permission = True

        if self.request.method in ('POST', 'PUT'):
            if special_permission:
                return CreateAccountByOwnerSerializer
            else:
                return CreateAccountSerializer
        elif self.request.method == 'GET':
            if special_permission:
                return PrivateAccountSerializer
            else:
                return PublicAccountSerializer

    def filter_queryset(self, queryset):
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        queryset = limit_filter(self.request, queryset)

        return super().filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        create_serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        create_serializer.is_valid(raise_exception=True)
        user = create_serializer.save()

        headers = self.get_success_headers(create_serializer.data)

        login(request, user)

        return Response(create_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer_class()(instance, data=request.data, partial=partial,
                                                 context={'request': request})

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class MyAccountViewSet(ModelViewSet):
    serializer_class = PrivateAccountSerializer
    queryset = Account.objects.all()
    permission_classes = [core.permissions.MyAccountPermission]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        special_permission = False
        user = self.request.user

        if not self.request.user.is_anonymous:
            if any([user.is_owner, user.is_staff, user.is_admin]):
                special_permission = True

        if self.action in ('create', 'partial_update'):
            if special_permission:
                return CreateAccountByOwnerSerializer
            else:
                return CreateAccountSerializer
        else:
            return PrivateAccountSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.username == request.user.username:
            serializer = self.get_serializer(instance)
        else:
            serializer = PrivateAccountSerializer(instance)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer_class()(instance, data=request.data, partial=True,
                                                 context={'request': request})

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class ReactionsViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = ReactionSerializer
    queryset = PostReaction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['author', 'post', 'reaction']
    permission_classes = [core.permissions.PostReactionPermission]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ReactionChangeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        duplicate = PostReaction.objects.filter(author=self.request.user, post=serializer.validated_data.get('post'))

        if duplicate.exists():
            raise ValidationError('Reaction to this post already exist')

        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = CommentSerializer
    queryset = PostComment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['author', 'post']
    permission_classes = [core.permissions.PostCommentPermission]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return CommentChangeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=serializer.validated_data.get('post'))
