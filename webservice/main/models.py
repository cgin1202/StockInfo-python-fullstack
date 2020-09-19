from django.db import models

# Create your models here.

class US_Stock(models.Model):
    id=models.BigIntegerField(primary_key=True)
    symbol=models.CharField(max_length=50)
    date=models.DateTimeField()
    highvalue=models.FloatField()
    lowvalue=models.FloatField()
    openvalue=models.FloatField()
    closevalue=models.FloatField()
    volumevalue=models.FloatField()
    adjclosevalue=models.FloatField()

    def __str__(self):
        return [self.symbol, self.date, self.highvalue, self.lowvalue, self.openvalue, self.closevalue, self.volumevalue, self.adjclosevalue]