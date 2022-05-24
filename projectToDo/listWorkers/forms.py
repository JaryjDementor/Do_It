from django.forms import ModelForm, TextInput, Textarea
from . import models
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class NewWorkerForm(ModelForm):
    class Meta:
        model = models.Workers
        fields = ["name", "surname"]

        widgets = {
            "name": TextInput(attrs={"class": "form-control", "placeholder": "name"}),
            "surname": TextInput(
                attrs={"class": "form-control", "placeholder": "surname"}
            ),
        }


class NewTaskForm(ModelForm):
    class Meta:
        model = models.Employees_Task_List
        fields = ["description", "categories", "date_of_completion"]

        widgets = {
            "description": Textarea(
                attrs={"class": "form-control", "placeholder": "description"}
            ),
            "categories": TextInput(
                attrs={"class": "form-control", "placeholder": "categories"}
            ),
            "date_of_completion": DateInput(),
        }
