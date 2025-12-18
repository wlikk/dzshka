import unittest
from converter import main
import tempfile
import os

class TestConverter(unittest.TestCase):
    def test_simple(self):
        test_input = 'name: "test"'
        expected = 'name = "test"\n'
        self._run_test(test_input, expected)
    
    def _run_test(self, input_text, expected_toml):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(input_text)
            input_file = f.name
        
        output_file = 'test_output.toml'
        
        import io
        import sys
        
        sys.stdin = io.StringIO(input_text)
        sys.argv = ['converter.py', '-o', output_file]
        
        try:
            main()
            with open(output_file, 'r') as f:
                result = f.read()
            self.assertEqual(result.strip(), expected_toml.strip())
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
            if os.path.exists(input_file):
                os.remove(input_file)

if __name__ == '__main__':
    unittest.main()
