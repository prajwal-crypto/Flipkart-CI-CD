import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret'
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_get_all_products(client):
    """Test products API returns all products"""
    response = client.get('/api/products')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0

def test_filter_by_category(client):
    """Test category filtering works"""
    response = client.get('/api/products?category=mobiles')
    assert response.status_code == 200
    data = response.get_json()
    for product in data:
        assert product['category'] == 'mobiles'

def test_search_products(client):
    """Test search functionality"""
    response = client.get('/api/products?search=samsung')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0

def test_add_to_cart(client):
    """Test adding item to cart"""
    product = {"id": 1, "name": "Test Phone", "price": 10000, "image": "📱"}
    response = client.post('/api/cart',
        json=product,
        content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True

def test_get_cart(client):
    """Test getting cart items"""
    response = client.get('/api/cart')
    assert response.status_code == 200

def test_remove_from_cart(client):
    """Test removing item from cart"""
    # Add first
    client.post('/api/cart', json={"id": 99, "name": "Test", "price": 100, "image": "📦"}, content_type='application/json')
    # Remove
    response = client.delete('/api/cart', json={"id": 99}, content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
