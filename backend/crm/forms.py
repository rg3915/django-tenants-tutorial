from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    required_css_class = 'required'

    username = forms.CharField(
        label='Usuário',
        max_length=150,
    )
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        required=False,
    )
    email = forms.EmailField(
        label='E-mail',
        required=False,
    )

    class Meta:
        model = Employee
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'occupation',
            'cpf',
        )
