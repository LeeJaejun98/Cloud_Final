from . import views
from django.urls import path

urlpatterns = [

    path('', views.PostList.as_view()),
    path('search_title/<str:q>/', views.PostSearch.as_view()),
    path('search/<str:month>/<str:year>/<str:day>/', views.find_by_date),
    path('create_post/', views.PostCreate.as_view()),
    path('post_update/<int:pk>/', views.PostUpdate.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/add_comment/', views.add_comment),
    path('category/<str:slug>/', views.categories_page),
    path('tag/<str:slug>/', views.tag_page),
]
