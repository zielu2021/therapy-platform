from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from blog.models import Post
from reviews.models import Review
from .models import PDFFile

# Create your views here.


def index(request):
    try:
        latest_post = Post.objects.latest("created_on")
    except Post.DoesNotExist:
        latest_post = None

    reviews = Review.objects.all().order_by("-id")[:5]

    context = {
        "latest_post": latest_post,
        "reviews": reviews,
    }

    return render(request, "home/index.html", context)


@login_required
def download_pdf(request, pdf_id):
    pdf_file = get_object_or_404(PDFFile, pk=pdf_id)

    with open(pdf_file.pdf_file.path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{pdf_file.title}.pdf"'

    return response


def service(request):
    return render(request, "home/service.html")
