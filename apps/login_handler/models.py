from __future__ import unicode_literals
from django.db import models
import re
    

# Create your models here.
class PWmanager(models.Manager):
    def Pass_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        if len(postData['password1']) < 8:
            errors['password'] = "your password is too short"
        if len(postData['first_name']) < 3:
            errors['firs_name']= "your first name must be entered and at least 3 letters long."
        if len(postData['last_name']) < 3:
            errors['last_name'] = "your last name must be entered and at least 3 letters long"
        for user in Users.objects.all():
            if user.email == postData['email']:
                errors['existance'] = "this email is already in use."
        return errors
        

class TripManager(models.Manager):
    def validater(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "must have a title with 3 letters or more"
        if len(postData['description']) < 3:
            errors['description'] = "must have a description with 3 letters or more"
        if len(postData['location']) < 3:
            errors['location'] = "the location must have 3 characters or more"
        return errors



class Users(models.Model):
    # "Jobs" exists as a many to many key
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=48)
    last_name = models.CharField(max_length=48)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = PWmanager()
    def __repr__(self):
        return f"\n{100*'*'}\nID: {self.id}\n{self.email} : {self.password}\nfirst_name : {self.first_name}\nlast_name : {self.last_name}\n{100*'*'}"

class Jobs(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=50)
    catagory = models.TextField()
    created_by = models.ForeignKey(Users, related_name="created_trips")
    users = models.ManyToManyField(Users, related_name="jobs")
    Created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = TripManager()
    def __repr__(self):
        return f"\n\n destination: {self.destination}\nid: {self.id}\nCreated by: {self.created_by.first_name}\n\n"


