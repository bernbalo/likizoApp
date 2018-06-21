from django.views.generic import ListView, UpdateView, DeleteView
from django.shortcuts import (render, get_object_or_404, redirect)
from .models import User, Leave
from .forms import NewLeaveForm, SupervisorApproveForm, EditLeaveForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render, redirect, reverse
# Create your views here.


@login_required
def edit_leave(request, leave_id):
    data = get_object_or_404(Leave, id=leave_id)
    if request.method == 'POST':
        form = EditLeaveForm(request.POST or None, instance=data, request=request)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.start_date = form.cleaned_data.get('start_date')

            # Handling duration
            # Case 1: duration for annual leave is entered value
            if form.cleaned_data.get('leave_type') == "ANNUAL":
                leave.duration = form.cleaned_data.get('duration')
            # compassionate is 14 days
            elif form.cleaned_data.get('leave_type') == "COMPASSIONATE":
                leave.duration = 14
            # paternity is 14 days
            elif form.cleaned_data.get('leave_type') == "PATERNITY":
                leave.duration = 14
            else:
                # maternity is 60 days
                leave.duration = 60
            leave.leave_type = form.cleaned_data.get('leave_type')
            leave.user = request.user
            leave.save()
            return redirect('list_user_leave', username=request.user.username)
        else:
            return render(request, 'new_leave.html', {'form': form})
    else:
        form = NewLeaveForm(instance=data, request=request)
    return render(request, 'new_leave.html', {'form': form})
'''
@method_decorator(login_required, name='dispatch')
class LeaveUpdateView(UpdateView):
    model = Leave
    fields = ('leave_type', 'start_date', 'duration')
    template_name = 'leave_update.html'
    pk_url_kwarg = 'leave_id'

    def get_queryset(self):
        return Leave.objects.filter(user_id=self.request.user.id)

    def get_success_url(self):
        username = self.request.user
        return reverse('list_user_leave', kwargs={'username': username})
'''

@method_decorator(login_required, name='dispatch')
class DeleteLeaveView(DeleteView):
    template_name = 'leave_confirm_delete.html'
    model = Leave
    pk_url_kwarg = 'leave_id'

    def get_success_url(self):
        username = self.request.user
        return reverse('list_user_leave', kwargs={'username': username})



def new_leave(request):

    #user = User.objects.get(first_name__icontains='evodia')

    if request.method == 'POST':
        form = NewLeaveForm(request.POST, request=request)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.start_date = form.cleaned_data.get('start_date')

            # Handling duration
            # Case 1: duration for annual leave is entered value
            if form.cleaned_data.get('leave_type') == "ANNUAL":
                leave.duration = form.cleaned_data.get('duration')
            # compassionate is 14 days
            elif form.cleaned_data.get('leave_type') == "COMPASSIONATE":
                leave.duration = 14
            # paternity is 14 days
            elif form.cleaned_data.get('leave_type') == "PATERNITY":
                leave.duration = 14
            else:
                # maternity is 60 days
                leave.duration = 60
            leave.leave_type = form.cleaned_data.get('leave_type')
            leave.user = request.user
            leave.save()
            return redirect('list_user_leave', username=request.user.username)
        else:
            return render(request, 'new_leave.html', {'form': form})
    else:
        form = NewLeaveForm(request=request)
    return render(request, 'new_leave.html', {'form': form})


def list_leave(request):
    user = request.user
    user_leave = user.leaves.all()

    return render(request, 'leave.html', {'user': user, 'user_leave': user_leave, })


def list_user_leave(request, username):
    #user = get_object_or_404(User, first_name__icontains=username)
    user = request.user
    user_leave = user.leaves.all()
    return render(request, 'list_user_leave.html',
                  {'user': user, 'user_leave': user_leave, })


class LeaveApprovedBySupervisor(UpdateView):
    model = Leave
    form_class = SupervisorApproveForm
    template_name = 'supervisor_approve.html'
    pk_url_kwarg = 'leave_id'
    context_object_name = 'leave'

    def form_valid(self, form):
        leave = form.save(commit=False)
        leave.supervisor_approved = True
        leave.save()
        return redirect('list_user_leave', username=leave.user.first_name)


class LeaveApprovedByManager(UpdateView):
    model = Leave
    form_class = SupervisorApproveForm
    template_name = 'supervisor_approve.html'
    pk_url_kwarg = 'leave_id'
    context_object_name = 'leave'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(supervisor_approved=True)

    def form_valid(self, form):
        leave = form.save(commit=False)
        leave.manager_approved = True
        leave.save()
        return redirect('list_user_leave', username=leave.user.first_name)


class AllNewLeavesByDepartmentList(ListView):
    model = Leave
    context_object_name = 'new_leaves'
    template_name = 'new_leave_department.html'


    def get_queryset(self):
        return self.objects.filter(department=self.request.user.department).\
            filter(supervisor_approved=False).filter(manager_approved=False)


