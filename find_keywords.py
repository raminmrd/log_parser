from log_parser import LogParser
import re
import json

def search_log_file(file_path, keyword):
    """Search for a keyword in the log file."""
    print(f"\nSearching for '{keyword}' in log file...")
    with open(file_path, 'r') as file:
        content = file.read()
        matches = re.finditer(keyword, content, re.IGNORECASE)
        found = False
        for match in matches:
            found = True
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end]
            print(f"\nFound in log file at position {match.start()}:")
            print(f"...{context}...")
        if not found:
            print("Keyword not found in log file")

def search_dataframe(df, keyword):
    """Search for a keyword in the DataFrame."""
    print(f"\nSearching for '{keyword}' in DataFrame...")
    found = False
    
    # Search in column values
    for col in df.columns:
        if df[col].dtype == 'object':  # Only search in string columns
            matches = df[df[col].astype(str).str.contains(keyword, case=False, na=False)]
            if not matches.empty:
                found = True
                print(f"\nFound in column '{col}':")
                print(matches)
    
    # Search in event names
    if 'event' in df.columns:
        event_matches = df[df['event'].str.contains(keyword, case=False, na=False)]
        if not event_matches.empty:
            found = True
            print("\nFound in event names:")
            print(event_matches)
    
    if not found:
        print("Keyword not found in DataFrame")

def search_raw_json(parser, keyword):
    """Search in the raw JSON strings that were parsed."""
    print(f"\nSearching in raw JSON strings...")
    found = False
    
    # Search in found objects
    for i, obj in enumerate(parser.json_objects):
        json_str = json.dumps(obj)
        if keyword.lower() in json_str.lower():
            found = True
            print(f"\nFound in parsed JSON object {i+1}:")
            print(json.dumps(obj, indent=2))
    
    # Search in skipped objects
    for reason, obj in parser.skipped_objects:
        if keyword.lower() in obj.lower():
            found = True
            print(f"\nFound in skipped object (reason: {reason}):")
            print(obj)
    
    if not found:
        print("Keyword not found in raw JSON strings")

def main():
    # Initialize parser with debug mode
    parser = LogParser(debug=True)
    
    # Parse the log file
    df = parser.parse_log_file('complex_test.log')
    
    # Get keyword from user
    keyword = input("Enter keyword to search for: ")
    
    # Search in all possible locations
    search_log_file('complex_test.log', keyword)
    search_dataframe(df, keyword)
    search_raw_json(parser, keyword)

if __name__ == "__main__":
    main() 