# Generated by Django 3.1.2 on 2020-10-09 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='static/default/default_img.png', upload_to='recipe/'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipe_ingredients', through='recipe.Recipe_Ingredient', to='recipe.Ingredient'),
        ),
    ]
