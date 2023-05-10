import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^/?(([.a-zA-Z0-9-])+(/){,1})*$')])),
                ('named_url', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menu.menu')),
            ],
        ),
    ]
