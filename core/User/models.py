from django.db import models

# Create your models here.
class UserApp_TB(models.Model):
    user_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    is_militar = models.BooleanField(default=True)
    timeCreated = models.DateTimeField(auto_now_add=True)
    is_temporal = models.BooleanField(default=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=100, unique=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return f"{self.user_id} - {self.name} {self.last_name} - {self.username}"
    

class TypeDocument_TB(models.Model):
    name_type_document = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name_type_document}"

class UserDocument_TB(models.Model):
    user_id = models.OneToOneField(UserApp_TB, on_delete=models.CASCADE)
    document = models.CharField(max_length=20, unique=True)
    type_document = models.ForeignKey(TypeDocument_TB, on_delete=models.PROTECT)
    place_expedition = models.CharField(max_length=60)
    date_expedition = models.DateField()
    
    def __str__(self):
        return f"{self.type_document.name_type_document}: {self.document} - {self.user_id.name} {self.user_id.last_name}"
    


class Country_TB(models.Model):
    country_code = models.CharField(max_length=4)
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name
    
class ContactInfo_TB(models.Model):
    user_id = models.OneToOneField(UserApp_TB, on_delete=models.CASCADE, related_name='contact')
    address = models.CharField(max_length=60)
    country_id = models.ForeignKey(Country_TB, on_delete=models.PROTECT)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    cel_phone = models.CharField(max_length=20)
    emergency_name = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user_id.name} {self.user_id.last_name}: {self.phone} - {self.address}"

