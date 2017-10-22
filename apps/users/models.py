from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime, date
from django.utils import timezone

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
DATE_REGEX = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')

class UserManager(models.Manager):
    def user_validation(self, postdata):
        errors = {}
        if len(postdata['first_name']) < 2:
            errors['first_name'] = "First name must be at lease 2 characters long"
        if len(postdata['last_name']) < 2:
            errors['last_name'] = "Last name must be at lease 2 characters long"
        if len(postdata['email']) < 1 or not EMAIL_REGEX.match(postdata['email']):
            errors['email'] = "Email must be valid"
        if User.objects.exists(postdata['email']):
            errors['email'] = "Email already in use"
        if len(postdata['password']) < 8:
            errors['password'] = "Password must be 8 characters long"
        if not DATE_REGEX.match(postdata['dob']):
            errors['date'] = "Date in wrong format, (YYYY-MM-DD)"
        if not postdata['password'] == postdata['confirm']:
            errors['confirm'] = "Password and confirm password must match"
        return errors
    def info_validation(self, postdata):
        errors = {}
        if len(postdata['first_name']) < 2:
            errors['first_name'] = "First name must be at lease 2 characters long"
        if len(postdata['last_name']) < 2:
            errors['last_name'] = "Last name must be at lease 2 characters long"
        if len(postdata['email']) < 1 or not EMAIL_REGEX.match(postdata['email']):
            errors['email'] = "Email must be valid"
        return errors
    def password_validation(self, postdata):
        errors = {}
        if len(postdata['password']) < 8:
            errors['password'] = "Password must be 8 characters long"
        if not postdata['password'] == postdata['confirm']:
            errors['confirm'] = "Password and confirm password must match"
        return errors
    def exists(self, email):
        try:
            user_check = User.objects.get(email=email)
        except:
            return False
        return True
    def id_exists(self, _id):
        try:
            user_check = User.objects.get(id=_id)
        except:
            return False
        return True


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    dob = models.DateField(default=timezone.now)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Friendship(models.Model):
    friend_a = models.ForeignKey(User, related_name="friend_a")
    friend_b = models.ForeignKey(User, related_name="friend_b")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
