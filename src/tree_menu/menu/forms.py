from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import CharField, ModelForm
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from tree_menu.menu.models import Menu


class TrailingSlashURLField(CharField):
    default_validators = [RegexValidator(regex=r"^/?(([.a-zA-Z0-9-])+(/){,1})*$")]

    def to_python(self, value: str) -> str:
        splited_path: list = super().to_python(value).split('/')
        if splited_path[-1]:
            splited_path.append('')
        return '/'.join(splited_path)


class MenuForm(ModelForm):
    url = TrailingSlashURLField(required=False)

    class Meta:
        model = Menu
        fields = ('name', 'parent', 'named_url', 'url')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data['url']:
            if self.cleaned_data['url'][0] != '/':
                instance.url = Menu.get_full_path(instance)
        if commit:
            instance.save()
        return instance

    def clean_url(self):
        url = self.cleaned_data['url']
        return None if url == '' else url

    def clean_named_url(self):
        named_url = self.cleaned_data['named_url']
        if named_url:
            splited_named_url = named_url.split()
            try:
                reverse(splited_named_url[0], args=splited_named_url[1:len(splited_named_url)])
            except NoReverseMatch as e:
                raise ValidationError(message=e)
            return named_url
