from django.db import models

class Trade(models.Model):
    date = models.DateField()
    company_name = models.CharField(max_length=100)
    trade_type = models.CharField(max_length=50)
    quantity = models.IntegerField()
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    balance_quantity = models.IntegerField(blank=True, null=True)
    avg_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.company_name}"

    def save(self, *args, **kwargs):
        if self.trade_type == "Buy":
            previous_trades = Trade.objects.filter(
                company_name=self.company_name,
                quantity=self.quantity,
                trade_type="Buy"
            ).exclude(pk=self.pk)
            previous_quantity = previous_trades.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
            if previous_quantity is None:
                previous_quantity = 0
            self.balance_quantity = self.quantity + previous_quantity

            total_buying_amount = Trade.objects.filter(
                company_name=self.company_name,
                trade_type="Buy"
            ).aggregate(total_amount=models.Sum('amount'))['total_amount']
            total_buying_quantity = Trade.objects.filter(
                company_name=self.company_name,
                trade_type="Buy"
            ).aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
            if total_buying_amount is not None and total_buying_quantity is not None:
                self.avg_purchase_price = total_buying_amount / total_buying_quantity
            else:
                self.avg_purchase_price = None
        else:
            self.balance_quantity = self.quantity
            self.avg_purchase_price = None

        self.amount = self.quantity * self.buy_price

        super(Trade, self).save(*args, **kwargs)

        if self.trade_type == "Buy":
            buy_trades = Trade.objects.filter(
                company_name=self.company_name,
                trade_type="Buy"
            )
            total_buying_amount = buy_trades.aggregate(total_amount=models.Sum('amount'))['total_amount']
            total_buying_quantity = buy_trades.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
            if total_buying_amount is not None and total_buying_quantity is not None:
                self.avg_purchase_price = total_buying_amount / total_buying_quantity
            else:
                self.avg_purchase_price = None

        super(Trade, self).save(*args, **kwargs)
