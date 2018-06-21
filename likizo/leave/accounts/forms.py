from django import forms
from django.contrib.auth.forms import UserCreationForm
from leave_app.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'gender', 'PF_number', 'title','email', 'department', 'is_manager',
                  'is_supervisor')

