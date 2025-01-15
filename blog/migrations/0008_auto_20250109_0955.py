# Generated by Django 3.2.10 on 2025-01-09 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_article_is_special_alter_article_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آدرس آی پی')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='hits',
            field=models.ManyToManyField(blank=True, related_name='hits', to='blog.IPAddress', verbose_name='بازدیدها'),
        ),
    ]
