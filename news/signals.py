
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .tasks import send_new_post_to_subscriber_category
from django.template.loader import render_to_string

from NewsPortal.settings import EMAIL_FROM_COMPLETE
from news.models import Post, SubscribersCategory


@receiver(m2m_changed, sender = Post.categories.through)
def notify_subscribers_category(sender, instance, **kwargs):
	post_obj = instance
	categories_objs = post_obj.categories.all()
	for category in categories_objs:
		sub_cat_rows = SubscribersCategory.objects.filter(
			category = category.id).select_related()
		print(sub_cat_rows, 'subscribers')
		for row in sub_cat_rows:
			subscriber_username_to_send = row.subscriber.username
			subscriber_email_to_send = row.subscriber.email
			category_name = category.category_name
			news_title = instance.title
			news_text = instance.text
			news_id = instance.id
			if subscriber_email_to_send:
				send_new_post_to_subscriber_category.delay(
					category_name,
					news_id,
					news_title,
					news_text,
					subscriber_email_to_send,
					subscriber_username_to_send)

