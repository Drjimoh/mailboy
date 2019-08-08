from django.db import models
import uuid 
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Books(models.Model):
	id = models.IntegerField(primary_key=True, editable=False)
	bookman = models.OneToOneField(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, blank=False, null=False)
	author = models.CharField(max_length=100, blank=False, null=False)
	location = models.CharField(max_length=100, blank=False, null=False, 
		default='Nigeria')


	def __str__(self):
		return str(self.title) + ' by ' + str(self.author)

class MailingList(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=140)
	owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse(
			'mailinglist:manage_mailinglist',
			kwargs={'pk':self.id}
			)
	def user_can_use_mailing_list(self, user):
		return user == self.owner

class Subscriber(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,
		editable=False)
	email = models.EmailField()
	confirmed = models.BooleanField(default=False)
	mailing_list = models.ForeignKey(to=MailingList,on_delete=models.CASCADE)

	class Meta:
		unique_together = ['email', 'mailing_list',]

class Message(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,
		editable=False)
	mailing_list = models.ForeignKey(to=MailingList, on_delete=models.CASCADE)
	subject = models.CharField(max_length=140)
	body = models.TextField()
	started = models.DateTimeField(default=None, null=True)
	finished = models.DateTimeField(default=None, null=True)


