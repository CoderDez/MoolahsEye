from __future__ import annotations
from typing import Union
from django.db import models
from django.contrib.auth.hashers import make_password, check_password 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from email_validator import validate_email, EmailNotValidError
from .exceptions import model_exceptions as mdlexc
from .utils import utils as ut


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, name, user_name, password, **other_fields):
        if not email:
            raise ValueError(("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, user_name=user_name, password=password, **other_fields) 

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
    - get_budgets(self) -> Queryset"""

    name = models.CharField(max_length=40, unique=True, null=False, blank=False)
    user_name = models.CharField(max_length=40, unique=True, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=150, null=False, blank=False)
    instantiated = models.BooleanField(null=False, default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'name','password']
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        #validate_email(self.email)
        if not self.instantiated:
            if not ut.is_password_valid(self.password):
                raise mdlexc.PasswordValueException()
            else:
                self.password = make_password(self.password)
                self.instantiated = True
        super(User, self).save(*args, **kwargs)

    def get_budgets(self) -> models.QuerySet:
        """returns all Budget objects associated with the user.
        
        Queryset is in alphabethical order."""
        try:
            return self.budget_set.all().order_by(models.functions.Lower('name'))
        except Exception as e:
            return models.QuerySet()
        

class Budget(models.Model):
    # options for frequency field
    frequencies = (
        (2, "weekly"),
        (3, "bi-weekly"),
        (4, "monthly")
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=40, default="New Budget", null=False, blank=False, unique=True)
    amount = models.FloatField(default=0.0, null=False, blank=False)
    frequency = models.IntegerField(null=False, default=7, choices=frequencies)

    def __str__(self):
        return self.name

    def __is_frequency_valid(self) -> bool:
        """returns whether objects frequency field is valid.
        Value is valid if present in frequencies."""
        try:
            for freq in Budget.frequencies:
                if self.frequency in freq:
                    return True
            return False
        except:
            return False

    def __is_amount_sufficient(self) -> bool:
        """returns whether the Budget object's amount is sufficient.
        The amount is sufficient if it is greater than or equal to
        the sum of all items costs within the budget."""
        try:
            return self.amount >= self.get_total_costs()
        except:
            return False

    def __is_amount_positive(self) -> bool:
        """Returns True if amount is 0 or greater, else False."""
        try:
            return self.amount >= 0
        except:
            return False

    def __are_items_frequency_exceeding(self) -> bool:
        """Returns True if any item frequencies within the Budget are exceeding 
        the Budgets frequency."""
        try:
            for item in self.item_set.all():
                if item.frequency > self.frequency:
                    return True
            return True
        except:
            return False

    def get_frequency(self, str_rep: bool = True) -> Union[int, str]:
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
    
    def get_frequencies(str_rep: bool = True) -> list:
        """returns list of Budget frequency options."""
        try:
            if str_rep:
                return [freq[1] for freq in Budget.frequencies]
            else:
                return [freq[0] for freq in Budget.frequencies]
        except:
            pass

    def get_daily_amount(self) -> float:
        """returns a given Budgets daily amount."""
        try:
            if self.frequency == 2:
                return self.amount / 7
            elif self.frequency == 3:
                return self.amount / 14
            elif self.frequency == 4:
                return (self.amount * 12) / 365
        except Exception as e:
            print(e)
            return 0.0
            
    def get_total_costs(self) -> float:
        """returns the total costs of all items converted to the budgets frequency."""
        try:
            return round(sum([item.get_real_cost() for item in self.item_set.all()]), 2)
        except Exception as e:
            print(e)
            return 0

    def save(self, *args, **kwargs):
        # ensure amount is positive
        if not self.__is_amount_positive():
            raise mdlexc.NegativeValueException("Budget Amount can not be negative.")

        # validate frequency
        if not self.__is_frequency_valid():
            raise mdlexc.InvalidFrequencyException()
        
        # set frequency to int representation.
        self.frequency = self.get_frequency(str_rep=False)

        # validate amount if primary key generated (object has been instantiated)
        if self.pk:
            if not self.__are_items_frequency_exceeding():
                raise mdlexc.FrequencyExceedanceException()
            if not self.__is_amount_sufficient():
                raise mdlexc.InsufficientBudgetAmountException()
        super(Budget, self).save(*args, **kwargs)

    def get_categorical_breakdown(self):
        try:
            total = 0
            breakdown = {cat.name: {"cost": 0, "perc": 0} for cat in Category.objects.all()}
            for item in self.item_set.all():
                item_cost = item.get_real_cost()
                total += item_cost
                breakdown[item.category.name]["cost"] += item_cost
            
            other = self.amount - total
            if other:
                breakdown["Available"] = {
                    "cost": other,
                    "perc": 0
                }

            for cat in breakdown:
                breakdown[cat]["cost"] = round(breakdown[cat]["cost"], 2)
                breakdown[cat]["perc"] = round((breakdown[cat]["cost"] / self.amount) * 100, 2)
            
            return breakdown
        except Exception as e:
            print(e)
            pass
    
    def get_items_by_cost(self, desc=True):
        try:
            if desc:
                return self.item_set.order_by('-cost')
            else:
                return self.item_set.order_by('cost')
        except Exception as e:
            print(e)
            pass
    

    def get_data_points(self):
        """Returns a dict containing important data about a budget.
        
        key-value pairs of dict being returned:
           "Daily Costs": float, 
           "Weekly Costs": float, 
           "Monthly Costs": float"""
        try:
            ret = {
                "Daily Costs": 0, 
                "Weekly Costs": 0, 
                "Monthly Costs": 0
            }
            
            items = self.item_set.all()
            if items:
                for item in items:
                    ret["Daily Costs"] += item.get_daily_cost()
                    ret["Weekly Costs"] += item.get_weekly_cost()
                    ret["Monthly Costs"] += item.get_monthly_cost()

                ret["Daily Costs"] = round(ret["Daily Costs"], 2)
                ret["Weekly Costs"] = round(ret["Weekly Costs"], 2)
                ret["Monthly Costs"] = round(ret["Monthly Costs"], 2)

            return ret
        except Exception as e:
            print(e)
            return ret
    
    def get_item_real_costs(self):
        ret = {}
        try:
            for item in self.item_set.all():
                ret[item.name] = round(item.get_real_cost(),2)
        except:
            pass
        return ret

    @classmethod
    def create_new_budget(cls, user_id: int):
        try:
            if not Budget.objects.filter("New Budget"):
                budget = Budget(user_id=user_id)
                budget.save()
            else:
                counter = 1
                while True:
                    if not Budget.objects.filter(f"New Budget ({counter})"):
                        budget = Budget(user_id=user_id, name=f"New Budget ({counter})")
                        budget.save()  
                        return budget   
                    else:
                        counter +=1 
        except:
            pass


class Category(models.Model):
    name = models.CharField(max_length=40, default="New Category", null=False, blank=False, unique=True)

    def __str__(self):
        return self.name
    
    
class Item(models.Model):
    # options for frequency field
    frequencies = (
        (1, "daily"),
        (2, "weekly"),
        (3, "bi-weekly"),
        (4, "monthly")
    )

    budget_id = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, default="New Item", null=False, blank=False)
    cost = models.FloatField(default=0.0, null=False, blank=False)
    frequency = models.IntegerField(null=False, default=7, choices=frequencies)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default=None, null=True)
    def __str__(self):
        return self.name

    def __is_frequency_value_valid(self) -> bool:
        """returns whether objects frequency field is valid.
        Value is valid if present in frequencies and does not exceed 
        budgets frequency."""
        try:
            for freq in Item.frequencies:
                if self.frequency in freq:
                    return True
        except:
            return False

    def __is_frequency_value_exceeding(self) -> bool:
        """Returns True if item frequency exceeds budget frequency, else False."""
        try:
            return self.frequency > self.budget_id.frequency
        except:
            return False
    
    def __is_item_cost_permissible(self) -> bool:
        """Returns True if cost is permissible, else False.
        
        cost is permissible if it doesn't cause the total cost
        of all items to exceed the budget's amount."""
        try:
            other_items = self.budget_id.item_set.exclude(id=self.id)
            costs = sum([i.get_real_cost() for i in other_items])
            res = (self.get_real_cost() + costs) <= self.budget_id.amount
            return res
        except Exception as e:
            print(e)
            return False

    def __is_cost_positive(self) -> bool:
        """Returns True if cost is 0 or greater, else False."""
        try:
            return self.cost >= 0
        except:
            return False

    def get_frequency(self, str_rep: bool = True) -> Union[int, str]:
        """returns the Budget objects frequency.

        if str_rep == True:
            frequency is returned as str representation
        else:
            frequency is returned as int representation"""
        try:
            for freq in Item.frequencies:
                if self.frequency in freq:
                    if str_rep:
                        return freq[1]
                    else:
                        return freq[0]
        except:
            pass

    def get_frequencies(self, str_rep: bool = True, limit:bool=False) -> list:
        """returns all possible item frequencies.
        
        if limit == True:
            return frequencies that are less than or equal to Budgets frequencies
        else:
            return all frequencies"""
        try:
            freqs = []
            for freq in Item.frequencies:
                if limit:
                    if freq[0] > self.budget_id.frequency:
                        break
                freqs.append(freq[1] if str_rep else freq[0])
        except:
            pass

    def get_daily_cost(self) -> float:
        """returns the daily cost of a given item (amount / frequency)"""
        try:
            if self.frequency == 1:
                return self.cost
            elif self.frequency == 2:
                return self.cost / 7
            elif self.frequency == 3:
                return self.cost / 14
            elif self.frequency == 4:
                return (self.cost * 12) / 365
            else:
                return 0
        except:
            return 0
        
    def get_weekly_cost(self) -> float:
        try:
            if self.frequency == 1:
                return self.cost * 7
            elif self.frequency == 2:
                return self.cost
            elif self.frequency == 3:
                return self.cost / 2
            elif self.frequency == 4:
                return (self.cost * 12) / 52
            
            return 0
        except:
            return 0
        
    def get_monthly_cost(self) -> float:
        try:
            if self.frequency == 1:
                return (self.cost * 365) / 12
            elif self.frequency == 2:
                return (self.cost * 52) / 12
            elif self.frequency == 3:
                return (self.cost * 26) / 12
            elif self.frequency == 4:
                return self.cost
            
            return 0
        except:
            return 0

    def get_real_cost(self):
        try:
            ### frequencies:
            # 1 = daily, 2 = weekly, 3 = bi-weekly, 4 = monthly
            if self.frequency == self.budget_id.frequency:
                return self.cost
            else:
                # items frequency is daily
                if self.frequency == 1:
                    if self.budget_id.frequency == 2: 
                        return self.cost * 7
                    elif self.budget_id.frequency == 3: 
                        return self.cost * 14
                    elif self.budget_id.frequency == 4: 
                        return (self.cost * 365) / 12
                
                # items frequency is weekly
                elif self.frequency == 2:
                    if self.budget_id.frequency == 3:
                        return self.cost * 2
                    elif self.budget_id.frequency == 4: 
                        return (self.cost * 52) / 12
                
                # items frequency is bi weekly
                elif self.frequency == 3:
                    return (self.cost * 26) / 12 
                
                return 0
        except:
            return 0

    def __is_name_unique_in_set(self):
        """Returns True if name of item is unique within the Budget's item_set"""
        try:
            items = self.budget_id.item_set.exclude(id=self.id).filter(name=self.name)
            return len(items) == 0
        except:
            return False

    def save(self, *args, **kwargs):
        # ensure name is unique
        if not self.__is_name_unique_in_set():
            raise mdlexc.UniqueNameValueException()
        # ensure cost is positive
        if not self.__is_cost_positive():
            raise mdlexc.NegativeValueException("Item costs can not be negative.")

        # validate frequency value
        if not self.__is_frequency_value_valid():
            raise mdlexc.InvalidFrequencyException()

        # set frequency to int representation 
        self.frequency = self.get_frequency(str_rep=False)

        # ensure frequency of item doesn't exceed budget frequency
        if self.__is_frequency_value_exceeding():
            raise mdlexc.FrequencyExceedanceException()

        # ensure cost is permissible
        if self.__is_item_cost_permissible():
            super(Item, self).save(*args, **kwargs)
            self.budget_id.save()    
        else:
            raise mdlexc.ImpermissibleItemCostException()






