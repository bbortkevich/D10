from django.urls import path

from .views import (
	NewsList,
	SearchPosts, NewsCreate,
	NewsUpdate, NewsDelete, subscribe_user_category, NewsDetail,
	unsubscribe_user_category, CategoryDetail, CategoriesList
)

urlpatterns = [
	path('', NewsList.as_view(), name = 'news_list'),
	path('<int:pk>/', NewsDetail.as_view(), name = 'news_detail'),
	path('search/', SearchPosts.as_view(), name = 'search_posts'),
	path('create/', NewsCreate.as_view(), name = 'news_create'),
	path('<int:pk>/delete/', NewsDelete.as_view(), name = 'news_delete'),
	path('<int:pk>/edit/', NewsUpdate.as_view(), name = 'news_update'),
	path('categories/', CategoriesList.as_view(), name = 'categories_list'),
	path('categories/<int:pk>/', CategoryDetail.as_view(), name = 'category_detail'),



	path('subscribe/<str:cat_name>', subscribe_user_category,
		 name = 'subscribe_category'),
	path('unsubscribe/<str:cat_name>', unsubscribe_user_category,
		 name = 'unsubscribe_category'),

]
