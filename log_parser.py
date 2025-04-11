import json
import re

class LogParser:
    def __init__(self, debug=False):
        self.debug = debug
        self.skipped_objects = []  # Track skipped objects for debugging
        self.json_objects = []  # Store all found JSON objects
    
    def _has_event_key(self, obj):
        """Check if the object or any of its nested dictionaries has an 'event' key."""
        if isinstance(obj, dict):
            if 'event' in obj:
                return True
            # Recursively check nested dictionaries
            for value in obj.values():
                if self._has_event_key(value):
                    return True
        return False
    
    def _extract_event(self, obj):
        """Extract the event value from the object or its nested dictionaries."""
        if isinstance(obj, dict):
            if 'event' in obj:
                return obj['event']
            # Recursively search nested dictionaries
            for value in obj.values():
                event = self._extract_event(value)
                if event is not None:
                    return event
        return None
    
    def _find_json_objects(self, text):
        """Find JSON objects in text by tracking opening and closing braces."""
        json_objects = []
        pos = 0
        text_length = len(text)
        
        while pos < text_length:
            # Find the start of a potential JSON object
            start = text.find('{', pos)
            if start == -1:
                break
                
            # Track nested braces
            brace_count = 1
            pos = start + 1
            
            while pos < text_length and brace_count > 0:
                if text[pos] == '{':
                    brace_count += 1
                elif text[pos] == '}':
                    brace_count -= 1
                pos += 1
            
            if brace_count == 0:
                # We found a complete JSON object
                json_str = text[start:pos]
                print(f"\nFound potential JSON string at position {start}: {json_str}")
                
                try:
                    json_obj = json.loads(json_str)
                    if isinstance(json_obj, dict) and self._has_event_key(json_obj):
                        event_value = self._extract_event(json_obj)
                        print(f"Valid JSON with event key: {event_value}")
                        json_objects.append(json_obj)
                    else:
                        print(f"Skipping object without 'event' key: {json_str}")
                        self.skipped_objects.append(('no_event_key', json_str))
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON: {e}")
                    print(f"Problematic string: {json_str}")
                    self.skipped_objects.append(('invalid_json', json_str))
            else:
                # Unmatched braces, move to next character
                pos = start + 1
        
        print(f"\nTotal JSON objects found: {len(json_objects)}")
        print("\nFound objects:")
        for i, obj in enumerate(json_objects):
            print(f"\nObject {i+1}:")
            print(json.dumps(obj, indent=2))
        
        if self.skipped_objects:
            print("\nSkipped objects:")
            for reason, obj in self.skipped_objects:
                print(f"\nReason: {reason}")
                print(f"Object: {obj}")
        
        self.json_objects = json_objects  # Store for later use
        return json_objects
    
    def parse_log_file(self, file_path, debug=False):
        """Parse a log file and return a list of JSON objects."""
        self.debug = debug
        print(f"\nReading file: {file_path}")
        
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                
            print(f"File content length: {len(content)} characters")
            print("\nFile content:")
            print(content)
            
            return self._find_json_objects(content)
            
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            raise
        except Exception as e:
            print(f"Error parsing log file: {str(e)}")
            raise

def main():
    """Example usage of the LogParser class."""
    try:
        parser = LogParser(debug=True)
        json_objects = parser.parse_log_file('complex_test.log')
        print("\nSuccessfully parsed log file!")
        print(f"Found {len(json_objects)} JSON objects with events")
        return json_objects
    except Exception as e:
        print(f"Failed to parse log file: {str(e)}")
        return None

if __name__ == "__main__":
    main() 