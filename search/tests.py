from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from account.models import User
from post.models import Post


class SearchViewTests(TestCase):
    def setUp(self):
        """
        Set up test environment including creating users and posts.
        """
        self.client = APIClient()

        # Create users
        self.user1 = User.objects.create_user(
            email="user1@example.com", name="User One", password="password1"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", name="User Two", password="password2"
        )

        # Create posts
        self.post1 = Post.objects.create(
            body="Public post about dogs", created_by=self.user1
        )
        self.post2 = Post.objects.create(
            body="Private post about cats",
            created_by=self.user1, is_private=True
        )
        self.post3 = Post.objects.create(
            body="Public post about birds", created_by=self.user2
        )

        # Authenticate user1
        self.client.force_authenticate(user=self.user1)

    def test_search(self):
        """
        Test searching for posts based on query.
        """
        url = reverse("search")
        query = "dogs"

        response = self.client.post(url, {"query": query}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posts = response.json()["posts"]
        self.assertTrue(
            any(post["body"] == "Public post about dogs" for post in posts))
        self.assertFalse(
            any(post["body"] == "Private post about cats" for post in posts)
        )
        self.assertFalse(
            any(post["body"] == "Public post about birds" for post in posts)
        )

    def test_search_no_results(self):
        """
        Test searching for a query with no matching results.
        """
        url = reverse("search")
        query = "elephants"
        response = self.client.post(url, {"query": query}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["users"]), 0)
        self.assertEqual(len(response.json()["posts"]), 0)

    def test_search_unauthenticated(self):
        """
        Test searching when user is not authenticated.
        """
        unauthenticated_client = APIClient()

        url = reverse("search")
        query = "birds"
        response = unauthenticated_client.post(
            url, {"query": query}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
