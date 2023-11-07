# Generated by Django 4.0.4 on 2022-04-20 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.EmailField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('communication_id', models.IntegerField(primary_key=True, serialize=False)),
                ('sender', models.EmailField(max_length=150)),
                ('receiver', models.EmailField(max_length=150)),
                ('type_receiver', models.CharField(max_length=10)),
                ('type_exchange', models.CharField(max_length=10)),
                ('date_mail', models.DateTimeField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('conversation_id', models.IntegerField(primary_key=True, serialize=False)),
                ('message_id', models.CharField(max_length=100, unique=True)),
                ('subject', models.CharField(max_length=400)),
                ('number_mails', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('category', models.CharField(max_length=30, null=True)),
                ('mail_box', models.CharField(max_length=20, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Extern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('email_address', models.EmailField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=500)),
                ('occurence', models.IntegerField()),
                ('conversation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.conversation')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000, null=True)),
                ('number_words', models.IntegerField(null=True)),
                ('filename', models.BooleanField(max_length=10, null=True)),
                ('date_mail', models.DateTimeField(max_length=30)),
                ('conversation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.conversation')),
            ],
        ),
        migrations.CreateModel(
            name='Communication_Extern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('communication_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.communication')),
                ('extern_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.extern')),
            ],
        ),
        migrations.AddField(
            model_name='communication',
            name='conversation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.conversation'),
        ),
        migrations.CreateModel(
            name='Address_Communication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.address')),
                ('communication_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.communication')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='employee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.employee'),
        ),
    ]
