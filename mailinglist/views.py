from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.shortcuts import render
from mailinglist.models import MailingList, Subscriber
from mailinglist.mixins import UserCanUseMailingList
from mailinglist.forms import MailingListForm, SubscriberForm
from django.urls import reverse_lazy

class MailingListListView(LoginRequiredMixin, ListView):
	def get_queryset(self):
		return MailingList.objects.filter(owner=self.request.user)
class CreateMailingListView(LoginRequiredMixin, CreateView):
	form_class = MailingListForm
	template_name = 'mailinglist/mailinglist_form.html'

	def get_initial(self):
		return {
		'owner':self.request.user.id,
		}
class DeleteMailingListView(LoginRequiredMixin, UserCanUseMailingList, DeleteView):
	model =MailingList
	success_url = reverse_lazy('mailinglist:mailinglist_list')

class MailingListDetailView(LoginRequiredMixin, UserCanUseMailingList, DetailView):
	model = MailingList

class SubscribeToMailingListView(CreateView):
	form_class = SubscriberForm
	template_name = 'mailinglist/subscriber_form.html'

	def get_initial(self):
		return {
		'mailing_list': self.kwargs['mailinglist_id']
		}

	def get_success_url(self):
		return reverse('mailinglist:subscriber_thankyou',
		 kwargs={
		 'pk':self.object.mailing_list.id,
		 })

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		mailing_list_id = self.kwargs['mailinglist_id']
		ctx['mailing_list']: get_object_or_404(
			MailingList, id=mailing_list_id)
		return ctx 
		

class ThankYouForSubscribingView(DetailView):
	model = MailingList
	template_name = 'mailinglist/subscription_thankyou.html'

class ConfirmSubscriptionView(DetailView):
	model = Subscriber 
	template_name = 'mailinglist/confirm_subscription.html'

	def get_object(self, queryset=None):
		subscriber = super().get_object(queryset=queryset)
		subscriber.confirmed = True
		subscriber.save()
		return subscriber
