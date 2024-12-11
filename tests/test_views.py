import unittest
from app import create_app
from flask import url_for
from flask_login import FlaskLoginClient

class ViewsTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Запускається один раз перед усіма тестами"""
        cls.app = create_app()  # Ініціалізація Flask-додатку
        cls.client = cls.app.test_client()  # Ініціалізація клієнта для тестування

    def test_registration_page(self):
        """Тест перевірки доступності сторінки реєстрації"""
        response = self.client.get(url_for('users.register'))  # Викликаємо маршрут реєстрації
        self.assertEqual(response.status_code, 200)  # Перевіряємо, що сторінка завантажилася успішно

    def test_login_page(self):
        """Тест перевірки доступності сторінки входу"""
        response = self.client.get(url_for('users.login'))  # Викликаємо маршрут входу
        self.assertEqual(response.status_code, 200)  # Перевіряємо, що сторінка завантажилася успішно

    @classmethod
    def tearDownClass(cls):
        """Запускається після всіх тестів"""
        pass

if __name__ == '__main__':
    unittest.main()
