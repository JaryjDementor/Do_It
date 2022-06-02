from django.forms import ModelForm, TextInput, Textarea
from . import models
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class WorkersForm(ModelForm):
    class Meta:
        model = models.Workers
        fields = ["username"]

        widgets = {
            "username": TextInput(
                attrs={"class": "form-control", "placeholder": "username"}
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


class TeamsListForm(ModelForm):
    class Meta:
        model = models.TeamsList
        fields = ["name_team"]

        widgets = {
            "name_team": TextInput(
                attrs={"class": "form-control", "placeholder": "name_team"}
            ),
        }