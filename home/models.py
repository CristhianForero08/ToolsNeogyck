from django.db import models

class SearchQuery(models.Model):
    keyword = models.CharField(max_length=255)
    url = models.URLField()
    position = models.IntegerField(null=True, blank=True)  # Permitir que sea nulo si no se encuentra la posición
    country = models.CharField(max_length=5, default='us')
    language = models.CharField(max_length=5, default='en')
    email = models.EmailField()
    accept_terms = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query: {self.keyword}, URL: {self.url}, Position: {self.position}, Email: {self.email}"
