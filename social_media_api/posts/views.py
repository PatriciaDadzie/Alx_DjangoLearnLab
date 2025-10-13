from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


# ---------------------------------------------------------------
# PERMISSIONS
# ---------------------------------------------------------------
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners to edit/delete their own posts/comments.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# ---------------------------------------------------------------
# CRUD VIEWSETS FOR POSTS & COMMENTS
# ---------------------------------------------------------------
class PostViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ---------------------------------------------------------------
# LIKE / UNLIKE VIEWS
# ---------------------------------------------------------------
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


# ---------------------------------------------------------------
# FEED VIEW (Checker-specific)
# ---------------------------------------------------------------
class FeedView(APIView):
    """
    Returns a feed of posts from users the current user follows,
    ordered by creation date (most recent first).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get all users the current user follows
        following_users = request.user.following.all()  

        # Fetch posts from followed users ordered by most recent first
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')  

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
