import json
import pandas as pd
import re

class LogParser:
    def __init__(self):
        pass
    
    def _find_json_objects(self, text):
        """Find JSON objects in text by tracking opening and closing braces."""
        json_objects = []
        stack = []
        start = -1
        
        for i, char in enumerate(text):
            if char == '{':
                if not stack:
                    start = i
                stack.append(char)
            elif char == '}':
                if stack:
                    stack.pop()
                    if not stack:  # We've found a complete JSON object
                        try:
                            json_str = text[start:i+1]
                            json_obj = json.loads(json_str)
                            if isinstance(json_obj, dict) and 'event' in json_obj:
                                json_objects.append(json_obj)
                        except json.JSONDecodeError:
                            continue
        
        return json_objects
    
    def parse_log_file(self, file_path):
        """Parse a log file and return a pandas DataFrame."""
        with open(file_path, 'r') as file:
            content = file.read()
        
        json_objects = self._find_json_objects(content)
        return pd.DataFrame(json_objects)

# Example usage
if __name__ == "__main__":
    parser = LogParser()
    df = parser.parse_log_file('test.log')
    print(df) 