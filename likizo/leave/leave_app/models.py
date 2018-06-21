from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
import datetime

#TODO:


class Department(models.Model):
    department_name = models.CharField(max_length=150)
    department_head = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='head')

    def __str__(self):
        return self.department_name


class User(AbstractUser):
    GENDER_TYPE =(
        ('M', 'Male'),
        ('F', 'Female')
    )
    is_supervisor = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    title = models.CharField(max_length=13, null=True, blank=True)
    PF_number = models.PositiveSmallIntegerField(null=True)
    department = models.ForeignKey(Department, related_name='users', blank=True, null=True)
    gender = models.CharField(choices=GENDER_TYPE, max_length=2, null=True, default='M')

    def get_remaining_annual_leaves(self):
        taken_leave = self.leaves.filter(leave_type="ANNUAL").aggregate(TotalLeaves=Sum('duration'))
        taken = 0
        if taken_leave['TotalLeaves']:
            taken = taken_leave['TotalLeaves']
        remaining_leaves = (28 - taken)
        return remaining_leaves

'''
Django user model has the following default fiels
 username
    Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.

first_name
    Optional (blank=True). 30 characters or fewer.

last_name
    Optional (blank=True). 150 characters or fewer.

password
    Required. A hash of, and metadata about, the password. 
    (Django doesn’t store the raw password.) Raw passwords can be arbitrarily long and can contain any character. See the password documentation.

groups
    Many-to-many relationship to Group

user_permissions
    Many-to-many relationship to Permission

is_staff
    Boolean. Designates whether this user can access the admin site.

is_active
    Boolean. Designates whether this user account should be considered active. We recommend that you set this flag to False instead of deleting accounts; that way, if your applications have any foreign keys to users, the foreign keys won’t break.

is_superuser
    Boolean. Designates that this user has all permissions without explicitly assigning them.

last_login
    A datetime of the user’s last login.

date_joined
    A datetime designating when the account was created. Is set to the current date/time by default when the account is created.
'''


class Leave(models.Model):
    LEAVE_TYPE_CHOICES = (
        ('ANNUAL', 'Annual'),
        ('COMPASSIONATE', 'compassionate'),
        ('MATERNITY', 'maternity'),
        ('PATERNITY', 'paternity')
    )
    leave_type = models.CharField(choices=LEAVE_TYPE_CHOICES, max_length=13, default='ANNUAL')
    start_date = models.DateField()
    duration = models.IntegerField()
    supervisor_approved = models.BooleanField(default=False)  # leave approved by employee supervisor
    manager_approved = models.BooleanField(default=False)   # leave approved by manager
    # if leave is approved by both then employee is on leave
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaves', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        user = self.user.get_full_name()
        start = self.start_date
        duration = self.duration
        type = self.leave_type
        return f'{type}: {user} from {start} for {duration} '

# TODO: Correct end date flow
    def end_date(self):
        return self.start_date + timedelta(days=self.duration)

    def leave_expired(self):
        if datetime.datetime.now().date() > self.end_date():
            return True
        else:
            return False

# return the last leave

    def waiting_leaves(self):
        return self.filter(supervisor_approved=True).filter(manager_approved=True)

    def approved_leaves(self):
        return self.objects.filter(manager_approved=True)


# This function takes a year and return all leaves of that year

    def get_leave_by_year(self, year):
        last_day_of_year = datetime.date(year, 12, 31)
        first_day_of_year = datetime.date(year, 1, 1)

        return self.filter(start_date__lte=last_day_of_year).\
            filter(start_date__gte=first_day_of_year)

    def is_supervisor_approved(self):
        return self.supervisor_approved

    def is_approved(self):
        if self.supervisor_approved and self.manager_approved:
            return True
        else:
            return False
    '''
    Return true if leave is approved
    '''














