from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from account.models import User, FriendshipRequest

class ViewTests(TestCase):
    def setUp(self):
        """
        Set up test environment including creating users and logging in.
        """
        self.client = APIClient()
        self.user1 = User.objects.create_user(email='user1@example.com', name='User One', password='password1')
        self.user2 = User.objects.create_user(email='user2@example.com', name='User Two', password='password2')
        self.client.force_authenticate(user=self.user1)  # Authenticate the client

    def test_me_view(self):
        """
        Test retrieving the authenticated user's profile information.
        """
        response = self.client.get(reverse('me'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], str(self.user1.id))
        self.assertEqual(response.json()['name'], self.user1.name)
        self.assertEqual(response.json()['email'], self.user1.email)

    def test_signup_view(self):
        """
        Test user signup functionality.
        """
        response = self.client.post(reverse('signup'), {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password1': '##qwert##',
            'password2': '##qwert##'
        })

        if 'password2' in response.json():
            self.assertIn('password_too_common', response.json()['password2'][0]['code'])
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('success', response.json()['message'])

    def test_friends_view(self):
        """
        Test retrieving the friends list and friendship requests for a user.
        """
        FriendshipRequest.objects.create(created_for=self.user2, created_by=self.user1)
        response = self.client.get(reverse('friends', kwargs={'pk': self.user2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.json())
        self.assertIn('friends', response.json())
        self.assertIn('requests', response.json())

    def test_handle_request_view(self):
        """
        Test handling (accepting/rejecting) a friendship request.
        """
        FriendshipRequest.objects.create(created_for=self.user1, created_by=self.user2)
        response = self.client.post(reverse('handle_request', kwargs={'pk': self.user2.id, 'status': 'accepted'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'friendship request updated')

    def test_editprofile_view(self):
        """
        Test editing the authenticated user's profile information.
        """
        response = self.client.post(reverse('editprofile'), {
            'email': 'user1_new@example.com',
            'name': 'User One Updated'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'information updated')
        self.assertEqual(response.json()['user']['email'], 'user1_new@example.com')
        self.assertEqual(response.json()['user']['name'], 'User One Updated')
