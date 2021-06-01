# Generated by Django 2.2.5 on 2021-06-02 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cite_Rec_Cache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_id', models.BigIntegerField(db_index=True)),
                ('field_id', models.IntegerField(db_index=True)),
                ('Update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['Update_time'],
            },
        ),
    ]
