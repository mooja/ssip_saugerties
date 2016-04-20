from django.db import models

# Create your models here.
class Member(models.Model):

    # basic information
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    birthday = models.CharField(max_length=200, null=True, blank=True)

    # contact information
    town = models.CharField(max_length=400, null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    zipcode = models.CharField(max_length=400, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    homephone = models.CharField(max_length=20, null=True, blank=True)
    cellphone = models.CharField(max_length=20, null=True, blank=True)

    # prefernces
    occupation = models.CharField(max_length=1500, null=True, blank=True)
    hobbies = models.CharField(max_length=1500, null=True, blank=True)
    canhelp = models.CharField(max_length=1500, null=True, blank=True)
    needhelp = models.CharField(max_length=1500, null=True, blank=True)
    comments = models.TextField(max_length=5000, null=True, blank=True)

    def get_full_name(self):
        return " ".join([self.first_name, self.last_name])

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['last_name']

