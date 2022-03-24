from django.contrib import admin

from .models import ReferralUser, SMSCode


admin.site.register(ReferralUser)
admin.site.register(SMSCode)
