from django.contrib import admin
from mailinglist.models import *

admin.site.register(MailingList)
admin.site.register(Message)
admin.site.register(Subscriber)
admin.site.register(Books)
