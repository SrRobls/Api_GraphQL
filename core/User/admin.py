from django.contrib import admin

from User.models import UserApp_TB, UserDocument_TB, TypeDocument_TB, Country_TB, ContactInfo_TB

# Register your models here.
admin.site.register(UserApp_TB)
admin.site.register(UserDocument_TB)
admin.site.register(TypeDocument_TB)
admin.site.register(Country_TB)
admin.site.register(ContactInfo_TB)
