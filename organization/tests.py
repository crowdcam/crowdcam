from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from organization.models import Organization, MediaFile
from guardian.shortcuts import assign_perm

User = get_user_model()

class OrganizationMediaUploadTest(TestCase):
    def setUp(self):
        self.org1 = Organization.objects.create(name="Org A", slug="org-a")
        self.org2 = Organization.objects.create(name="Org B", slug="org-b")
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_upload_media_for_organization(self):
        file_data = SimpleUploadedFile("orgA_file.txt", b"org A file content", content_type="text/plain")
        media = MediaFile.objects.create(organization=self.org1, file=file_data)

        self.assertEqual(MediaFile.objects.count(), 1)
        self.assertEqual(media.organization.name, "Org A")
        self.assertTrue(media.file.name.startswith("organization_media/orgA_file"))

    def test_organization_file_is_not_shared(self):
        file_data = SimpleUploadedFile("orgA_file.txt", b"org A file content", content_type="text/plain")
        MediaFile.objects.create(organization=self.org1, file=file_data)

        org2_files = MediaFile.objects.filter(organization=self.org2)
        self.assertEqual(org2_files.count(), 0)

class JoinOrgViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.group = Group.objects.create(name='TestGroup')
        self.org = Organization.objects.create(name="TestOrg", join_code="JOIN123", accepting_users=True, slug="testorg")

        Organization.get_user_group = lambda self: "TestGroup"
        self.join_url = reverse("organization:join_org")

    def test_get_request_renders_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.join_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "organization/join_org.html")

    def test_post_with_valid_code_adds_user_to_group(self):
        self.client.force_login(self.user)
        response = self.client.post(self.join_url, {"input_code": self.org.join_code})
        self.assertRedirects(response, reverse("organization:org_view", kwargs={"org_id": self.org.id})
    )

    def test_post_with_invalid_code_shows_error(self):
        self.client.force_login(self.user)
        response = self.client.post(self.join_url, {"input_code": "WRONGCODE"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid Join Code")

    def test_post_with_non_accepting_org_rejects(self):
        self.org.accepting_users = False
        self.org.save()

        self.client.force_login(self.user)
        response = self.client.post(self.join_url, {"input_code": "JOIN123"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid Join Code")

class UserOrgsViewTestRedirect(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('organization:user_orgs'))
        self.assertRedirects(response, '/users/login/?next=/organization/')

class UserOrgsViewTestWithPermissions(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.org = Organization.objects.create(name='Test Org', slug="test-org")
        assign_perm('user', self.user, self.org)
        assign_perm('mod', self.user, self.org)

        self.client.login(username='testuser', password='password123')

    def test_user_org_permissions(self):
        response = self.client.get(reverse('organization:index'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('orgs', response.context)
        org_permissions = response.context['orgs']

        self.assertEqual(len(org_permissions), 1)
        org = org_permissions[0]
        self.assertEqual(org['org'], self.org)
        self.assertTrue(org['is_user'])
        self.assertTrue(org['is_mod']) 
        self.assertFalse(org['is_admin'])

class UserOrgsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_user_with_no_orgs(self):
        response = self.client.get(reverse('organization:user_orgs'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('orgs', response.context)
        self.assertEqual(response.context['orgs'], [])

class UserOrgsViewTest(TestCase):
    def setUp(self):
        # Create a user and an organization
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.org = Organization.objects.create(name='Test Org')

        self.client.login(username='testuser', password='password123')

    def test_user_with_no_permissions(self):
        response = self.client.get(reverse('organization:user_orgs'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('orgs', response.context)
        org_permissions = response.context['orgs']

        self.assertEqual(len(org_permissions), 1)
        org = org_permissions[0]
        self.assertEqual(org['org'], self.org)
        self.assertFalse(org['is_user']) 
        self.assertFalse(org['is_mod'])   
        self.assertFalse(org['is_admin'])

class UserOrgsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.org = Organization.objects.create(name='Test Org')
        assign_perm('user', self.user, self.org)
        self.client.login(username='testuser', password='password123')

    def test_user_permissions_displayed(self):
        response = self.client.get(reverse('organization:user_orgs'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('orgs', response.context)
        org_permissions = response.context['orgs']

        self.assertEqual(len(org_permissions), 1)
        org = org_permissions[0]
        self.assertTrue(org['is_user'])
        self.assertFalse(org['is_mod'])
        self.assertFalse(org['is_admin'])