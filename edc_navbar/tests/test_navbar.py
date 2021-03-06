from django.test import TestCase, tag
from django.urls.base import reverse

from ..navbar import Navbar
from ..navbar_item import NavbarItem, NavbarItemError
from ..site_navbars import site_navbars, AlreadyRegistered


class TestNavbar(TestCase):

    def setUp(self):
        site_navbars._registry = {}

    def create_navbar(self):
        testnavbar = Navbar(name='pharmacy_dashboard')
        testnavbar.append_item(
            NavbarItem(name='navbar1',
                       title='Navbar1',
                       label='one',
                       url_name='navbar_one_url'))

        testnavbar.append_item(
            NavbarItem(name='navbar2',
                       title='Navbar2',
                       label='two',
                       url_name='navbar_two_url'))
        return testnavbar

    def test_urls(self):
        reverse('navbar_one_url')
        reverse('navbar_two_url')

    def test_site_navbar_register(self):
        navbar = self.create_navbar()
        site_navbars.register(navbar)
        self.assertTrue(navbar.name in site_navbars.registry)
        self.assertRaises(
            AlreadyRegistered,
            site_navbars.register, navbar)

    def test_navbar_item_raises_missing_url(self):
        self.assertRaises(
            NavbarItemError,
            NavbarItem,
            name='navbar_item_one',
            label='Navbar Item One',
            title='navbar_item_one',
            url_name=None)

    def test_navbar_item_raises_bad_url(self):
        self.assertRaises(
            NavbarItemError,
            NavbarItem,
            name='navbar_item_one',
            label='Navbar Item One',
            title='navbar_item_one',
            url_name='blahblahblah')

    def test_navbar_item_ok(self):
        navbar_item = NavbarItem(
            name='navbar_item_one',
            label='Navbar Item One',
            title='navbar_item_one',
            url_name='navbar_one_url')
        self.assertEqual(navbar_item.name, 'navbar_item_one')
        self.assertEqual(navbar_item.title, 'navbar_item_one')
        self.assertEqual(navbar_item.label, 'Navbar Item One')

    def test_render_navbar_item_to_string(self):
        navbar_item_selected = 'navbar_item_one'
        navbar_item = NavbarItem(
            name='navbar_item_one',
            label='Navbar Item One',
            title='navbar_item_one',
            url_name='navbar_one_url')
        template_string = navbar_item.render(
            navbar_item_selected=navbar_item_selected)
        self.assertIn(navbar_item.name, template_string)
        self.assertIn(navbar_item.title, template_string)
        self.assertIn(navbar_item.reversed_url, template_string)
        self.assertIn(navbar_item.label, template_string)

    def test_navbar_repr(self):
        navbar = Navbar(name='default')
        self.assertTrue(repr(navbar))

    def test_render_navbar_item_to_string_fa_icon(self):
        navbar_item_selected = 'navbar_item_one'
        navbar_item = NavbarItem(
            name='navbar_item_one',
            label='Navbar Item One',
            title='navbar_item_one',
            url_name='navbar_one_url',
            fa_icon='far fa-user-circle')
        template_string = navbar_item.render(
            navbar_item_selected=navbar_item_selected)
        self.assertIn(navbar_item.fa_icon, template_string)

    def test_render_navbar_item_to_string_icon(self):
        navbar_item_selected = 'navbar_item_one'
        navbar_item = NavbarItem(
            name='navbar_item_one',
            label='Navbar Item One',
            title='navbar_item_one',
            url_name='navbar_one_url',
            icon='medicine.png')
        template_string = navbar_item.render(
            navbar_item_selected=navbar_item_selected)
        self.assertIn(navbar_item.icon, template_string)
