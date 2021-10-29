from django.db import models
from django.db.models.base import Model

class DataSets(models.Model):
    user_name = models.CharField(max_length=255)
    dataset_name = models.CharField(max_length=255)


class DataValues(models.Model):
    dataset = models.ForeignKey(DataSets, on_delete=models.CASCADE)
    value = models.FloatField()


class SetScore(models.Model):
    dataset = models.ForeignKey(DataSets, on_delete=models.CASCADE)
    value = models.FloatField()


class ColumnNames(models.Model):
    dataset = models.ForeignKey(DataSets, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=63)

class BenfordDistributions(models.Model):
    dataset = models.ForeignKey(DataSets, on_delete=models.CASCADE)
    number = models.IntegerField()
    occurence = models.FloatField()
    bensfords = models.FloatField()