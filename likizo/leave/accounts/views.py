from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, UpdateView, DeleteView
from .forms import CreateUserForm
from django.contrib.auth import get_user_model

User = get_user_model()


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users.html'
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('PF_number', 'first_name', 'last_name', 'username','gender','department',
              'title','is_manager','is_supervisor',)

    template_name = 'edit_user.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'update_user'

    def get_success_url(self):
        return reverse('list_users')


@method_decorator(login_required, name='dispatch')
class DeleteUserView(DeleteView):
    template_name = 'user_confirm_delete.html'
    model = User
    pk_url_kwarg = 'user_id'

    def get_success_url(self):
        return reverse('list_users')


def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('new_leave')
    else:
        form = CreateUserForm()
    return render(request, 'signup.html', {'form': form})
