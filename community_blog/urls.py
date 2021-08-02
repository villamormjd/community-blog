from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from blog import views

router = routers.DefaultRouter()
router.register("posts", views.PostViewSet, basename="posts")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include(router.urls)),
    path('api/posts/delete/<int:pk>', views.DeletePostDetail.as_view(), name='delete-post'),
    path('api/me/posts/', views.ListLoggedInUserView.as_view(), name='list-user-post'),

    # comments
    path('api/posts/<int:blog_id>/comments/', views.CommentListView.as_view(), name='comment'),
    path('api/posts/<int:blog_id>/comments/<int:pk>', views.CommentDetailView.as_view(), name='comment'),

    # jwt
    path('api/gettoken/', TokenObtainPairView.as_view(), name='gettoken'),
    path('api/refresh_token/', TokenRefreshView.as_view(), name='refresh_token')
]
