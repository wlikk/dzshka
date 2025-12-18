import unittest
import tempfile
import os
from converter import parse_config, parse_struct
import toml


class TestConverter(unittest.TestCase):

    def test_parse_simple(self):
        text = 'name: "John"'
        result = parse_config(text)
        self.assertEqual(result['name'], 'John')

    def test_parse_struct(self):
        text = '''config: struct {
    host = "localhost",
    port = 8080
}'''
        result = parse_config(text)
        self.assertIn('config', result)
        self.assertEqual(result['config']['host'], 'localhost')
        # Теперь ожидаем число, не строку
        self.assertEqual(result['config']['port'], 8080)

    def test_comments(self):
        text = '''*> Комментарий
name: "test"
*> Еще комментарий'''
        result = parse_config(text)
        self.assertEqual(result['name'], 'test')

    def test_numbers(self):
        text = 'port: 8080'
        result = parse_config(text)
        self.assertEqual(result['port'], 8080)

    def test_negative_numbers(self):
        text = 'temperature: -10'
        result = parse_config(text)
        self.assertEqual(result['temperature'], -10)

    def test_boolean(self):
        text = '''settings: struct {
    enabled = true,
    active = false
}'''
        result = parse_config(text)
        self.assertEqual(result['settings']['enabled'], True)
        self.assertEqual(result['settings']['active'], False)


if __name__ == '__main__':
    unittest.main()