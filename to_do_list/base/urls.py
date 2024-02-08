from django.urls import path
# from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, CustomLogoutView, RegisterPage # used this way because of class based view
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('register/', RegisterPage.as_view(), name="register"),
    # path('logout/', LogoutView.as_view(http_method_names = ['post', 'get']), name="logout"),
    # path('logout/', CustomLogoutView.as_view(), name="logout"),
    path('logout/', CustomLogoutView.as_view(), name="logout"),
    path('', TaskList.as_view(), name="tasks"),
    path('task/<int:pk>/', TaskDetail.as_view(), name="task"),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
]

