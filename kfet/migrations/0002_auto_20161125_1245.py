# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-25 11:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('kfet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionvp',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionvp_target', to='users.Client'),
        ),
        migrations.AddField(
            model_name='transactionpg',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionpg_source', to='users.Client'),
        ),
        migrations.AddField(
            model_name='transactionpg',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionpg_target', to='users.Client'),
        ),
        migrations.AddField(
            model_name='transactionboulc',
            name='authortb',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionboulc_authortb', to='users.Client'),
        ),
        migrations.AddField(
            model_name='transactionboulc',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionboulc_target', to='users.Client'),
        ),
        migrations.AddField(
            model_name='product',
            name='associated_entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kfet.entity'),
        ),
        migrations.AddField(
            model_name='cashinput',
            name='authorci',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashinput_authorci', to='users.Client'),
        ),
        migrations.AddField(
            model_name='cashinput',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kfet.inputmethod'),
        ),
        migrations.AddField(
            model_name='cashinput',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashinput_target', to='users.Client'),
        ),
    ]
