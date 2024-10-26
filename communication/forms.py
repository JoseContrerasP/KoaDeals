from django import forms

from .models import ConversationMessage


class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={"class": "tw-w-full tw-py-4 tw-px-6 tw-rounded-xl tw-border", "rows": "3", "autofocus": True}
            )
        }
