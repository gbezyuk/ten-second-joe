"""
Studio: ActionLearning.Ru
Authors: Andrew Sinitsyn, Grigoriy Beziuk
Project: Ten Second Joe
Module: Ten Second Joe
Part: Tests
"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import LimitedLink, LimitedLinkExpired
import factory

class UserFactory(factory.Factory):
    """
    User model factory
    """
    FACTORY_FOR = User
    username = 'sample_user'
    is_active = True

class LimitedLinkFactory(factory.Factory):
    """
    LimitedLink model factory
    """
    FACTORY_FOR = LimitedLink

    slug = 'slug'
    enabled = True
    usages_left = 100

class LimitedLinkModelTest(TestCase):
    """
    Testing LimitedLink model custom methods
    """
    def setUp(self):
        self.sample_user = UserFactory()

    def test_link_is_accessible_property(self):
        """
        Tests that link.is_accessible property works fine
        """
        link = LimitedLinkFactory(content_object=self.sample_user, usages_left=0, enabled=False)
        self.assertFalse(link.is_accessible)
        link.enabled = True
        self.assertTrue(link.is_accessible)
        link.usages_left = 1
        self.assertTrue(link.is_accessible)
        link.enabled = False
        self.assertFalse(link.is_accessible)
        link.enabled = True
        self.assertTrue(link.is_accessible)

    def test_link_usage_limiting(self):
        """
        Basic test case
        """
        link = LimitedLinkFactory(content_object=self.sample_user, usages_left=3, enabled=True)
        self.assertTrue(link.is_accessible)
        self.assertEqual(link.usages_count, 0)
        self.assertEquals(self.sample_user, link.get_access())
        self.assertTrue(link.is_accessible)
        self.assertEqual(link.usages_count, 1)
        self.assertEqual(link.usages_left, 2)
        self.assertEquals(self.sample_user, link.get_access())
        self.assertTrue(link.is_accessible)
        self.assertEqual(link.usages_count, 2)
        self.assertEqual(link.usages_left, 1)
        self.assertEquals(self.sample_user, link.get_access())
        self.assertFalse(link.is_accessible)
        self.assertEqual(link.usages_count, 3)
        self.assertEqual(link.usages_left, 0)
        self.assertRaises(LimitedLinkExpired, link.get_access)
