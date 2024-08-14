from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    wallet = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'wallet', 'is_superuser']

    def clean_wallet(self):
        wallet = self.cleaned_data.get('wallet')
        if wallet is not None and wallet < 0:
            raise forms.ValidationError("Wallet balance cannot be negative.")
        return wallet

    def save(self, commit=True):
        user = super().save(commit=False)
        user.wallet = self.cleaned_data['wallet']
        if commit:
            user.save()
        return user
