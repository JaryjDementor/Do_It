from django.db.models import Model, CharField, DateTimeField


class Workers(Model):
    name = CharField("name", max_length=1000, null=False)
    surname = CharField("surname", max_length=1000, null=False)

    class Meta:
        verbose_name = "Workers"
        verbose_name_plural = "Workers"

    def __str__(self):
        return f" {self.name} {self.surname} "


class Employees_Task_List(Model):
    description = CharField("description", max_length=1000, null=False)
    status = CharField("status", max_length=100, auto_created="Not complete")
    categories = CharField("categories", max_length=1000, null=False)
    date_of_completion = DateTimeField()
    idworker = CharField("idworker", max_length=10)

    class Meta:
        ordering = ["id"]
        verbose_name = "Employees_Task_List"
        verbose_name_plural = "Employees_Task_List"

    def __str__(self):
        return f" {self.description} {self.status} {self.categories} {self.date_of_completion}"
