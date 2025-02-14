from rest_framework.test import APITestCase, APIClient

from api import models
from api.tests import factories


class LogoutPasswordsTestCase(APITestCase):
    def test_get_passwords_401(self):
        response = self.client.get("/api/passwords/")
        self.assertEqual(401, response.status_code)


class LoginPasswordsTestCase(APITestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_empty_passwords(self):
        request = self.client.get("/api/passwords/")
        self.assertEqual(0, len(request.data["results"]))

    def test_retrieve_its_own_passwords(self):
        password = factories.PasswordFactory(user=self.user)
        request = self.client.get("/api/passwords/")
        self.assertEqual(1, len(request.data["results"]))
        self.assertEqual(password.site, request.data["results"][0]["site"])

    def test_cant_retrieve_other_passwords(self):
        not_my_password = factories.PasswordFactory(user=factories.UserFactory())
        request = self.client.get("/api/passwords/%s/" % not_my_password.id)
        self.assertEqual(404, request.status_code)

    def test_delete_its_own_passwords(self):
        password = factories.PasswordFactory(user=self.user)
        self.assertEqual(1, models.Password.objects.all().count())
        request = self.client.delete("/api/passwords/%s/" % password.id)
        self.assertEqual(204, request.status_code)
        self.assertEqual(0, models.Password.objects.all().count())

    def test_cant_delete_other_password(self):
        not_my_password = factories.PasswordFactory(user=factories.UserFactory())
        self.assertEqual(1, models.Password.objects.all().count())
        request = self.client.delete("/api/passwords/%s/" % not_my_password.id)
        self.assertEqual(404, request.status_code)
        self.assertEqual(1, models.Password.objects.all().count())

    def test_create_password_old_api(self):
        password = {
            "site": "lesspass.com",
            "login": "test@lesspass.com",
            "lowercase": False,
            "uppercase": True,
            "numbers": False,
            "symbols": False,
            "counter": 2,
            "length": 12,
        }
        self.assertEqual(0, models.Password.objects.count())
        self.client.post("/api/passwords/", password)
        self.assertEqual(1, models.Password.objects.count())
        profile = models.Password.objects.first()
        self.assertEqual(profile.site, "lesspass.com")
        self.assertEqual(profile.login, "test@lesspass.com")
        self.assertFalse(profile.lowercase)
        self.assertTrue(profile.uppercase)
        self.assertFalse(profile.digits)
        self.assertFalse(profile.symbols)
        self.assertEqual(profile.counter, 2)
        self.assertEqual(profile.length, 12)
        self.assertEqual(profile.version, 2)

    def test_create_password_with_missing_s_old_api(self):
        password = {
            "site": "lesspass.com",
            "login": "test@lesspass.com",
            "lowercase": True,
            "uppercase": True,
            "number": False,
            "symbol": False,
            "counter": 1,
            "length": 16,
            "version": 2,
        }
        self.client.post("/api/passwords/", password)
        profile = models.Password.objects.first()
        self.assertFalse(profile.digits)
        self.assertFalse(profile.symbols)

    def test_create_password_v2(self):
        password = {
            "site": "lesspass.com",
            "login": "testv2@lesspass.com",
            "lowercase": True,
            "uppercase": False,
            "digits": False,
            "symbols": False,
            "counter": 3,
            "length": 16,
            "version": 2,
        }
        self.client.post("/api/passwords/", password)
        profile = models.Password.objects.first()
        self.assertEqual(profile.site, "lesspass.com")
        self.assertEqual(profile.login, "testv2@lesspass.com")
        self.assertTrue(profile.lowercase)
        self.assertFalse(profile.uppercase)
        self.assertFalse(profile.digits)
        self.assertFalse(profile.symbols)
        self.assertEqual(profile.counter, 3)
        self.assertEqual(profile.length, 16)
        self.assertEqual(profile.version, 2)

    def test_update_password(self):
        password = factories.PasswordFactory(user=self.user)
        self.assertNotEqual("facebook.com", password.site)
        new_password = {
            "site": "facebook.com",
            "login": "test@lesspass.com",
            "lowercase": True,
            "uppercase": True,
            "digits": False,
            "symbols": False,
            "counter": 2,
            "length": 20,
            "version": 2,
        }
        request = self.client.put("/api/passwords/%s/" % password.id, new_password)
        self.assertEqual(200, request.status_code, request.content.decode("utf-8"))
        password_updated = models.Password.objects.get(id=password.id)
        self.assertEqual(password_updated.site, "facebook.com")
        self.assertEqual(password_updated.login, "test@lesspass.com")
        self.assertTrue(password_updated.lowercase)
        self.assertTrue(password_updated.uppercase)
        self.assertFalse(password_updated.digits)
        self.assertFalse(password_updated.symbols)
        self.assertEqual(password_updated.counter, 2)
        self.assertEqual(password_updated.length, 20)
        self.assertEqual(password_updated.version, 2)

    def test_cant_update_other_password(self):
        not_my_password = factories.PasswordFactory(user=factories.UserFactory())
        self.assertEqual("lesspass.com", not_my_password.site)
        new_password = {
            "site": "facebook",
        }
        request = self.client.put(
            "/api/passwords/%s/" % not_my_password.id, new_password
        )
        self.assertEqual(404, request.status_code)
        self.assertEqual(1, models.Password.objects.all().count())
