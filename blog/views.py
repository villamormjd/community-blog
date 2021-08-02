from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import BlogSerializers, CommentSerializer
from .models import Blogs, Comment
from utility.helpers import validate_decoded_token, decode_jwt_token


class PostViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_objects(self, pk=None):
        try:
            queryset = Blogs.objects.all()
            return queryset
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        response = dict()
        blogs = self.get_objects()
        paginator =PageNumberPagination()
        result_page =paginator.paginate_queryset(blogs, request)
        serializer = BlogSerializers(result_page, many=True, context={'request': request})
        response['error'] = False
        response['message'] = 'Retrieved all posts list.'
        response["count"] = blogs.count()
        response['data'] = serializer.data

        return Response(response)

    def create(self, request):
        response = dict()
        request.data['author_id'] = decode_jwt_token(request)['user_id']
        try:
            serializer = BlogSerializers(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response['error'] = False
            response['message'] = 'Post has been created!'
            response['data'] = serializer.data
        except:
            response['error'] = True
            response['message'] = 'Error Creating Post!'

        return Response(response)

    def retrieve(self, request, pk=None):
        response = dict()
        queryset = Blogs.object.all()
        blog = get_object_or_404(queryset, pk=pk)
        serializer = BlogSerializers(blog, context={'request': request})
        response['error'] = False
        response['message'] = 'Fetched single blog post.'
        response['data'] = serializer.data

        return Response(response)

    def update(self, request, pk=None):
        response = dict()

        queryset = Blogs.object.all()
        blog = get_object_or_404(queryset, pk=pk)
        response['error'] = False
        response['message'] = 'Post has been successfully updated!'

        if not validate_decoded_token(request, blog):
            response['error'] = True
            response['message'] = 'Unauthorized to update this post!'

        if not response['error']:
            serializer = BlogSerializers(blog, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response['data'] = serializer.data

        return Response(response)


class DeletePostDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, pk=None):
        response = dict()
        response['error'] = False
        response['message'] = 'Post has been Deleted!'
        blog = Blogs.object.filter(pk=pk).first()
        if not blog:
            response['message'] = 'Post no found or has been removed.'

        if not validate_decoded_token(request, blog):
            response['error'] = True
            response['message'] = 'Unauthorized to delete this post!'

        if not response['error']:
            blog.delete()

        return Response(response)


class ListLoggedInUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        response = dict()
        response['error'] = False
        response['message'] = 'Fetched logged in User Posts!'
        decodedToken = decode_jwt_token(request)
        blogs = Blogs.object.filter(author_id=decodedToken['user_id'])

        serializer = BlogSerializers(blogs, many=True, context={'request': request})

        if blogs.count() == 0:
            response['error'] = True
            response['message'] = 'You haven\'t created blog for a while!'

        response['data'] = serializer.data

        return Response(response)

###### COMMENT VIEWS ####

class CommentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, blog_id=None):

        response = dict()

        request.data['blog_id'] = blog_id
        request.data['comment_author_id'] = decode_jwt_token(request)['user_id']
        try:
            serializer = CommentSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response['error'] = False
            response['message'] = "Comment has been created!"
            response["data"] = serializer.data
        except:
            response['error'] = True
            response['message'] = "Error adding comment."

        return Response(response)


    def get(self, request, blog_id=None):
        paginator = PageNumberPagination()

        response = dict()
        response["error"] = False
        response["message"] = "Retrieved comments for this blog."
        comments = Comment.objects.filter(blog_id=blog_id)
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(result_page, many=True, context={'request': request})
        response["count"] = len(comments)
        response["data"] = serializer.data

        return Response(response)


class CommentDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, blog_id=None, pk=None):
        response = dict()
        comments = Comment.objects.all()
        comment = get_object_or_404(comments, pk=pk)
        serializers = CommentSerializer(comment, context={"request": request})
        response["error"] = False
        response["message"] = "Retrieved single comment."
        response["data"] = serializers.data

        return Response(response)

    def put(self, request, blog_id=None, pk=None):
        response = dict()
        response["error"] = False
        response["message"] = "Comment has been Updated!"
        comment = Comment.objects.get(pk=pk)

        if comment.comment_author_id.id != decode_jwt_token(request)['user_id']:
            response["error"] = True
            response["message"] = "Unauthorized to edit this comment!"

        if not response["error"]:
            serializer = CommentSerializer(comment, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response["data"] = serializer.data

        return Response(response)

    def delete(self, request, blog_id=None, pk=None):
        response = dict()
        response["error"] = False
        response["message"] = "Comment has been Deleted!"
        comment = Comment.objects.get(pk=pk)
        allowed_delete = [comment.comment_author_id.id, comment.blog_id.author_id.id]
        if decode_jwt_token(request)['user_id'] not in allowed_delete:
            response["error"] = True
            response["message"] = "Unauthorized to delete this comment!"

        if not response["error"]:
            comment.delete()

        return Response(response)
