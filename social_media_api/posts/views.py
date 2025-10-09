from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Like
from notifications.models import Notification


class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the post author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post,
            )

        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            return Response({"detail": "You haven’t liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)
