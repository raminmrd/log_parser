import json
import re
import pandas as pd

class LogParser:
    def __init__(self, debug=False):
        self.debug = debug
        self.skipped_objects = []  # Track skipped objects for debugging
        self.json_objects = []  # Store all found JSON objects
    
    def _find_json_objects(self, text):
        """Find JSON objects in text by tracking opening and closing braces."""
        json_objects = []
        
        # First, try to find all potential JSON objects using regex
        potential_objects = re.finditer(r'\{[^{}]*\}|(\{[^{}]*(\{[^{}]*\}[^{}]*)*\})', text)
        
        for match in potential_objects:
            json_str = match.group(0)
            if self.debug:
                print(f"\nFound potential JSON string at position {match.start()}: {json_str}")
            
            try:
                json_obj = json.loads(json_str)
                if isinstance(json_obj, dict) and 'event' in json_obj:
                    if self.debug:
                        print(f"Valid JSON with event key: {json_obj['event']}")
                    json_objects.append(json_obj)
                else:
                    if self.debug:
                        print(f"Skipping object without 'event' key: {json_str}")
                    self.skipped_objects.append(('no_event_key', json_str))
            except json.JSONDecodeError as e:
                if self.debug:
                    print(f"Invalid JSON: {e}")
                    print(f"Problematic string: {json_str}")
                self.skipped_objects.append(('invalid_json', json_str))
        
        if self.debug:
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
        """Parse a log file and return a pandas DataFrame containing the JSON objects.
        
        Args:
            file_path (str): Path to the log file to parse
            debug (bool): Whether to print debug information
            
        Returns:
            pandas.DataFrame: DataFrame containing the parsed JSON objects
            
        Raises:
            FileNotFoundError: If the log file doesn't exist
            pd.errors.EmptyDataError: If no valid JSON objects were found
            Exception: For other unexpected errors
        """
        self.debug = debug
        if self.debug:
            print(f"\nReading file: {file_path}")
        
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                
            if self.debug:
                print(f"File content length: {len(content)} characters")
                print("\nFile content:")
                print(content)
            
            json_objects = self._find_json_objects(content)
            
            if not json_objects:
                raise pd.errors.EmptyDataError("No valid JSON objects found in the log file")
            
            df = pd.DataFrame(json_objects)
            
            if self.debug:
                print("\nDataFrame shape:", df.shape)
                print("\nDataFrame columns:", df.columns.tolist())
                print("\nDataFrame preview:")
                print(df)
                
                print("\nUnique values in each column:")
                for col in df.columns:
                    print(f"\n{col}:")
                    print(df[col].unique())
            
            return df
            
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            raise
        except pd.errors.EmptyDataError:
            print("Error: No valid JSON objects found in the log file")
            raise
        except Exception as e:
            print(f"Error parsing log file: {str(e)}")
            raise

def main():
    """Example usage of the LogParser class."""
    try:
        parser = LogParser(debug=True)
        df = parser.parse_log_file('complex_test.log')
        print("\nSuccessfully parsed log file!")
        print(f"Found {len(df)} JSON objects with events")
        return df
    except Exception as e:
        print(f"Failed to parse log file: {str(e)}")
        return None

if __name__ == "__main__":
    main() 