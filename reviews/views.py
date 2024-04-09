from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from .forms import ReviewForm
from .models import Review


@login_required
def leave_review(request):
    user_reviews = Review.objects.filter(author=request.user)

    if user_reviews.exists():
        return render(
            request,
            "reviews/review_error.html",
            {"message": _("You have already submitted a review.")},
        )

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect("all_reviews")
    else:
        form = ReviewForm()

    return render(request, "reviews/leave_review.html", {"form": form})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, author=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("all_reviews")
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/edit_review.html", {"form": form, "review": review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, author=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, _("Review deleted successfully."))
        return redirect("all_reviews")

    return render(request, "reviews/delete_review.html", {"review": review})


def all_reviews(request):
    reviews = Review.objects.all()
    return render(request, "reviews/all_reviews.html", {"reviews": reviews})


def review_error(request):
    message = _("You have already submitted a review.")
    return render(request, "reviews/review_error.html", {"message": message})
