# from django.contrib import admin
# from .models import *
# # Register your models here.

# admin.site.register(Language)

from django.contrib import admin
from .models import *
# Register your models here.

class CaseAdmin(admin.ModelAdmin):
	pass

class SightingAdmin(admin.ModelAdmin):
	pass

class  FAQAdmin(admin.ModelAdmin):
    pass

class AboutUsAdmin(admin.ModelAdmin):
    pass 

class TeamAdmin(admin.ModelAdmin):
    pass 

class PrivacyPolicyAdmin(admin.ModelAdmin):
    pass
	# list_display = ["__str__", "begin_date", "location"]
	# class Meta:
	# 	model = Event

admin.site.register(Case, CaseAdmin)
admin.site.register(Sighting, SightingAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)