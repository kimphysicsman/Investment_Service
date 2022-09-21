# Generated by Django 4.0.6 on 2022-09-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='status',
            field=models.CharField(choices=[('validate', '검증 상태'), ('complete', '입금 완료')], default='validate', max_length=128, verbose_name='상태'),
        ),
    ]
