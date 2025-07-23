# tracker/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 当用户访问应用的根路径时，调用 views.book_list 函数
    path('', views.book_list, name='book_list'),

    # 新增：书籍详情页的URL
    # <int:book_id> 是一个“路径转换器”，它会捕获URL中一个整数，并把它作为名为 book_id 的参数传给视图函数
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    # 新增：添加书籍页面的URL
    path('add_book/', views.add_book, name='add_book'),

    # 新增：登录页面的URL
    # 我们直接使用Django内置的LoginView，并告诉它使用我们自己创建的模板
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),

    # 新增：登出功能的URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 新增：注册页面的URL
    path('register/', views.register, name='register'),

    # 新增：修改阅读记录页面的URL
    # log_id 将会作为参数传递给我们的视图函数
    path('log/<int:log_id>/edit/', views.edit_log, name='edit_log'),

    # 新增：删除阅读记录的URL
    path('log/<int:log_id>/delete/', views.delete_log, name='delete_log'),

 # 新增：修改书籍状态的URL
    path('book/<int:book_id>/change_status/', views.change_book_status, name='change_book_status'),

 # 新增：删除书籍的URL
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),

]


