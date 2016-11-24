# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-07 17:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('fams', models.CharField(blank=True, max_length=200, verbose_name="Fam's")),
                ('bucque', models.CharField(blank=True, max_length=200)),
                ('proms', models.CharField(blank=True, max_length=200, verbose_name="Prom's")),
                ('credit', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date_negatss', models.DateTimeField(blank=True, null=True)),
                ('is_debucquable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='cashinput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='inputmethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('associated_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kfet.entity')),
            ],
        ),
        migrations.CreateModel(
            name='transactionentity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('product_name', models.CharField(max_length=200)),
                ('accepted', models.BooleanField(default=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionentity_source', to='kfet.account')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionentity_target', to='kfet.account')),
            ],
        ),
        migrations.CreateModel(
            name='transactionpg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.CharField(max_length=200)),
                ('accepted', models.BooleanField(default=False)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionpg_source', to='kfet.account')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionpg_target', to='kfet.account')),
            ],
        ),
        migrations.AddField(
            model_name='cashinput',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kfet.inputmethod'),
        ),
        migrations.AddField(
            model_name='cashinput',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashinput_source', to='kfet.account'),
        ),
        migrations.AddField(
            model_name='cashinput',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashinput_target', to='kfet.account'),
        ),
    ]