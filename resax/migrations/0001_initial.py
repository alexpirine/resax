# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 18:00
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='stock')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'activity',
                'swappable': 'RESAX_ACTIVITY_MODEL',
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='ActivityResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-1)], verbose_name='quantity')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_resources', to=settings.RESAX_ACTIVITY_MODEL, verbose_name='activity')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'activity resource',
                'swappable': 'RESAX_ACTIVITYRESOURCE_MODEL',
                'verbose_name_plural': 'activity resources',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField(db_index=True, verbose_name='date_start')),
                ('date_stop', models.DateTimeField(db_index=True, verbose_name='date_stop')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='stock')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='modificationexit date')),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.RESAX_ACTIVITY_MODEL, verbose_name='activity')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'event',
                'swappable': 'RESAX_EVENT_MODEL',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='FlexiReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='flexi_reservation', to=settings.RESAX_EVENT_MODEL, verbose_name='event')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'flexible reservations',
                'swappable': 'RESAX_FLEXIRESERVATION_MODEL',
                'verbose_name_plural': 'flexible reservations',
            },
        ),
        migrations.CreateModel(
            name='FlexiReservationResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-1)], verbose_name='quantity')),
                ('flexi_reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flexi_reservation_resources', to=settings.RESAX_FLEXIRESERVATION_MODEL, verbose_name='reservation')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'flexible reservation resource',
                'swappable': 'RESAX_FLEXIRESERVATIONRESOURCE_MODEL',
                'verbose_name_plural': 'flexible reservation resources',
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'organisation',
                'swappable': 'RESAX_ORGANISATION_MODEL',
                'verbose_name_plural': 'organisations',
            },
        ),
        migrations.CreateModel(
            name='Planning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodicity', models.PositiveIntegerField(choices=[(1, 'daily'), (2, 'weekly'), (3, 'monthly')], verbose_name='periodicity')),
                ('days_of_week', models.CharField(max_length=7, verbose_name='days of week')),
                ('time_start', models.DateTimeField(verbose_name='time start')),
                ('time_stop', models.DateTimeField(verbose_name='time stop')),
                ('date_stop', models.DateTimeField(blank=True, null=True, verbose_name='date stop')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plannings', to=settings.RESAX_ACTIVITY_MODEL, verbose_name='activity')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'planning',
                'swappable': 'RESAX_PLANNING_MODEL',
                'verbose_name_plural': 'plannings',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)], verbose_name='quantity')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.RESAX_EVENT_MODEL, verbose_name='event')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'reservation',
                'swappable': 'RESAX_RESERVATION_MODEL',
                'verbose_name_plural': 'reservations',
            },
        ),
        migrations.CreateModel(
            name='ReservationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_types', to=settings.RESAX_ORGANISATION_MODEL, verbose_name='organisation')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'reservation type',
                'swappable': 'RESAX_RESERVATIONTYPE_MODEL',
                'verbose_name_plural': 'reservation types',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='stock')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'resource',
                'swappable': 'RESAX_RESOURCE_MODEL',
                'verbose_name_plural': 'resources',
            },
        ),
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_types', to=settings.RESAX_ORGANISATION_MODEL, verbose_name='organisation')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'resource type',
                'swappable': 'RESAX_RESOURCETYPE_MODEL',
                'verbose_name_plural': 'resource types',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('events', models.ManyToManyField(related_name='users', through='resax.Reservation', to=settings.RESAX_EVENT_MODEL, verbose_name='events')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.RESAX_ORGANISATION_MODEL, verbose_name='organisation')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'swappable': 'RESAX_USER_MODEL',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.AddField(
            model_name='resource',
            name='resource_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to=settings.RESAX_RESOURCETYPE_MODEL, verbose_name='resource type'),
        ),
        migrations.AddField(
            model_name='reservationtype',
            name='resources',
            field=models.ManyToManyField(related_name='reservation_type', to=settings.RESAX_RESOURCE_MODEL, verbose_name='resources'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.RESAX_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='flexireservationresource',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flexi_reservation_resources', to=settings.RESAX_RESOURCE_MODEL, verbose_name='resource'),
        ),
        migrations.AddField(
            model_name='flexireservation',
            name='reservation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flexi_reservations', to=settings.RESAX_RESERVATIONTYPE_MODEL, verbose_name='reservation type'),
        ),
        migrations.AddField(
            model_name='flexireservation',
            name='resources',
            field=models.ManyToManyField(related_name='flexi_reservations', through='resax.FlexiReservationResource', to=settings.RESAX_RESOURCE_MODEL, verbose_name='resources'),
        ),
        migrations.AddField(
            model_name='flexireservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flexi_reservations', to=settings.RESAX_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='event',
            name='planning',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.RESAX_PLANNING_MODEL, verbose_name='planning'),
        ),
        migrations.AddField(
            model_name='activityresource',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_resources', to=settings.RESAX_RESOURCE_MODEL, verbose_name='resource'),
        ),
        migrations.AddField(
            model_name='activity',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.RESAX_ORGANISATION_MODEL, verbose_name='organisation'),
        ),
        migrations.AddField(
            model_name='activity',
            name='resources',
            field=models.ManyToManyField(related_name='activities', through='resax.ActivityResource', to=settings.RESAX_RESOURCE_MODEL, verbose_name='resources'),
        ),
        migrations.AlterUniqueTogether(
            name='resourcetype',
            unique_together=set([('organisation', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('resource_type', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='reservationtype',
            unique_together=set([('organisation', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='activityresource',
            unique_together=set([('resource', 'activity')]),
        ),
    ]