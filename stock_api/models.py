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
    split_ratio_x = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    split_ratio_y = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.company_name}"

    def save(self, *args, **kwargs):
        if self.trade_type == "Buy":
            previous_trades = Trade.objects.filter(
                company_name=self.company_name,
                trade_type="Buy"
            )
            previous_quantity = previous_trades.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
            if previous_quantity is None:
                previous_quantity = 0
            self.balance_quantity = self.quantity + previous_quantity

            total_buying_amount = previous_trades.aggregate(total_amount=models.Sum('amount'))['total_amount']
            total_buying_quantity = previous_trades.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
            if total_buying_amount is not None and total_buying_quantity is not None:
                self.avg_purchase_price = total_buying_amount / total_buying_quantity
            else:
                self.avg_purchase_price = None

        elif self.trade_type == "Sell":
            previous_trades = Trade.objects.filter(
                company_name=self.company_name,
                trade_type="Buy"
            )
            previous_quantity = previous_trades.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
            if previous_quantity is None:
                previous_quantity = 0
            self.balance_quantity = previous_quantity - self.quantity

            total_buying_amount = previous_trades.aggregate(total_amount=models.Sum('amount'))['total_amount']
            total_buying_quantity = previous_trades.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
            if total_buying_amount is not None and total_buying_quantity is not None:
                self.avg_purchase_price = total_buying_amount / total_buying_quantity
            else:
                self.avg_purchase_price = None

        elif self.trade_type == "Split":
            previous_trades = Trade.objects.filter(
                company_name=self.company_name,
                trade_type="Buy"
            )
            previous_quantity = previous_trades.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
            if previous_quantity is None:
                previous_quantity = 0

            split_ratio_x = self.split_ratio_x if self.split_ratio_x is not None else 1
            split_ratio_y = self.split_ratio_y if self.split_ratio_y is not None else 1

            self.balance_quantity = (previous_quantity * split_ratio_x) / (self.quantity * split_ratio_y)

            total_buying_amount = previous_trades.aggregate(total_amount=models.Sum('amount'))['total_amount']
            total_buying_quantity = previous_trades.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
            if total_buying_amount is not None and total_buying_quantity is not None:
                self.avg_purchase_price = total_buying_amount / (total_buying_quantity * split_ratio_x / split_ratio_y)
            else:
                self.avg_purchase_price = None

        self.amount = self.quantity * self.buy_price

        super(Trade, self).save(*args, **kwargs)
