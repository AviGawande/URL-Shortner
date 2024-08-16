from django.db import models

class UrlShortner(models.Model):
    long_url = models.CharField(max_length=200)
    alias = models.CharField(max_length=50)

    def __str__(self):
        return self.title

