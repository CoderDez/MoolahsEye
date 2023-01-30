from __future__ import annotations
from typing import Union
from django.db import models
from django.contrib.auth.hashers import make_password, check_password 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from exceptions import model_exceptions as mdlexc

class Budget(models.Model):

    # options for frequency field
    frequencies = (
        (7, "weekly"),
        (30, "monthly")
    )
    name = models.CharField(max_length=40, default="New Budget", null=False, blank=False)
    amount = models.FloatField(default=0.0, null=False, blank=False)
    frequency = models.IntegerField(null=False, default=7, choices=frequencies)

    def __str__(self):
        return self.name

    def get_frequency(self, str_rep: True) -> Union[int, str]:
        """returns the Budget objects frequency.

        if str_rep == True:
            frequency is returned as str representation
        else:
            frequency is returned as int representation"""
        try:
            for freq in Budget.frequencies:
                if self.frequency in freq:
                    if str_rep:
                        return freq[1]
                    else:
                        return freq[0]
        except:
            pass


    def __is_frequency_valid(self) -> bool:
        """returns whether objects frequency field is valid.
        Value is valid if present in frequencies."""
        try:
            for freq in Budget.frequencies:
                if self.frequency in freq:
                    return True
            return False
        except:
            pass

    def __is_amount_sufficient(self) -> bool:
        """returns whether the Budget objects amount is sufficient.
        The amount is sufficient if it is greater than or equal to
        the sum of all items costs within the budget."""
        try:
            items_total = sum([i.cost for i in self.item_set.all()])
            return self.amount >= items_total
        except:
            pass

    def save(self, *args, **kwargs):
        # validate frequency
        if not self.__is_frequency_valid():
            raise mdlexc.FrequencyException()
        else:
            self.frequency = self.get_frequency(str_rep=False)
        #validate amount
        if not self.__is_amount_sufficient(self):
            raise mdlexc.InsufficientAmountException()
        super(Budget, self).save(*args, **kwargs)

    
class Item(models.Model):
    # options for frequency field
    frequencies = (
        (1, "daily"),
        (7, "weekly"),
        (30, "daily")
    )

    budget_id = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, default="New Item", null=False, blank=False)
    amount = models.FloatField(default=0.0, null=False, blank=False)
    frequency = models.IntegerField(null=False, default=7, choices=frequencies)

    def __str__(self):
        return self.name

    def get_frequency(self, str_rep: True) -> Union[int, str]:
        """returns the Budget objects frequency.

        if str_rep == True:
            frequency is returned as str representation
        else:
            frequency is returned as int representation"""
        try:
            for freq in Budget.frequencies:
                if self.frequency in freq:
                    if str_rep:
                        return freq[1]
                    else:
                        return freq[0]
        except:
            pass

    def __is_frequency_valid(self) -> bool:
        """returns whether objects frequency field is valid.
        Value is valid if present in frequencies and does not exceed 
        budgets frequency."""
        try:
            for freq in Budget.frequencies:
                if self.frequency in freq:
                    return self.budget_id.frequency >= self.frequency
            return False
        except:
            pass


    def save(self, *args, **kwargs):
        if not self.__is_frequency_valid():
            mdlexc.FrequencyException()
        else:
            self.frequency = self.get_frequency(str_rep=False)
        super(Item, self).save(*args, **kwargs)
        # performs additional validation relating to the amount
        self.budget_id.save()


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, name, user_name, password, **other_fields):
        if not email:
            raise ValueError(("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, user_name=user_name, **other_fields) 

        user.save()
        return user

    def create_superuser(self, email, user_name, name, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(
            email=email, user_name=user_name, name=name, password=password,**other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """class to represent User of the system.
    
    fields:
    - name: models.ChatField
    - user_name: models.CharField
    - email: models.CharField
    - password: models.CharField
    - is_staff: models.BooleanField
    - is_active: models.BooleanField
    - objects: CustomAccountManager instance
    - USERNAME_FIELD : str
    - REQUIRED_FIELDS: list

    methods:
    - get_user(cls, email: str, password: str) -> User | None"""

    name = models.CharField(max_length=40, null=False, blank=False)
    user_name = models.CharField(max_length=40, unique=True, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=150, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'name','password']
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    @classmethod
    def get_user(cls, email: str, password: str) -> Union[User, None]:
        """returns a User object if both email and password match a User objects
        credentials, else None."""
        try:
            user = User.objects.get(email = email)
            if check_password(password, user.password):
                return user
            else: 
                return None
        except:
            return None



