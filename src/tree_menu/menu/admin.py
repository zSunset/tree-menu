from django.contrib import admin

from tree_menu.menu.models import Menu
from tree_menu.menu.forms import MenuForm


class MenuAdminForm(admin.ModelAdmin):
    form = MenuForm


admin.site.register(Menu, MenuAdminForm)
