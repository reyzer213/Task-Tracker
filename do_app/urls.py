from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Список завдань
    path('', TaskListView.as_view(), name='task_list'),  

    # Деталі завдання
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),  

    # Створення нового завдання
    path('task/new/', TaskCreateView.as_view(), name='task_create'),

    # Редагування завдання
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),

    # Видалення завдання
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),

    # Реєстрація
    path('signup/', SignUpView.as_view(), name='signup'),

    # Вихід з акаунту
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # коменти
    
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),

    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    path('comment/<int:comment_id>/like/', like_comment, name='like_comment'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 



#if settings.DEBUG:
#    urlpatterns += patterns('',
#        url(r'^media/(?P<path>.*)$',
#           'django.views.static.serve',
#            {'document_root': settings.MEDIA_ROOT, }),
#    )



#path('project/<int 😛 k>/',  
# ProjectDetailView.as_view(), 
#  name='project_detail') 
