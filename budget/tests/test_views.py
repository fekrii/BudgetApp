from http import client
from unicodedata import category, name
from urllib import response
from bleach import clean
from django.test import TestCase, Client
from django.urls import reverse
import budget
from budget.models import Project, Category, Expense
import json 



class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project1'])
        
        # becauese we are using the slug in this url we will create 
        # new project with a known slug to use it in test function
        self.project1 = Project.objects.create(
            name = 'project1',
            budget = 1000
        )


    
    def test_project_list_view(self):
        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')
    

    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')
    

    def test_project_detail_POST(self):
        Category.objects.create(
            project=self.project1,
            name = "development"
        )

        response = self.client.post(self.detail_url, {
            'title': 'expense1',
            'amount': 1000,
            'category': 'development'
        })

        # status_code 302 is for redirect status in views
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.project1.expenses.first().title, 'expense1')

    # test if POST have no data to make sure that no expanses added 
    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)

        # status_code 302 is for redirect status in views
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.project1.expenses.count(), 0)
    
    def test_project_detail_DELETE(self):
        category1 = Category.objects.create(
            project=self.project1,
            name = "development"
        )

        Expense.objects.create(
            project = self.project1,
            title = "expese1",
            amount = 1000,
            category = category1
        )

        response = self.client.delete(self.detail_url, json.dumps({
            'id':1
        }))

        self.assertEquals(response.status_code, 204)
        self.assertEquals(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE_no_id(self):
        category1 = Category.objects.create(
            project=self.project1,
            name = "development"
        )

        Expense.objects.create(
            project = self.project1,
            title = "expese1",
            amount = 1000,
            category = category1
        )

        response = self.client.delete(self.detail_url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(self.project1.expenses.count(), 1)

    
    def test_project_create_POST(self):
        url = reverse('add')
        response = self.client.post(url, {
            'name': 'project2',
            'budget':2000,
            'categoriesString': 'design,development'
        })

        # check if project created
        project2 = Project.objects.get(id=2)
        self.assertEquals(project2.name, 'project2')

        # check if category 1 created
        first_category = Category.objects.get(id=1)
        self.assertEquals(first_category.project, project2)
        self.assertEquals(first_category.name, 'design')

        # check if category 2 created
        second_category = Category.objects.get(id=2)
        self.assertEquals(second_category.project, project2)
        self.assertEquals(second_category.name, 'development')
