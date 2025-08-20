from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0005_alter_blog_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='blogtag',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]


