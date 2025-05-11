from django.contrib import admin

from User.models import UserApp_TB, UserDocument_TB, TypeDocument_TB, Country_TB, ContactInfo_TB

# Register your models here.
@admin.register(UserApp_TB)
class UserAppAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserApp_TB._meta.fields]
admin.site.register(UserDocument_TB)
admin.site.register(TypeDocument_TB)
admin.site.register(Country_TB)
admin.site.register(ContactInfo_TB)
