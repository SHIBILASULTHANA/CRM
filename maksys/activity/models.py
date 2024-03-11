from django.db import models

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class List(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')

    def __str__(self):
        return str(self.name)

class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)