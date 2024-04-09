from django.db import models


# Create your models here.
class PDFFile(models.Model):
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to="pdfs/%Y/%m/%d/", blank=True, null=True)

    def __str__(self):
        return self.title
