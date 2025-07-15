from django.contrib import admin

# Register your models here.

from django.contrib.admin import AdminSite

class NoLogAdminSite(AdminSite):
    def log_addition(self, request, object, message):
        pass
    def log_change(self, request, object, message):
        pass
    def log_deletion(self, request, object, object_repr):
        pass

custom_admin_site = NoLogAdminSite(name="no_log_admin")

# admin.site.unregister(CustomUser)
# admin.site.unregister(Group)