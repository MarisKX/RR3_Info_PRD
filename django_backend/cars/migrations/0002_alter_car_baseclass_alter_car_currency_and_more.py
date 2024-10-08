# Generated by Django 5.0.7 on 2024-07-15 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='baseclass',
            field=models.CharField(choices=[('0', 'P'), ('1', 'S'), ('2', 'R')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='car',
            name='currency',
            field=models.CharField(choices=[('0', 'MS'), ('1', 'RS'), ('2', 'Gold'), ('3', 'Bonus')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='car',
            name='eng_drive',
            field=models.CharField(choices=[('0', 'FF'), ('1', 'FR'), ('2', 'RR'), ('3', 'MR'), ('4', 'F4'), ('5', 'R4'), ('6', 'M4')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='car',
            name='repair_currency',
            field=models.CharField(choices=[('0', 'MS'), ('1', 'RS'), ('2', 'Gold'), ('3', 'Bonus')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='car',
            name='section',
            field=models.CharField(choices=[('0', 'Motorsports'), ('1', 'Road Collection')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='carupgrade',
            name='upgrade_option1_currency',
            field=models.CharField(choices=[('0', 'MS'), ('1', 'RS'), ('2', 'Gold'), ('3', 'Bonus')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='carupgrade',
            name='upgrade_option2_currency',
            field=models.CharField(choices=[('0', 'MS'), ('1', 'RS'), ('2', 'Gold'), ('3', 'Bonus')], default='2', max_length=1),
        ),
    ]
