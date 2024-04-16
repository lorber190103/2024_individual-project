from flask import render_template

from app import app


def test_home_route():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        expected_text = render_template('home.html')
        assert expected_text.encode() in response.data


def test_deal_route():
    with app.test_client() as client:
        response = client.get('/Deals')
        assert response.status_code == 200


def test_store_route():
    with app.test_client() as client:
        response = client.get('/Stores')
        assert response.status_code == 200


def test_search_route():
    with app.test_client() as client:
        response = client.get('/Search')
        assert response.status_code == 200
