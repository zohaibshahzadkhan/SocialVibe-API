from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from account.models import User
from .models import Post, Like, Comment, PostAttachment
from .serializers import PostSerializer

class ViewTests(TestCase):
    def setUp(self):
        """
        Set up test environment including creating users and logging in.
        """
        self.client = APIClient()
        self.user1 = User.objects.create_user(email='user1@example.com', name='User One', password='password1')
        self.user2 = User.objects.create_user(email='user2@example.com', name='User Two', password='password2')
        self.client.force_authenticate(user=self.user1)  # Authenticate the client

        # Create some posts for testing
        self.post1 = Post.objects.create(body="Test Post 1", created_by=self.user1)
        self.post2 = Post.objects.create(body="Test Post 2", created_by=self.user2)
        self.post3 = Post.objects.create(body="Test Post 3", created_by=self.user2)

    def test_post_list(self):
        """
        Test retrieving a list of posts.
        """
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.json(), serializer.data)

    def test_post_list_profile(self):
        """
        Test retrieving a list of posts for a user profile.
        """
        response = self.client.get(reverse('post_list_profile', kwargs={'id': self.user2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['posts']), 2)
        self.assertEqual(response.json()['user']['id'], str(self.user2.id))

    def test_post_create(self):
        """
        Test creating a new post.
        """
        initial_count = Post.objects.count()
        response = self.client.post(reverse('post_create'), {
            'body': 'New test post',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), initial_count + 1)
        self.assertEqual(response.json()['body'], 'New test post')

    def test_post_like(self):
        """
        Test liking a post.
        """
        post_to_like = self.post1
        response = self.client.post(reverse('post_like', kwargs={'pk': post_to_like.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'like created')

        # Test liking the same post again (should not create another like)
        response = self.client.post(reverse('post_like', kwargs={'pk': post_to_like.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'post already liked')

    def test_post_detail(self):
        """
        Test retrieving details of a specific post.
        """
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['post']['id'], str(self.post1.id))
        self.assertEqual(response.json()['post']['body'], self.post1.body)

    def test_post_create_comment(self):
        """
        Test creating a comment on a post.
        """
        initial_count = Comment.objects.count()
        response = self.client.post(reverse('post_create_comment', kwargs={'pk': self.post1.id}), {
            'body': 'New comment on post 1',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), initial_count + 1)
        self.assertEqual(response.json()['body'], 'New comment on post 1')

    def test_post_delete(self):
        """
        Test deleting a post.
        """
        initial_count = Post.objects.count()
        response = self.client.delete(reverse('post_delete', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), initial_count - 1)
        self.assertEqual(response.json()['message'], 'post deleted')
    
    def tearDown(self):
        """
        Clean up after each test.
        """
        Post.objects.all().delete()
        Like.objects.all().delete()
        Comment.objects.all().delete()
        PostAttachment.objects.all().delete()

        self.user1.delete()
        self.user2.delete()
