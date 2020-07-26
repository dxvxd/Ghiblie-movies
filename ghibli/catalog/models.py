from django.db import models


class Film(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Character(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    films = models.ManyToManyField(Film, related_name='characters')

    def __str__(self):
        return self.name
