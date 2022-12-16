from celery import shared_task
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import  get_object_or_404
from .tasks import hello
from django.urls import reverse_lazy

from django.views.generic import (
	CreateView, DeleteView,
	DetailView, ListView,
	UpdateView
)


from .models import Post, Category, SubscribersCategory

from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin, \
	PermissionRequiredMixin


class NewsList(ListView):
	model = Post
	template_name = 'news_list.html'
	context_object_name = 'news_list'
	queryset = Post.objects.order_by('-date')
	paginate_by = 10


class SearchPosts(ListView):
	paginate_by = 10
	model = Post
	ordering = 'date'
	template_name = 'search.html'
	context_object_name = 'news'

	def get_queryset(self):
		queryset = super().get_queryset()
		self.filterset = PostFilter(self.request.GET, queryset)
		return self.filterset.qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search_filter'] = self.filterset
		return context


class NewsDetail(DetailView):
	model = Post
	template_name = 'news_detail.html'
	context_object_name = 'news'


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
	form_class = PostForm
	model = Post
	template_name = 'news_edit.html'
	success_url = reverse_lazy('news_list')
	permission_required = ('news.add_post')

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		context['page_title'] = "Добавить материал"
		return context


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
	form_class = PostForm
	model = Post
	template_name = 'news_edit.html'
	permission_required = ('news.change_post')

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		context['page_title'] = "Редактировать материал"
		return context


class NewsDelete(PermissionRequiredMixin, DeleteView):
	model = Post
	template_name = 'news_delete.html'
	success_url = reverse_lazy('news_list')
	permission_required = ('news.delete_post')

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		context['page_title'] = "Удалить материал"
		context['previous_page_url'] = reverse_lazy('news_list')
		return context


@login_required
def subscribe_user_category(request, cat_name):
	category_obj = get_object_or_404(Category, category_name = cat_name)
	SubscribersCategory.objects.get_or_create(subscriber = request.user,
											  category = category_obj)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_user_category(request, cat_name):
	category_obj = get_object_or_404(Category, category_name = cat_name)
	subscribe = SubscribersCategory.objects.filter(subscriber = request.user,
												   category = category_obj).first()
	if subscribe:
		subscribe.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CategoryDetail(DetailView):
	model = Category
	template_name = 'category_detail.html'
	context_object_name = 'category'


class CategoriesList(ListView):
	model = Category
	template_name = 'categories_list.html'
	context_object_name = 'categories_list'

