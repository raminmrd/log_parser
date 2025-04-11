# Log Parser

A Python tool for parsing JSON-like log files into pandas DataFrames. The parser can handle complex JSON structures, nested objects, and various edge cases.

## Features

- Parses JSON objects from log files
- Handles nested JSON structures
- Supports special characters and Unicode
- Skips invalid JSON entries
- Requires 'event' key in JSON objects
- Converts results to pandas DataFrame

## Installation

1. Clone the repository:
```bash
git clone https://github.com/raminmrd/log_parser.git
cd log_parser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```python
from log_parser import LogParser

# Create a parser instance
parser = LogParser(debug=True)  # Set debug=True to see detailed parsing information

# Parse a log file
df = parser.parse_log_file('your_log_file.log')

# Work with the DataFrame
print(df)  # View all data
print(df['event'].unique())  # See all unique event types
print(df[df['event'] == 'login'])  # Filter by event type
```

## Example Log File Format

The parser expects JSON objects in the log file, each containing an 'event' key:

```text
{"event": "login", "user": "test1", "timestamp": "2024-03-20"}
{"event": "nested", "data": {"inner": {"value": 42}}}
{"event": "array", "items": [1, 2, 3]}
```

## Testing

Run the test suite:
```bash
python -m unittest test_log_parser.py -v
```

## Notes

- Each JSON object must have an 'event' key
- Invalid JSON entries are skipped
- Objects without 'event' key are skipped
- Supports nested JSON structures
- Handles special characters and Unicode
- Works with large numbers and scientific notation 