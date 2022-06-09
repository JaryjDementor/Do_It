from django.db.models import Model, CharField, DateTimeField, IntegerField


class Workers(Model):
    id_team = IntegerField("id_team", max_length=1000, null=True)
    id_admin = IntegerField("id_admin", max_length=1000, null=True)
    id_worker = IntegerField("id_worker", max_length=1000, null=False)
    username = CharField("username", max_length=1000, null=False)
    first_name = CharField("first_name", max_length=1000, null=False)
    last_name = CharField("last_name", max_length=1000, null=False)
    class Meta:
        verbose_name = "Workers"
        verbose_name_plural = "Workers"




class Employees_Task_List(Model):
    id_creator = IntegerField("id_creator", max_length=1000, null=False)
    id_worker = IntegerField("id_worker", max_length=1000, null=False)
    id_team = IntegerField("id_team", max_length=1000, null=False)
    description = CharField("description", max_length=1000, null=False)
    status = CharField("status", max_length=100, auto_created="Not complete")
    categories = CharField("categories", max_length=1000, null=False)
    date_of_completion = DateTimeField()

    class Meta:
        ordering = ["id"]
        verbose_name = "Employees_Task_List"
        verbose_name_plural = "Employees_Task_List"

    def __str__(self):
        return f" {self.description} {self.status} {self.categories} {self.date_of_completion}"

class TeamsList(Model):
    id_admin = IntegerField("id_admin", max_length=1000, null=False)
    name_team = CharField("name_team", max_length=1000, null=False)

    class Meta:
        verbose_name = "Teams"
        verbose_name_plural = "Teams"

    def __str__(self):
        return f" {self.id_admin} {self.name_team} "