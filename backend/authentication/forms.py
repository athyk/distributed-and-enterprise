from django import forms
from .models import User
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
    )
    
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "full_name", "nickname", "gender"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])  # Hash password
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid email or password.")

        if not check_password(password, user.password):
            raise forms.ValidationError("Invalid email or password.")

        cleaned_data["user"] = user
        return cleaned_data
