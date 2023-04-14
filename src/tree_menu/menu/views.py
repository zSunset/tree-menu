from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from tree_menu.menu.models import Menu


class MenuView(TemplateView):
    template_name = 'menu/index.html'
