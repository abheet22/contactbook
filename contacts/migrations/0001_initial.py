# Generated by Django 3.0.6 on 2021-03-03 07:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('update_ts', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('email_address', models.CharField(db_index=True, error_messages={'invalid': 'Email already exist in system'}, max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactNumber',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('update_ts', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('home', 'Home'), ('mobile', 'Mobile'), ('fax', 'Fax'), ('work', 'Work'), ('other', 'Other')], default='other', max_length=10)),
                ('number', models.CharField(max_length=50)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contactdetail', to='contacts.Contacts')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]