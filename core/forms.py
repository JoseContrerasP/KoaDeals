from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# from allauth.account.forms import SignupForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": "tw-w-full tw-py-4 tw-px-6 tw-rounded-xl",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": "tw-w-full tw-py-4 tw-px-6 tw-rounded-xl",
            }
        )
    )


# class MySignupForm(SignupForm):
# class Meta:
#     model = User
# fields = ("username", "email", "password1", "password2")

# username = forms.CharField(
#     widget=forms.TextInput(
#         attrs={
#             "placeholder": "Your username",
#             "class": "w-full py-4 px-6 rounded-xl",
#         }
#     )
# )

# email = forms.CharField(
#     widget=forms.EmailInput(
#         attrs={
#             "placeholder": "Your email address",
#             "class": "w-full py-4 px-6 rounded-xl",
#         }
#     )
# )

# password1 = forms.CharField(
#     widget=forms.PasswordInput(
#         attrs={
#             "placeholder": "Your password",
#             "class": "w-full py-4 px-6 rounded-xl",
#         }
#     )
# )

# password2 = forms.CharField(
#     widget=forms.PasswordInput(
#         attrs={
#             "placeholder": "Repeat password",
#             "class": "w-full py-4 px-6 rounded-xl",
#         }
#     )
# )
# pass


class MySignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": "tw-w-full tw-py-4 tw-px-6 tw-rounded-xl",
            }
        )
    )

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Your email address",
                "class": "tw-w-full tw-py-4 tw-px-6 tw-rounded-xl",
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": "tw-w-full tw-py-4 tw-px-6 tw-rounded-xl",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat password",
                "class": "tw-w-full tw-py-4 tw-px-6 tw-rounded-xl",
            }
        )
    )
