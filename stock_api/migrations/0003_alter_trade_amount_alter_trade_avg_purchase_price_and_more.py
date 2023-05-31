# Generated by Django 4.2.1 on 2023-05-31 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0002_remove_trade_cumulative_allocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='avg_purchase_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='balance_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]