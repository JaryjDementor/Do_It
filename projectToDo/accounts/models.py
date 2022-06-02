from django.db.models import Model, CharField


class Roles(Model):
    id_user = CharField("id_user", max_length=1000, null=False)
    admin = CharField("admin", max_length=1000, null=False)

    class Meta:
        verbose_name = "Roles"
        verbose_name_plural = "Roles"

