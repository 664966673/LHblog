# Generated by Django 2.0.5 on 2018-05-14 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='文章列表')),
                ('excerpt', models.CharField(blank=True, max_length=200, verbose_name='摘要')),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
                ('update_time', models.DateTimeField(blank=True, null=True)),
                ('url_height', models.PositiveIntegerField(default=225)),
                ('url_width', models.PositiveIntegerField(default=300)),
                ('images', models.ImageField(blank=True, height_field='url_height', null=True, upload_to='art_img', width_field='url_width')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='阅读量')),
                ('show_img', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '文章列表',
                'verbose_name_plural': '文章列表',
                'db_table': 'blogarticle',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '栏目',
                'verbose_name_plural': '栏目',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
                'db_table': 'Tag',
            },
        ),
    ]
