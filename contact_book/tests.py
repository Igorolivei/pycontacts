import unittest

from pyramid import testing


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from .views import ContactBook

        request = testing.DummyRequest()
        inst = ContactBook(request)
        response = inst.contact_book()
        self.assertEqual(len(response['contacts']), 3)


class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        from contact_book import main

        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<title>Contact Book - Page</title>', res.body)

    def test_contact_view(self):
        res = self.testapp.get('/2', status=200)
        self.assertIn(b'<title>Contact View - Page</title>', res.body)