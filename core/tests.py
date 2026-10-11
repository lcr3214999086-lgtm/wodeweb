from django.test import Client, TestCase
from .models import Inquiry
from .forms import REQUEST_TYPES, BUDGETS
from .models import Product
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import site


class ProductManagementTests(TestCase):
    def test_public_catalog_and_admin_publication(self):
        Product.objects.all().delete()
        hidden = Product.objects.create(name='Draft', category='Storage', description='Draft')
        published = Product.objects.create(name='Live', category='Storage', description='Original', is_published=True, sort_order=2)
        self.assertEqual([x['id'] for x in self.client.get('/api/products/').json()['products']], [published.pk])
        user = get_user_model().objects.create_superuser('testadmin', password='test-only')
        self.client.force_login(user)
        response = self.client.post('/admin/core/product/', {'action': 'publish', '_selected_action': [hidden.pk]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual([x['id'] for x in self.client.get('/api/products/').json()['products']], [hidden.pk, published.pk])
        self.client.post('/admin/core/product/', {'action': 'unpublish', '_selected_action': [published.pk]})
        published.refresh_from_db()
        self.assertFalse(published.is_published)
        hidden.refresh_from_db()
        hidden.description = 'Updated'
        hidden.save()
        self.assertEqual(self.client.get('/api/products/').json()['products'][0]['desc'], 'Updated')
        self.client.logout()
        self.assertEqual(self.client.post('/api/products/', {}).status_code, 405)
        self.assertEqual(self.client.get('/admin/core/product/').status_code, 302)


class InquirySubmissionTests(TestCase):
    def test_submission_validation_and_csrf(self):
        client = Client(enforce_csrf_checks=True)
        data = dict(contact='Test', phone='13800138000', company='Example',
                    request_type=REQUEST_TYPES[0], quantity=2, city='Shanghai',
                    budget=BUDGETS[-1], description='Storage project')
        self.assertEqual(client.post('/api/inquiries/', data, content_type='application/json').status_code, 403)
        self.assertEqual(client.get('/api/inquiries/').status_code, 200)
        token = client.cookies['csrftoken'].value
        response = client.post('/api/inquiries/', data, content_type='application/json', HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Inquiry.objects.get().company, 'Example')
        data['quantity'] = 0
        self.assertEqual(client.post('/api/inquiries/', data, content_type='application/json', HTTP_X_CSRFTOKEN=token).status_code, 400)
        self.assertEqual(Inquiry.objects.count(), 1)

    def test_invalid_requests_do_not_create_records(self):
        client = Client(enforce_csrf_checks=True)
        response = client.get('/api/inquiries/')
        token = response.json()['csrf_token']
        self.assertEqual(client.post('/api/inquiries/', {}, HTTP_X_CSRFTOKEN=token).status_code, 415)
        for payload in ['invalid', '[]', '{}']:
            response = client.post('/api/inquiries/', payload, content_type='application/json', HTTP_X_CSRFTOKEN=token)
            self.assertEqual(response.status_code, 400)
        self.assertFalse(Inquiry.objects.exists())
