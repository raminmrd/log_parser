# Log Parser

A Python utility for parsing log files containing JSON objects with event data. The parser extracts JSON objects from log files and converts them into a pandas DataFrame for easy analysis.

## Features

- Extracts JSON objects from log files, even when embedded in other text
- Handles nested JSON structures
- Validates JSON objects and requires an "event" key
- Converts valid JSON objects into a pandas DataFrame
- Debug mode for detailed parsing information
- Tracks skipped objects and parsing errors

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/log-parser.git
cd log-parser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from log_parser import LogParser

# Create a parser instance
parser = LogParser(debug=False)

# Parse a log file and get a DataFrame
df = parser.parse_log_file('your_log_file.log')

# Work with the DataFrame
print(df.head())
print(df['event'].unique())
```

### Debug Mode

Enable debug mode to see detailed information about the parsing process:

```python
parser = LogParser(debug=True)
df = parser.parse_log_file('your_log_file.log')
```

### Expected Log File Format

The log file can contain any text, but JSON objects should have an "event" key:

```
Some text before the JSON
{"event": "user_login", "timestamp": "2024-03-20", "user_id": 123}
More text here
{"event": "page_view", "page": "/home", "user_id": 123}
```

## Error Handling

The parser handles several types of errors:

- FileNotFoundError: When the log file doesn't exist
- pd.errors.EmptyDataError: When no valid JSON objects are found
- JSONDecodeError: When invalid JSON is encountered (these objects are skipped)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 