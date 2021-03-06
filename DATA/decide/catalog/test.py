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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import os
import time
import json


class VisualizerTestCase(BaseTestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.vars = {}
        super().setUp()
        
    def tearDown(self):
        self.driver.quit()
        super().tearDown()
    
    def test_get_home_ok(self):
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Vota en Decide"
    
    def test_change_language(self):
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        el = self.driver.find_element(By.NAME, "language")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'English (en)':
                option.click()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(4)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == 'Voting in Decide'

    def test_change_language_es(self):
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        el = self.driver.find_element(By.NAME, "language")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'spanish (es)':
                option.click()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(4)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == 'Vota en Decide'
    
    def test_link_user_guide(self):
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        self.driver.find_element(By.LINK_TEXT, "User guide").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Manual de uso de nuevas funcionalidades"
    
    def test_voting(self):
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".listavotings")
        assert len(elements) > 0
    
    def test_link_voting(self):
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        self.driver.find_element(By.LINK_TEXT, "Esta va").click()
        url = self.driver.current_url
        assert url == "https://decide-full-alcazaba-visualize.herokuapp.com/visualizer/5/"
    
    def test_redirectAdmin(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".imagen-port:nth-child(1) > .hover-galeria")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.LINK_TEXT, "admin/")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "admin/").click()
        self.driver.find_element(By.ID, "content").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("buenas1234")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        assert self.driver.find_element(By.LINK_TEXT, "Administraci??n de Django").text == "Administraci??n de Django"
        assert self.driver.find_element(By.CSS_SELECTOR, "strong").text == "ADMIN"
    
    def test_incorrectAdmin(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/admin/login/?next=/admin/")
        self.driver.set_window_size(909, 1016)
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("incorrecto")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".errornote")
        assert len(elements) > 0
    
    def test_redirectAPI(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".imagen-port:nth-child(2) > .hover-galeria")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.LINK_TEXT, "doc/")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "doc/").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".title").text == "Decide API"

    def test_redirectPostproc(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".imagen-port:nth-child(9) > .hover-galeria")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.LINK_TEXT, "postproc/")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "postproc/").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Post Proc"
    
    def test_redirectBase(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".imagen-port:nth-child(5) > .hover-galeria")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.LINK_TEXT, "base/")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "base/").click()
        self.driver.find_element(By.ID, "content").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("buenas1234")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".section").text == "BASE"
    
    def test_okFooter(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        elements = self.driver.find_elements(By.CSS_SELECTOR, "footer")
        assert len(elements) > 0

    def test_view_url_guia_error(self):
        resp = self.client.get('/guiaUsuario')
        self.assertEqual(resp.status_code, 404)
     
    def test_guia_ok(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/guia/")
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Manual de uso de nuevas funcionalidades"
    
    def test_guiaInicio(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/guia/")
        self.driver.find_element(By.LINK_TEXT, "Inicio").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".galeria-port")
        assert len(elements) > 0
    
    def test_guiaAdmin(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/guia/")
        self.driver.find_element(By.LINK_TEXT, "Admin").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("buenas1234")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        assert self.driver.find_element(By.LINK_TEXT, "Administraci??n de Django").text == "Administraci??n de Django"
        assert self.driver.find_element(By.CSS_SELECTOR, "strong").text == "ADMIN"
    
    def test_access_visualizer_200(self):
        self.driver = webdriver.Chrome()
        response = self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/visualizer/5")
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votaci??n no comenzada"

    def test_darkmode(self):
        self.driver = webdriver.Chrome()
        response = self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/visualizer/5")
        self.driver.find_element(By.CSS_SELECTOR, "span:nth-child(1)").click()
        '''
        assert self.driver.find_element(By.CSS_SELECTOR, ".text-muted > th:nth-child(1)").text == "Opci??n"
        assert self.driver.find_element(By.CSS_SELECTOR, "th:nth-child(2)").text == "Puntuaci??n"
        assert self.driver.find_element(By.CSS_SELECTOR, "th:nth-child(3)").text == "Votos"
        '''
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votaci??n no comenzada"
    
    def test_lightmode(self):
        self.driver = webdriver.Chrome()
        response = self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/visualizer/5")
        self.driver.find_element(By.CSS_SELECTOR, "span:nth-child(1)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votaci??n no comenzada"
        self.driver.find_element(By.CSS_SELECTOR, "span:nth-child(2)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votaci??n no comenzada"
    
    def test_showgraphics(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.LINK_TEXT, "Color de pelo").click()
        element = self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas").click()
        url = self.driver.current_url
        assert url == "http://localhost:8000/visualizer/3/graficos"
    
    def test_showgraphics_title_ok(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.LINK_TEXT, "Color de pelo").click()
        element = self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "GR??FICOS DE LA VOTACI??N"

    def test_showgraphics_button_ok(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.LINK_TEXT, "Color de pelo").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "Ver Gr??ficas")
        assert len(elements) > 0
    
    def test_showgraphics_allgraphics_ok(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.LINK_TEXT, "Color de pelo").click()
        element = self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-lg-12")
        assert len(elements) > 0
    
    def test_showgraphics_footer_ok(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.LINK_TEXT, "Color de pelo").click()
        element = self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas").click()
        element = self.driver.find_elements(By.CSS_SELECTOR, ".footer-content")
        assert len(element) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "h3").text == "Decide"

    def test_showgraphics_pagetitle_ok(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.LINK_TEXT, "Color de pelo").click()
        element = self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "Ver Gr??ficas").click()
        assert self.driver.title == "Decide!"

    def test_census(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".imagen-port:nth-child(7) > .hover-galeria")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "census/").click()
        self.driver.find_element(By.ID, "content").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("buenas1234")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "#content > h1").text == "Administraci??n de Census"

    def test_auth(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".imagen-port:nth-child(4) > .hover-galeria")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "authentication/").click()
        self.driver.find_element(By.ID, "content").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("buenas1234")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "#content > h1").text == "Administraci??n de Autenticaci??n y autorizaci??n"

    def test_mixnet(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".imagen-port:nth-child(8) > .hover-galeria")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "mixnet/").click()
        self.driver.find_element(By.ID, "content").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("buenas1234")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "#content > h1").text == "Administraci??n de Mixnet"
    
    def test_store(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://decide-full-alcazaba-visualize.herokuapp.com/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".imagen-port:nth-child(10) > .hover-galeria")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "store/").click()
        self.driver.find_element(By.ID, "content").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("buenas1234")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "#content > h1").text == "Administraci??n de Store"

    def test_pdf(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.LINK_TEXT, "Color de las mesas").click()
        element = self.driver.find_element(By.LINK_TEXT, "Exportar en PDF")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "Exportar en PDF").click()
        url = self.driver.current_url
        assert url == "http://localhost:8000/visualizer/1/pdf"

    def test_pdf_title(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.LINK_TEXT, "Color de las mesas").click()
        element = self.driver.find_element(By.LINK_TEXT, "Exportar en PDF")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "Exportar en PDF").click()
        title = self.driver.title
        assert self.driver.title == "Decide!"