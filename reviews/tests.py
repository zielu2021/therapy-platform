from accounts.models import CustomUser as User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Review
from django.utils import timezone


class ReviewModelTest(TestCase):

    def setUp(self):
        # Create two test users with unique email addresses
        self.user1 = User.objects.create_user(username="user1", password="password1", email="user1@example.com")
        self.user2 = User.objects.create_user(username="user2", password="password2", email="user2@example.com")

    def test_reviews_ordered_by_created_on(self):
        # Create reviews with different users
        review1 = Review.objects.create(
            author=self.user1, text="Review 1", rating=4, created_on=timezone.now()
        )
        review2 = Review.objects.create(
            author=self.user2,
            text="Review 2",
            rating=3,
            created_on=timezone.now() + timezone.timedelta(days=1),
        )

        # Check that the reviews are ordered by created_on in descending order
        reviews = Review.objects.all()
        self.assertEqual(reviews[0], review2)
        self.assertEqual(reviews[1], review1)


class DeleteReviewViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a review for the test user
        self.review = Review.objects.create(
            author=self.user, text="Test review", rating=5
        )

        # Set up the Django test client
        self.client = Client()

    def test_delete_review_requires_login(self):
        # Access the delete_review view without logging in
        response = self.client.get(reverse("delete_review", args=[self.review.id]))

        # Check that the response status code is 404 (Page Not Found)
        # If the view requires login, it should return a redirect (302)
        self.assertEqual(response.status_code, 404)

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Access the delete_review view again after logging in
        response_after_login = self.client.get(
            reverse("delete_review", args=[self.review.id])
        )

        # Check that the response status code is now 200 (successful access)
        self.assertEqual(response_after_login.status_code, 200)

        # You can add more assertions based on your specific requirements


class EditReviewViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a review for the test user
        self.review = Review.objects.create(
            author=self.user, text="Test review", rating=5
        )

        # Set up the Django test client
        self.client = Client()

    def test_edit_review_requires_login(self):
        # Access the edit_review view without logging in
        response = self.client.get(reverse("edit_review", args=[self.review.id]))

        # Check that the response status code is 302 (redirect to login)
        self.assertEqual(response.status_code, 302)

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Access the edit_review view again after logging in
        response_after_login = self.client.get(
            reverse("edit_review", args=[self.review.id])
        )

        # Check that the response status code is now 200 (successful access)
        self.assertEqual(response_after_login.status_code, 200)

    def test_edit_review_form_submission(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Access the edit_review view to get the initial form
        response = self.client.get(reverse("edit_review", args=[self.review.id]))

        # Check that the response status code is 200 (successful access)
        self.assertEqual(response.status_code, 200)

        # Create a valid form submission data (adjust as needed based on your form)
        form_data = {
            "text": "Updated review text",
            "rating": 4,
        }

        # Submit the form with a POST request
        response_after_submission = self.client.post(
            reverse("edit_review", args=[self.review.id]), form_data
        )

        # Check that the form submission redirects to 'all_reviews'
        self.assertRedirects(response_after_submission, reverse("all_reviews"))

        # Check that the review was updated in the database
        updated_review = Review.objects.get(id=self.review.id)
        self.assertEqual(updated_review.text, "Updated review text")
        self.assertEqual(updated_review.rating, 4)

        # You can add more assertions based on your specific requirements


class LeaveReviewViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Set up the Django test client
        self.client = Client()

    def test_leave_review_requires_login(self):
        # Access the leave_review view without logging in
        response = self.client.get(reverse("leave_review"))

        # Check that the response status code is 302 (redirect to login)
        self.assertEqual(response.status_code, 302)

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Access the leave_review view again after logging in
        response_after_login = self.client.get(reverse("leave_review"))

        # Check that the response status code is now 200 (successful access)
        self.assertEqual(response_after_login.status_code, 200)

    def test_leave_review_with_existing_review(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Create a review for the test user
        Review.objects.create(author=self.user, text="Existing review", rating=5)

        # Access the leave_review view
        response = self.client.get(reverse("leave_review"))

        # Check that the response status code is 200 (successful access)
        self.assertEqual(response.status_code, 200)

        # Check that the user is redirected to 'review_error' template
        self.assertTemplateUsed(response, "reviews/review_error.html")

    def test_leave_review_form_submission(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Access the leave_review view to get the initial form
        response = self.client.get(reverse("leave_review"))

        # Check that the response status code is 200 (successful access)
        self.assertEqual(response.status_code, 200)

        # Create a valid form submission data (adjust as needed based on your form)
        form_data = {
            "text": "New review text",
            "rating": 4,
        }

        # Submit the form with a POST request
        response_after_submission = self.client.post(reverse("leave_review"), form_data)

        # Check that the form submission redirects to 'all_reviews'
        self.assertRedirects(response_after_submission, reverse("all_reviews"))

        # Check that the review was created in the database
        created_review = Review.objects.filter(author=self.user).first()
        self.assertIsNotNone(created_review)
        self.assertEqual(created_review.text, "New review text")
        self.assertEqual(created_review.rating, 4)
