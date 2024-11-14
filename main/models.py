from django.db import models
from cloudinary.models import CloudinaryField

"""
A model for storing employees' professions.
"""
class Position(models.Model):
    name = models.CharField(max_length=30, blank=False)
    salary = models.FloatField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        ordering = ['-salary']

"""
A model for storing information on female workers.
"""
class Worker(models.Model):
    first_name = models.CharField(max_length=25, blank=False)
    second_name = models.CharField(max_length=25, blank=False)
    photo = CloudinaryField('image')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.second_name} ({self.position})"
    
    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'
        ordering = ['-first_name', '-second_name']
