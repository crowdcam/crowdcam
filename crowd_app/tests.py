from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from media_app.models import Media
from organization.models import Organization

class IndexViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.org = Organization.objects.create(name='Test Org', join_code='test123', accepting_users=True)
    def test_index_view_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('crowd_app:home'))
        self.assertEqual(response.status_code, 200)

'''

    def test_media_index_view_displays_media(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('media_app:media_index'))
        self.assertEqual(response.status_code, 200)

    def test_media_view_displays_correct_media(self):
        self.client.force_login(self.user)
        file = SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpeg")
        media = Media.objects.create(media_path=file, user=self.user, organization=self.org)
        response = self.client.get(reverse('media_app:media_view', args=[media.id]))
        self.assertContains(response, "media/")
        self.assertEqual(response.status_code, 200)

    def test_upload_view_get_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('media_app:upload'))
        self.assertEqual(response.status_code, 200)

    def test_upload_view_post_valid_data(self):
        self.client.force_login(self.user)
        file = SimpleUploadedFile( "testfile.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('media_app:upload'), {
            'media_path': file,
            'organization': self.org.id,
        })
        self.assertEqual(response.status_code, 200)
'''