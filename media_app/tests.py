from django.test import TestCase
from django.contrib.auth.models import User
from media_app.models import Media, Tag
from organization.models import Organization  # Assuming this exists
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile

class MediaTagModelTest(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create organization
        self.organization = Organization.objects.create(name='Test Org')

        # Create tag
        self.tag = Tag.objects.create(name='Nature', organization=self.organization)

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Nature')
        self.assertEqual(self.tag.organization.name, 'Test Org')
        self.assertEqual(str(self.tag), 'Nature')
        self.assertEqual(self.tag.bg_color, '#F07857')  # default color

    def test_media_creation_and_filename(self):
        # Simulate an uploaded file
        file = SimpleUploadedFile("sunset.jpg", b"file_content", content_type="image/jpeg")

        media = Media.objects.create(
            media_path=file,
            user=self.user,
            organization=self.organization,
            status=None
        )
        media.tag.add(self.tag)

        self.assertTrue(media.pk is not None)
        self.assertIn('sunset.jpg', str(media))
        self.assertEqual(media.getFileName(), 'sunset.jpg')
        self.assertEqual(media.file_name, 'sunset.jpg')

    def test_human_status(self):
        media1 = Media.objects.create(media_path=SimpleUploadedFile("a.jpg", b"123"), user=self.user, organization=self.organization, status=None)
        media2 = Media.objects.create(media_path=SimpleUploadedFile("b.jpg", b"123"), user=self.user, organization=self.organization, status=True)
        media3 = Media.objects.create(media_path=SimpleUploadedFile("c.jpg", b"123"), user=self.user, organization=self.organization, status=False)

        self.assertEqual(media1.human_status, "Awaiting Approval")
        self.assertEqual(media2.human_status, "Approved")
        self.assertEqual(media3.human_status, "Rejected")
