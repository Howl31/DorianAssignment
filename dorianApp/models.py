from django.db import models

# Create your models here.


class InsurerMaster(models.Model):
    insurer = models.CharField(max_length=100, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    clubbed_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return self.clubbed_name
    

class LOBMaster(models.Model):
    lob = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return self.lob
    

class CategoryMaster(models.Model):
    clubbed_name = models.CharField(max_length=100, null=False, blank=False)
    category = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return self.category
    

class MonthMaster(models.Model):
    month = models.CharField(max_length=100, null=False, blank=False)
    month_num = models.IntegerField(null=False, blank=False)

    def __int__(self):
        return self.month
    

class InsurerValue(models.Model):
    year = models.CharField(max_length=10, null=False, blank=False)
    month = models.CharField(max_length=10, null=False, blank=False)
    category = models.ForeignKey(CategoryMaster, on_delete=models.DO_NOTHING, null=False, blank=False)
    product = models.ForeignKey(LOBMaster, on_delete=models.DO_NOTHING, null=False, blank=False)
    value = models.FloatField(null=False, blank=False)