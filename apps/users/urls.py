from django.urls import path
from .import views


urlpatterns = [
    path('create-users', views.RegisterUserView.as_view(), name="create_user"),
    path('list-users', views.ListUserView.as_view(), name="list_users"),
    path('user-detail/<uuid:id>',views.RetrieveUserView.as_view(), name="user_detail"),
    path('update-user/<uuid:id>', views.UpdateUserView.as_view(), name="update_user"),
    path('delete-user/<uuid:id>', views.DeleteUserView.as_view(), name="delete_user"),
    path('user-login', views.UserLoginView.as_view(), name="user_login"),
    path('user-logout', views.UserLogoutView.as_view(), name="user_logout")
]
