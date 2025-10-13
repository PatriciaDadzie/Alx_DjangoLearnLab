from rest_framework.views import APIView

# ---------------------------------------------------------------
# FEED VIEW
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

        # Fetch posts from those users
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        # Serialize and return the posts
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
