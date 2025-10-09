from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from .models import Post, Like
from notifications.models import Notification


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """
    Allows a user to like a post.
    Creates a notification for the post author if liked by another user.
    """
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        return Response({'message': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a notification if the user is not the author
    if post.author != user:
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb='liked your post',
            target=post
        )

    return Response({'message': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """
    Allows a user to unlike a post.
    Removes the like if it exists.
    """
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    like = Like.objects.filter(user=user, post=post).first()
    if not like:
        return Response({'message': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

    like.delete()
    return Response({'message': 'Post unliked successfully.'}, status=status.HTTP_200_OK)
