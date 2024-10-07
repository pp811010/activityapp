# Generated by Django 5.1.1 on 2024-10-03 13:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('phone', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BookingFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='studentcard/')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('card', models.IntegerField()),
                ('photo', models.ImageField(upload_to='place/')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.activity')),
                ('staff', models.ManyToManyField(to='booking.staff')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.place'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('faculty', models.CharField(choices=[('It', 'Information Technology'), ('ENG', 'Engineering'), ('BUS', 'Business'), ('MED', 'Medicine'), ('LAW', 'Law'), ('ART', 'Arts'), ('EDU', 'Education'), ('SC', 'Sciences')], max_length=50)),
                ('stu_card', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('phone', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='report/')),
                ('status', models.CharField(choices=[('REPORTED', 'Reported'), ('IN_PROGRESS', 'In Progress'), ('DONE', 'Done')], max_length=50)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.place')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.student')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.student'),
        ),
    ]
