from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("service", views.service, name="service"),
    path("download-pdf/<int:pdf_id>/", views.download_pdf, name="download_pdf"),
]
