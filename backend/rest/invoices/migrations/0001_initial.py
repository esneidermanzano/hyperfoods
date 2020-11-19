# Generated by Django 3.1 on 2020-11-17 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('codeInvoice', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTimeInvoice', models.DateTimeField(auto_now_add=True)),
                ('totalInvoice', models.PositiveIntegerField(default=0)),
                ('clientInvoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.client')),
            ],
        ),
    ]
