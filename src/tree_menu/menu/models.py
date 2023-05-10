from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.CharField(max_length=255, blank=True, null=True, unique=True,
                           validators=[RegexValidator(regex=r"^/?(([.a-zA-Z0-9-])+(/){,1})*$")])
    named_url = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def get_full_path(self):
        return self.parent.get_url() + self.get_url() if self.parent else '/{}'.format(self.get_url())

    def get_url(self) -> str:
        return reverse(self.named_url.split()[0], args=self.named_url.split()[1:len(
            self.named_url.split())]) if self.named_url else self.url if self.url else ''


def get_all_children(name, include_self=False):
    table_name = Menu.objects.model._meta.db_table
    query = (
        "WITH RECURSIVE children (id) AS ("
        f"  SELECT {table_name}.id FROM {table_name} WHERE name = '{name}'"
        "  UNION ALL"
        f"  SELECT {table_name}.id FROM children, {table_name}"
        f"  WHERE {table_name}.parent_id = children.id"
        ")"
        f" SELECT {table_name}.*"
        f" FROM {table_name}, children WHERE children.id = {table_name}.id"
    )
    if not include_self:
        query += f" AND {table_name}.name != {name}"
    return Menu.objects.raw(query)
