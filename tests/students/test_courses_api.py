from random import randint

import pytest
import os
from rest_framework.test import APIClient
from tests.fixtures.fixture_data import *
from django.conf import settings


client = APIClient()
class TestCourses:
    @pytest.mark.django_db(transaction=True)
    def test_courses_urls(self, course):
        response = client.get(f'/api/v1/courses/{course.id}/')

        assert response.status_code == 200
        assert response.data['id'] == course.id

    @pytest.mark.django_db(transaction=True)
    def test_list_courses(self, courses):
        response = client.get(f'/api/v1/courses/')  # Правильно надо указывать путь

        assert response.status_code == 200
        assert len(response.data) == len(courses)  # Проверка списка

    @pytest.mark.django_db(transaction=True)
    def test_courses_list_filters_id(self, courses):
        random_id = [c.id for c in courses][randint(0, 10)]
        response = client.get(f'/api/v1/courses/?id={random_id}')

        assert response.status_code == 200
        assert response.data[0]['id'] == random_id


    @pytest.mark.django_db(transaction=True)
    def test_courses_list_filters_name(self, courses):
        random_name = [c.name for c in courses][randint(0, 10)]
        response = client.get(f'/api/v1/courses/?name={random_name}')

        assert response.status_code == 200
        assert response.data[0]['name'] == random_name


    @pytest.mark.django_db(transaction=True)
    def test_course_create_update_delete(self):
        fixture_path = os.path.join(settings.BASE_DIR, 'tests', 'fixtures', 'courses.json')

        with open(fixture_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        create_response = client.post('/api/v1/courses/', data=data[0])

        course_id = create_response.data['id']
        assert create_response.status_code == 201

        update_response = client.put(f'/api/v1/courses/{course_id}/', data=data[1])
        assert update_response.status_code == 200

        retrieve_response = client.get(f'/api/v1/courses/{course_id}/')
        assert retrieve_response.status_code == 200

        assert retrieve_response.data['name'] == data[1]['name']

        delete_response = client.delete(f'/api/v1/courses/{course_id}/')
        assert delete_response.status_code == 204





