from django.db import models
import re
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # password = (postData['confirm'])
        # if password.match(postData['password'])
            # errors['password']= "Passwords should match"
        if len(postData['fname']) < 2:
            errors['fname'] = "First name should be longer than two characters"
        if len(postData['lname']) < 2:
            errors['lname'] = "last name should be longer than two characters"
        if len(postData['user_name']) < 4:
            errors['user_name'] = "username must be at least 4 characters long!"
        if len(postData['email']) < 3:        
            errors['email'] = "Email should be at least 3 characters long!"
        if len(postData['password']) < 2: 
            errors['password'] = "password should be longer than two characters"
        if postData['password'] != postData['confirm']: 
            errors['cofirm_password'] = "Passwords should match"
        for user in User.objects.all():
            if postData['email'] == user.email:
                errors['email'] = 'Email already in use'
        # if len(postData['pfp'])<1:
        #     errors['pfp']='Please select a profile picture'
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email!'   # test whether a field matches the pattern 
        if len(postData['password']) < 2:
            errors['password'] = "Invalid password!"

        return errors

    def create_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Title must be more than 1 character!!!"
        if len(postData['episode'])<1:
            errors['episode'] = "Please enter an episode!"
        if len(postData['season'])<1:
            errors['season'] = "Please enter a season!"
        if len(postData['rating'])<1:
            errors['rating'] = "Please enter a rating!"
        return errors

    def edit_anime_validator(self, postData):
        errors={}
        if len(postData['episode'])<1:
            errors['episode'] = "Please enter an episode!"
        if len(postData['season'])<1:
            errors['season'] = "Please enter a season!"
        if len(postData['rating'])<1:
            errors['rating'] = "Please enter a rating!"
        return errors

    def edit_user_validator(self, postData):
        errors={}
        user=(User.objects.get(id=postData['user_id']))
        if postData['user_name']:
            if len(postData['user_name'])<4:
                errors['user_name']='New username must be greater than four characters'
            if postData['user_name'] == user.user_name:
                errors['user_name']='New username can not be the same as your current username'
        if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            errors['password']='New password can not be the same as your current password'
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    pfp = models.TextField()
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Anime(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True,blank=None, default=None)
    end_date = models.DateTimeField(null=True,blank=None, default=None)
    season = models.IntegerField()
    episode = models.IntegerField(default=1)
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="animes", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





