from django.db import models


class DataURL(models.Model):
    """
    URLs for fetching data are stored in this model.
    """
    name = models.CharField(primary_key=True, max_length=50)
    url = models.URLField()
    data_hash = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name

    def update_hash(self, new_hash):
        self.data_hash = new_hash
        self.save()
