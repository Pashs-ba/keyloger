from django.db import models
import time

class KeyloggerID(models.Model):
    '''Infected computer's id'''
    def __str__(self):
        return str(self.pk)

    class Meta():
        verbose_name = 'Keylogger Id'

class KeyloggerData(models.Model):
    '''Data that ifected computers send to server'''
    data = models.CharField(max_length=1000, verbose_name='Data', null=True)
    date = models.DateTimeField(verbose_name='Date')
    keylogger_ref = models.ForeignKey(KeyloggerID,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Keylogger data'
        verbose_name_plural = 'Keyloger data'
