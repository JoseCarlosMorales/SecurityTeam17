import random
from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient
from django.db import transaction

from voting.models import Voting, Question, QuestionOption
from mixnet.models import Auth
from django.contrib.auth.models import User
from base import mods
from base.tests import BaseTestCase
from census.models import Census

import os

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class VisualizerTestCase(BaseTestCase):
    
    voter = None
    voting = None
    census = None
    
    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()
        self.census = None
        self.voting = None
        self.voter = None
        
    def create_voting(self):
        return self.create_voting_by_id(1)

    def create_voting_by_id(self, pk):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting {}'.format(pk), question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)
        v.id = 1
        return v
    
    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.id = pk
        user.save()
        return user

    def create_census(self, nameC):
        Census.objects.all().delete()
        self.census = Census(name=nameC)
        self.census.id = 1
        self.census.save()

    def test_enpoint_is_avaliable(self):
        self.create_voting()
        response = self.client.get('/visualizer/all', format='json')
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.json(), {'voters': [self.voter.id]})

    def test_there_is_one_voting(self):
        self.create_voting()
        response = self.client.get('/visualizer/all', format='json')
        n = len(response.json())
        self.assertEqual(n, 1)

    def test_information_is_correct(self):
        self.create_voting()
        voting = self.create_voting()
        response = self.client.get('/visualizer/all', format='json')
        voting_id = voting.id
        voting_name = voting.name
        name_response = response.json()['2']['name']
        self.assertEqual(name_response, voting_name)
        voting_desc = voting.desc
        desc_response = response.json()['2']['description']
        self.assertEqual(desc_response, voting_desc)
        question_desc = str(voting.question).split(':')[0]
        question_desc_response = response.json()['2']['question_desc']
        self.assertEqual(question_desc, question_desc_response)

    def test_users_ok(self):
        pk = 1
        self.get_or_create_user(pk)
        user = self.get_or_create_user(pk)
        response = self.client.get('/visualizer/allUsers', format='json')
        user_id = user.id
        username = user.username
        username_response = response.json()[str(user_id)]['username']
        self.assertEqual(username_response, username)

    def test_census_ok(self):
        cName = "Avila"
        self.create_census(cName)
        response = self.client.get('/visualizer/allCensus', format='json')
        census_response = response.json()["1"]['name']
        self.assertEqual(cName, census_response)
    
    def test_bot_login(self):
        pk = 1
        self.get_or_create_user(pk)
        user = self.get_or_create_user(pk)
        data={"username":"user","password":"querty"}
        response = self.client.post('/authentication/login-bot', data, format='json')
        self.assertEqual(response.status_code, 301)
