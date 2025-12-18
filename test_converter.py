import unittest
import subprocess
import tempfile
import os

class TestConverter(unittest.TestCase):
    def test_simple(self):
        # Создаем временный файл с тестовыми данными
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
            f.write('name: "test"')
            input_file = f.name
        
        output_file = 'test_output.toml'
        
        try:
            # Запускаем конвертер
            with open(input_file, 'r') as infile:
                result = subprocess.run(
                    ['python', 'converter.py', '-o', output_file],
                    stdin=infile,
                    capture_output=True,
                    text=True
                )
            
            self.assertEqual(result.returncode, 0)
            
            # Проверяем что файл создан
            self.assertTrue(os.path.exists(output_file))
            
            # Читаем результат
            with open(output_file, 'r') as f:
                content = f.read()
                self.assertIn('name = "test"', content)
                
        finally:
            # Удаляем временные файлы
            if os.path.exists(input_file):
                os.remove(input_file)
            if os.path.exists(output_file):
                os.remove(output_file)
    
    def test_struct(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
            f.write('''config: struct {
    host = "localhost",
    port = 8080
}''')
            input_file = f.name
        
        output_file = 'test_output.toml'
        
        try:
            with open(input_file, 'r') as infile:
                result = subprocess.run(
                    ['python', 'converter.py', '-o', output_file],
                    stdin=infile,
                    capture_output=True,
                    text=True
                )
            
            self.assertEqual(result.returncode, 0)
            self.assertTrue(os.path.exists(output_file))
            
            with open(output_file, 'r') as f:
                content = f.read()
                self.assertIn('[config]', content)
                self.assertIn('host = "localhost"', content)
                
        finally:
            if os.path.exists(input_file):
                os.remove(input_file)
            if os.path.exists(output_file):
                os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
