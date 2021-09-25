from django.test import TestCase
from .models import StallionUser as User

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username="john",
            password="l33tPa55word",
            email="john@ecorp.com",
            bio="Just a sweet person",
            firstname="john",
            lastname="doe",
            gender="Homme",
            location="Abidjan",
            phone_number="+225 00 00 00 00 00",
        )

    def test_user_creation(self):
        user = User.objects.get(username="john")
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, "john")
        self.assertEqual(user.email, "john@ecorp.com")
        self.assertEqual(user.bio, "Just a sweet person")
        self.assertEqual(user.firstname, "john")
        self.assertEqual(user.lastname, "doe")
        self.assertEqual(user.gender, "Homme")
        self.assertEqual(user.location, "Abidjan")
        self.assertEqual(user.phone_number, "+225 00 00 00 00 00")
