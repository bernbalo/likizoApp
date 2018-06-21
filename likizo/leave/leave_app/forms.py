import datetime
from django import forms
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus import DatePickerInput
from.models import Leave, User


class NewLeaveForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(NewLeaveForm, self).__init__(*args, **kwargs)

    date = datetime.datetime.today()
    today_date = date.strftime("%Y-%m-%d")
    LEAVE_TYPE_CHOICES = (
        ('ANNUAL', 'Annual'),
        ('COMPASSIONATE', 'compassionate'),
        ('MATERNITY', 'maternity'),
        ('PATERNITY', 'paternity')
    )
    leave_type = forms.CharField(widget=forms.Select(choices=LEAVE_TYPE_CHOICES))
    start_date = forms.DateField(initial=today_date, widget=DatePickerInput(
        options={"format": "yyyy-mm-dd", "autoclose": True,
                 "startDate": "-1w",
                 "endDate": "+1y",
                 "todayHighlight": True,
                 }))
    duration = forms.IntegerField(required=False)

    class Meta:
        model = Leave
        fields = ['leave_type', 'start_date', 'duration']

    def clean_leave_type(self):
        # Ensure individual can as only the leaves assigned to their genders
        # IE men are not entitled maternity leave and woman are not entitled paternity leave

        gender = self.request.user.gender

        if gender == 'M' and self.cleaned_data.get('leave_type') == "MATERNITY":
            raise ValidationError("Likizo hii ni kwa kina mama tu!")

        if gender == 'F' and self.cleaned_data.get('leave_type') == "PATERNITY":
            raise ValidationError("Likizo hii ni kwa kina mama tu!,")

        return self.cleaned_data.get('leave_type')

    def clean_start_date(self):
        data = self.cleaned_data.get('start_date')
        # find the last leave end date
        last_leave_end_date = self.request.user.leaves.all()[0].end_date()

        if data < last_leave_end_date:
            text = f"likizo yako iliyopita bado haijaisha, itaisha tarehe {last_leave_end_date}" \
                   f" Tafadhali futalikizo inayosubiri kuisha ndiouombe tena..!"
            raise ValidationError(text)

        # check if date is not in the past
        if data < datetime.date.today():
            raise ValidationError("Hairuhusiwi kuomba likizo kwa siku zilizopita.")

        # check if date is not in the next year,
        # you can not start this year's leave in the next year

        last_day_of_year = datetime.date(datetime.date.today().year, 12, 31)

        if data > last_day_of_year:
            raise ValidationError("Hairuhusiwi kuanza likizo ya mwaka ujao")
        # check if there is another leave in the database which cover the same perion
        # Ensure that use does not ask for leave which start in the middle of the last leave


        return data

    def clean_duration(self):
        #user = User.objects.get(first_name__icontains ="evodia")
        remaining_leaves = self.request.user.get_remaining_annual_leaves()
        error = f'Umebakiza siku {remaining_leaves} tu za likizo ! , tafadhali hakikisha idadi ya siku ulizoomba'
        if self.cleaned_data.get("leave_type") == "ANNUAL":

            if not self.cleaned_data.get('duration'):
                raise ValidationError(" Tafadhali ingiza idadi ya siku")

            data = self.cleaned_data.get('duration')

            if data < 1:
                raise ValidationError("Tafadhali ingiza idadi ya siku sahihi")

            if data > remaining_leaves:

                raise ValidationError(error)
            return data


class EditLeaveForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(EditLeaveForm, self).__init__(*args, **kwargs)

    date = datetime.datetime.today()
    today_date = date.strftime("%Y-%m-%d")
    LEAVE_TYPE_CHOICES = (
        ('ANNUAL', 'Annual'),
        ('COMPASSIONATE', 'compassionate'),
        ('MATERNITY', 'maternity'),
        ('PATERNITY', 'paternity')
    )
    leave_type = forms.CharField(widget=forms.Select(choices=LEAVE_TYPE_CHOICES))
    start_date = forms.DateField(initial=today_date, widget=DatePickerInput(
        options={"format": "yyyy-mm-dd", "autoclose": True,
                 "startDate": "-1w",
                 "endDate": "+1y",
                 "todayHighlight": True,
                 }))
    duration = forms.IntegerField(required=False)

    class Meta:
        model = Leave
        fields = ['leave_type', 'start_date', 'duration']

    def clean_leave_type(self):
        # Ensure individual can as only the leaves assigned to their genders
        # IE men are not entitled maternity leave and woman are not entitled paternity leave

        gender = self.request.user.gender

        if gender == 'M' and self.cleaned_data.get('leave_type') == "MATERNITY":
            raise ValidationError("Likizo hii ni kwa kina mama tu!")

        if gender == 'F' and self.cleaned_data.get('leave_type') == "PATERNITY":
            raise ValidationError("Likizo hii ni kwa kina mama tu!,")

        return self.cleaned_data.get('leave_type')

    def clean_start_date(self):
        data = self.cleaned_data.get('start_date')
        # check if date is not in the past
        if data < datetime.date.today():
            raise ValidationError("Hairuhusiwi kuomba likizo kwa siku zilizopita.")

        # check if date is not in the next year,
        # you can not start this year's leave in the next year

        last_day_of_year = datetime.date(datetime.date.today().year, 12, 31)

        if data > last_day_of_year:
            raise ValidationError("Hairuhusiwi kuanza likizo ya mwaka ujao")
        # check if there is another leave in the database which cover the same perion
        # Ensure that use does not ask for leave which start in the middle of the last leave


        return data

    def clean_duration(self):
        #user = User.objects.get(first_name__icontains ="evodia")
        remaining_leaves = self.request.user.get_remaining_annual_leaves()
        error = f'Umebakiza siku {remaining_leaves} tu za likizo ! , tafadhali hakikisha idadi ya siku ulizoomba'
        if self.cleaned_data.get("leave_type") == "ANNUAL":

            if not self.cleaned_data.get('duration'):
                raise ValidationError(" Tafadhali ingiza idadi ya siku")

            data = self.cleaned_data.get('duration')

            if data < 1:
                raise ValidationError("Tafadhali ingiza idadi ya siku sahihi")

            if data > remaining_leaves:

                raise ValidationError(error)
            return data

class SupervisorApproveForm(forms.ModelForm):
    date = datetime.datetime.today()
    today_date = date.strftime("%Y-%m-%d")
    LEAVE_TYPE_CHOICES = (
        ('ANNUAL', 'Annual'),
        ('COMPASSIONATE', 'compassionate'),
        ('MATERNITY', 'maternity'),
        ('PATERNITY', 'paternity')
    )
    leave_type = forms.CharField(disabled=True, widget=forms.Select(choices=LEAVE_TYPE_CHOICES))
    start_date = forms.DateField(initial=today_date, widget=DatePickerInput(
        options={"format": "yyyy-mm-dd", "autoclose": True,
                 "startDate": "-1w",
                 "endDate": "+1y",
                 "todayHighlight": True,
                 }))
    duration = forms.IntegerField(required=False, disabled=True)

    class Meta:
        model = Leave
        fields = ['leave_type', 'start_date', 'duration']

    def clean_start_date(self):
        data = self.cleaned_data.get('start_date')
        # check if date is not in the past

        if data < datetime.date.today():
            raise ValidationError("Hairuhusiwi kuomba likizo kwa siku zilizopita.")

        # check if date is not in the next year,
        # you can not start this year's leave in the next year

        last_day_of_year = datetime.date(datetime.date.today().year, 12, 31)

        if data > last_day_of_year:
            raise ValidationError("Hairuhusiwi kuanza likizo ya mwaka ujao")

        return data

    def clean_duration(self):
        user = User.objects.get(first_name__icontains ="evodia")
        remaining_leaves = user.get_remaining_annual_leaves()
        error = f'Umebakiza siku {remaining_leaves} tu za likizo ! , tafadhali hakikisha idadi ya siku ulizoomba'
        if self.cleaned_data.get("leave_type") == "ANNUAL":
            data = self.cleaned_data.get('duration')

            if data < 1:
                raise ValidationError("Tafadhali ingiza idadi ya siku sahihi")

            if data > remaining_leaves:

                raise ValidationError(error)
            return data





