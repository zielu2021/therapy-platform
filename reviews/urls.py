from django.urls import path
from .views import all_reviews, delete_review, edit_review, leave_review, review_error


urlpatterns = [
    path("leave_review/", leave_review, name="leave_review"),
    path("all/", all_reviews, name="all_reviews"),
    path("review_error/", review_error, name="review_error"),
    path("edit_review/<int:review_id>/", edit_review, name="edit_review"),
    path("delete_review/<int:review_id>/", delete_review, name="delete_review"),
]
