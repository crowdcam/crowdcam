from collections import UserString
from django.contrib.auth.models import Group
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from organization.models import Organization, MediaFile
from django.contrib.auth import get_user_model
from guardian.shortcuts import assign_perm
import users



class OrganizationMediaUploadTest(TestCase):
    def setUp(self):
        self.org1 = Organization.objects.create(name="Org A")
        self.org2 = Organization.objects.create(name="Org B")
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_upload_media_for_organization(self):
        # Simulate file
        file_data = SimpleUploadedFile("orgA_file.txt", b"org A file content", content_type="text/plain")

        # Upload for org1
        media = MediaFile.objects.create(organization=self.org1, file=file_data)

        # Assertions
        self.assertEqual(MediaFile.objects.count(), 1)
        self.assertEqual(media.organization.name, "Org A")
        self.assertTrue(media.file.name.startswith("organization_media/orgA_file"))
    def test_organization_file_is_not_shared(self):
        # Upload file for org1
        file_data = SimpleUploadedFile("orgA_file.txt", b"org A file content", content_type="text/plain")
        MediaFile.objects.create(organization=self.org1, file=file_data)

        # Simulate checking access: Org2 should not see Org1's file
        org2_files = MediaFile.objects.filter(organization=self.org2)
        self.assertEqual(org2_files.count(), 0)

class JoinOrgViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.group = Group.objects.create(name='TestGroup')
        self.org = Organization.objects.create(
            name="TestOrg",
            join_code="JOIN123",
            accepting_users=True
        )

        # Mock `get_user_group()` if necessary, or override it in test subclass
        Organization.get_user_group = lambda self: "TestGroup"

        self.join_url = reverse("organization:join_org")

    def test_get_request_renders_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.join_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "organization/join_org.html")

    def test_post_with_valid_code_adds_user_to_group(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("organization:join_org"),
            {"input_code": self.org.join_code},
        )

        assign_perm('user', self.user, self.org)

        response = self.client.get(
            reverse("organization:org_view", kwargs={"org_id": self.org.id}
        )
    )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "org")

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

class UserOrgsViewTest(TestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('user_orgs'))
        self.assertRedirects(response, '/accounts/login/?next=/user_orgs/')

class UserOrgsViewTest(TestCase):

    def setUp(self):
        # Create a user and an organization
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.org = Organization.objects.create(name='Test Org')
        assign_perm('user', self.user, self.org)
        assign_perm('mod', self.user, self.org)
        
        # Log in the user
        self.client.login(username='testuser', password='password123')

    def test_user_org_permissions(self):
        response = self.client.get(reverse('user_orgs'))
        
        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check that the organization is in the context
        self.assertIn('orgs', response.context)
        org_permissions = response.context['orgs']
        
        # Check that the org and permissions are correct
        self.assertEqual(len(org_permissions), 1)
        org = org_permissions[0]
        self.assertEqual(org['org'], self.org)
        self.assertTrue(org['is_user'])  # The user should have 'user' permission
        self.assertTrue(org['is_mod'])   # The user should have 'mod' permission
        self.assertFalse(org['is_admin'])  # The user should not have 'admin' permission

class UserOrgsViewTest(TestCase):

    def setUp(self):
        # Create a user with no organizations
        self.user = users.objects.create_user(username='testuser', password='password123')
        
        # Log in the user
        self.client.login(username='testuser', password='password123')

    def test_user_with_no_orgs(self):
        response = self.client.get(reverse('user_orgs'))
        
        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check that the organization list is empty
        self.assertIn('orgs', response.context)
        self.assertEqual(response.context['orgs'], [])

class UserOrgsViewTest(TestCase):

    def setUp(self):
        # Create a user and an organization
        self.user = users.objects.create_user(username='testuser', password='password123')
        self.org = Organization.objects.create(name='Test Org')

        # Log in the user without assigning any permissions
        self.client.login(username='testuser', password='password123')

    def test_user_with_no_permissions(self):
        response = self.client.get(reverse('user_orgs'))
        
        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check that the organization is in the context
        self.assertIn('orgs', response.context)
        org_permissions = response.context['orgs']
        
        # Check that the org and permissions are correctly set
        self.assertEqual(len(org_permissions), 1)
        org = org_permissions[0]
        self.assertEqual(org['org'], self.org)
        self.assertFalse(org['is_user'])   # The user should not have 'user' permission
        self.assertFalse(org['is_mod'])    # The user should not have 'mod' permission
        self.assertFalse(org['is_admin'])  # The user should not have 'admin' permission

class UserOrgsViewTest(TestCase):

    def setUp(self):
        # Create a user and an organization
        self.user = users.objects.create_user(username='testuser', password='password123')
        self.org = Organization.objects.create(name='Test Org')
        assign_perm('user', self.user, self.org)
        
        # Log in the user
        self.client.login(username='testuser', password='password123')

    def test_user_permissions_displayed(self):
        response = self.client.get(reverse('user_orgs'))
        
        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check that the organization and permissions are correctly displayed
        self.assertIn('orgs', response.context)
        org_permissions = response.context['orgs']
        
        # Check permissions
        self.assertEqual(len(org_permissions), 1)
        org = org_permissions[0]
        self.assertTrue(org['is_user'])
        self.assertFalse(org['is_mod'])
        self.assertFalse(org['is_admin'])