import unittest
import pandas as pd
from log_parser import LogParser
import os

class TestLogParser(unittest.TestCase):
    def setUp(self):
        self.parser = LogParser()
        self.test_file = 'test_cases.log'
    
    def tearDown(self):
        # Clean up test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def create_test_file(self, content):
        with open(self.test_file, 'w') as f:
            f.write(content)
    
    def test_basic_json_parsing(self):
        """Test basic JSON parsing with valid entries"""
        content = """
        {"event": "login", "user": "test1", "timestamp": "2024-03-20"}
        {"event": "logout", "user": "test1", "timestamp": "2024-03-21"}
        """
        self.create_test_file(content)
        df = self.parser.parse_log_file(self.test_file)
        
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['event'], 'login')
        self.assertEqual(df.iloc[1]['event'], 'logout')
    
    def test_nested_json(self):
        """Test parsing of nested JSON structures"""
        content = """
        {"event": "nested", "data": {"inner": {"value": 42}}}
        {"event": "complex", "metadata": {"user": {"id": 123, "name": "test"}}}
        """
        self.create_test_file(content)
        df = self.parser.parse_log_file(self.test_file)
        
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['data']['inner']['value'], 42)
        self.assertEqual(df.iloc[1]['metadata']['user']['id'], 123)
    
    def test_missing_event_key(self):
        """Test handling of JSON objects without event key"""
        content = """
        {"user": "test1", "timestamp": "2024-03-20"}
        {"event": "valid", "user": "test2"}
        """
        self.create_test_file(content)
        df = self.parser.parse_log_file(self.test_file)
        
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['event'], 'valid')
    
    def test_invalid_json(self):
        """Test handling of invalid JSON entries"""
        content = """
        {invalid json}
        {"event": "valid", "user": "test1"}
        {missing closing brace
        """
        self.create_test_file(content)
        df = self.parser.parse_log_file(self.test_file)
        
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['event'], 'valid')
    
    def test_empty_file(self):
        """Test handling of empty log file"""
        self.create_test_file("")
        df = self.parser.parse_log_file(self.test_file)
        
        self.assertTrue(df.empty)
    
    def test_mixed_content(self):
        """Test handling of mixed content with valid and invalid entries"""
        content = """
        Some random text
        {"event": "valid1", "data": 123}
        More random text
        {"event": "valid2", "data": 456}
        {invalid json}
        """
        self.create_test_file(content)
        df = self.parser.parse_log_file(self.test_file)
        
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['data'], 123)
        self.assertEqual(df.iloc[1]['data'], 456)
    
    def test_special_characters(self):
        """Test handling of special characters in JSON"""
        content = """
        {"event": "special", "text": "line\\nbreak", "unicode": "你好"}
        {"event": "quotes", "text": "He said \\"Hello\\""}
        """
        self.create_test_file(content)
        df = self.parser.parse_log_file(self.test_file)
        
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['text'], "line\nbreak")
        self.assertEqual(df.iloc[0]['unicode'], "你好")
        self.assertEqual(df.iloc[1]['text'], 'He said "Hello"')
    
    def test_large_numbers(self):
        """Test handling of large numbers and scientific notation"""
        content = """
        {"event": "numbers", "large": 12345678901234567890, "scientific": 1.23e10}
        """
        self.create_test_file(content)
        df = self.parser.parse_log_file(self.test_file)
        
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['large'], 12345678901234567890)
        self.assertEqual(df.iloc[0]['scientific'], 1.23e10)

if __name__ == '__main__':
    unittest.main() 