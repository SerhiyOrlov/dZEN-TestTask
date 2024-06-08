from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, CommentReplySerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        if self.action == 'reply':
            return CommentReplySerializer
        return CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        parent_comment = get_object_or_404(Comment, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(parent=parent_comment, post=parent_comment.post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
