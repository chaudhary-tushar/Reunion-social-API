from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from unittest.mock import patch
from django.db.utils import OperationalError
from django.core.management import call_command
from psycopg2 import OperationalError as Psycopg2Error
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from .models import Profile, Post, Comments
import time


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(id_user=1, user=self.user)

    def test_profile_user(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.user.username, 'testuser')

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if db ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for Database when getting Operational error"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(Post_id='123e4567-e89b-12d3-a456-426655440000', user='testuser',
                                        title='Test Post', description='This is a test post')
        self.post.save()

    def test_post_title(self):
        post = Post.objects.get(Post_id='123e4567-e89b-12d3-a456-426655440000')
        self.assertEqual(post.title, 'Test Post')


class TestAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser3', password='testpass3')
        self.profile = Profile.objects.create(id_user=self.user.id, user=self.user)
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.profile2 = Profile.objects.create(id_user=self.user2.id, user=self.user2)
        self.post = Post.objects.create(user=self.user.username, title='Test post', description='Test description')
        self.comment = Comments.objects.create( comment='Test comment')
        gettoken= self.client.post('/api/authenticate/', {'username': 'testuser3', 'password': 'testpass3'})
        self.token=gettoken.data['access']

    def test_authenticate(self):
        # Test authentication with valid credentials
        response = self.client.post('/api/authenticate/', {'username': 'testuser3', 'password': 'testpass3'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Test authentication with invalid credentials
        response = self.client.post('/api/authenticate/', {'username': 'testuser3', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follow(self):
        
        
        # self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(f'/api/follow/{self.profile2.id_user}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('success', response.data)
        self.profile2.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertIn(str(self.profile.user.username), self.profile2.followers)
        self.assertIn(str(self.profile2.user.username), self.profile.following)
        #self.assertEqual(self.profile2.followers, [str(self.profile.user.username)])

    def test_unfollow(self):
        # Authenticate the user and get the self.token
        
        self.client.force_authenticate(user=self.user)
        self.profile.following = [str(self.profile2.user.username)]
        self.profile2.followers = [str(self.profile.user.username)]
        self.profile.save()
        self.profile2.save()
        self.profile2.refresh_from_db()
        self.profile.refresh_from_db()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(f'/api/unfollow/{self.profile2.id_user}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED )
        self.assertIn('success', response.data)
        self.profile2.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.following, [])
        self.assertEqual(self.profile2.followers, [])

    def test_like(self):
        # Authenticate the user and get the self.token
        
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(f'/api/like/{self.post.Post_id}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('success', response.data)
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes, [self.user.username])

    def test_unlike(self):
        # Authenticate the user and get the self.token
        
        
        self.client.force_authenticate(user=self.user)
        self.post.likes = [self.user.username]
        self.post.save()
        self.post.refresh_from_db()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(f'/api/unlike/{self.post.Post_id}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('success', response.data)
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes, [])

    def test_add_comment(self):
        # Authenticate the user and get the self.token
        

        # Add a comment to the post
        comment_data = {'comment': 'Test comment'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(f'/api/comment/{self.post.Post_id}', comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the comment was added to the post
        post = Post.objects.get(Post_id=self.post.Post_id)
        self.assertEqual(post.count_comments, 1)
        # [f'{self.profile.user.username}']
        self.assertIn(str({f'{self.profile.user.username}': 'Test comment'}),post.comments)
        
    def test_get_user_profile(self):
        
        url = reverse('getuser')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        
        url = reverse('post')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "title": "Test Post 2",
            "description": "This is another test post"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post(self):
        
        url = reverse('getdelete', args=[self.post.Post_id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        
        url = reverse('getdelete', args=[self.post.Post_id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK )

    def test_get_all_posts(self):
        
        url = reverse('all-post')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
