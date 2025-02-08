from django import forms

from .models import Item


INPUT_CLASSES = "tw-w-full tw-py-4 tw-px-6 tw-rounded-xl tw-border"


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            "name",
            "description",
            "price",
            "image",
            "category",
        )

        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": "3"}),
            "price": forms.NumberInput(attrs={"class": INPUT_CLASSES}),
            "image": forms.FileInput(attrs={"class": INPUT_CLASSES}),
            "category": forms.Select(attrs={"class": INPUT_CLASSES}),
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("name", "description", "price", "image", "category", "sold")

        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": "3"}),
            "price": forms.NumberInput(attrs={"class": INPUT_CLASSES}),
            "image": forms.FileInput(attrs={"class": INPUT_CLASSES}),
            "category": forms.Select(attrs={"class": INPUT_CLASSES}),
            # "sold": forms.CheckboxInput(attrs={"class": INPUT_CLASSES}),
        }
