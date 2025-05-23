from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets, permissions
)
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post
from .serializers import (
    CommentSerializer, GroupSerializer,
    PostSerializer, FollowSerializer
)
from .permissions import IsAuthorOrReadOnly
from .viewsets import CustomFollowViewSet


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с группами."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(
            Post,
            pk=self.kwargs['post_id']
        )
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            pk=self.kwargs['post_id']
        )
        serializer.save(
            author=self.request.user,
            post=post
        )


class FollowViewSet(CustomFollowViewSet):
    """
    Вьюсет для работы с подписками.
    Наследуется от кастомного вьюсета.
    """

    serializer_class = FollowSerializer
