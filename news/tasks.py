from celery import shared_task
import time
import datetime

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from NewsPortal.settings import EMAIL_FROM_COMPLETE
from news.models import Post, Category


@shared_task
def hello():
	time.sleep(10)
	print("Hello, world!")



@shared_task
def send_new_post_to_subscriber_category(category_name,news_id, news_title, news_text, subscriber_email, subscriber_username):

	html_content = render_to_string(
		'emails_template/notification_new_news_category_celery.html',
		{
			'username': subscriber_username,
			'category_name': category_name,
			'news_text': news_text,
			'news_title': news_title,
			'news_id': news_id,
		}
	)
	msg = EmailMultiAlternatives(
		subject = f'Новая статья в твоём любимом разделе {category_name}',
		body = news_text[:50],
		from_email = EMAIL_FROM_COMPLETE,
		to = [subscriber_email],
	)
	msg.attach_alternative(html_content,
						   "text/html")

	msg.send()


@shared_task
def sending_week_newsletters_celery():
	time_delta = datetime.timedelta(7)
	start_date = datetime.datetime.utcnow() - time_delta
	end_date = datetime.datetime.utcnow()
	posts = Post.objects.filter(date__range = (start_date, end_date))
	print(time_delta)
	print(start_date)
	print(end_date)
	print(posts)
	for category in Category.objects.all():
		html_content = render_to_string(
			'emails_template/weekly_send_newsletter.html',
			{
				'posts': posts,
				'category': category
			}
		)
		msg = EmailMultiAlternatives(
			subject = f'Еженедельные новости по любимой категории: {category.category_name}',
			body = 'Новости за неделю по категории, которую вы подписаны!',
			from_email = EMAIL_FROM_COMPLETE,
			to = category.get_all_subscribers_emails(),
		)
		msg.attach_alternative(html_content,
							   "text/html")
		msg.send()
