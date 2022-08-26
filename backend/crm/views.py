from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import EmployeeForm
from .models import Customer, Employee


def create_new_user(form):
    # Cria o Usuário.
    user = User.objects.create(
        username=form.cleaned_data['username'],
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        email=form.cleaned_data['email'],
    )
    return user


def create_new_employee(form, user):
    # Cria o Funcionário.
    Employee.objects.create(
        occupation=form.cleaned_data['occupation'],
        cpf=form.cleaned_data['cpf'],
        user=user,
    )


def employee_create(request):
    template_name = 'crm/employee_form.html'
    form = EmployeeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            user = create_new_user(form)
            create_new_employee(form, user)
            # return HttpResponse('OK')
            return redirect('crm:employee_list')

    context = {'form': form}
    return render(request, template_name, context)


def customer_list(request):
    template_name = 'crm/customer_list.html'
    object_list = Customer.objects.all()
    context = {'object_list': object_list}
    return render(request, template_name, context)


def employee_list(request):
    template_name = 'crm/employee_list.html'
    object_list = Employee.objects.all()
    context = {'object_list': object_list}
    return render(request, template_name, context)
