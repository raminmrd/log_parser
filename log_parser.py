import json
import pandas as pd
import re

class LogParser:
    def __init__(self):
        self.pattern = r'\{[^{}]*\}'
    
    def _extract_json_objects(self, text):
        """Extract JSON-like objects from text using regex."""
        matches = re.finditer(self.pattern, text)
        json_objects = []
        
        for match in matches:
            try:
                # Try to parse the matched text as JSON
                json_obj = json.loads(match.group())
                if isinstance(json_obj, dict) and 'event' in json_obj:
                    json_objects.append(json_obj)
            except json.JSONDecodeError:
                # Skip invalid JSON objects
                continue
        
        return json_objects
    
    def parse_log_file(self, file_path):
        """Parse a log file and return a pandas DataFrame."""
        with open(file_path, 'r') as file:
            content = file.read()
        
        json_objects = self._extract_json_objects(content)
        return pd.DataFrame(json_objects)

# Example usage
if __name__ == "__main__":
    parser = LogParser()
    df = parser.parse_log_file('test.log')
    print(df) 