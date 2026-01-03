# toSpanish

A FastAPI application that adds Spanish translations to ProPresenter song files using Google's Gemini AI.

## Description

toSpanish is a tool designed for churches and worship teams that need to display song lyrics in both English and Spanish. It leverages Google's Gemini AI to translate English song lyrics to Spanish and formats them in a way that can be imported back into ProPresenter with both languages displayed.

The application provides both API endpoints for integration with other systems and batch processing capabilities for handling multiple files at once.

## Features

- Translate individual lines of text from English to Spanish
- Process ProPresenter exported files and add Spanish translations
- Generate importable files that can be used in ProPresenter with both English and Spanish lyrics
- API endpoints for integration with other systems
- Batch processing for handling multiple files

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/toSpanish.git
   cd toSpanish
   ```

2. Set up the environment and install dependencies:
   ```bash
   make setup
   ```

   This will:
   - Create a virtual environment
   - Install all required dependencies
   - Activate the virtual environment

3. Create a `.env` file in the project root with the following content:
   ```
   environment=local
   genai_client_api_key=your_google_gemini_api_key
   allowed_origins=http://localhost:PORT|https://yourdomain2.com
   ```

## Usage

### Running the Application

Start the FastAPI server using one of the following methods:

#### Option 1: Using make command

```bash
make run
```

This will activate the virtual environment and start the server on port 8000.

#### Option 2: Using uvicorn directly

```bash
uvicorn app.server:app --reload --port 9000
```

The API will be available at http://localhost:8000 (with make run) or http://localhost:9000 (with direct uvicorn command)

### API Endpoints

#### 1. Translate a Single Text

```
POST /propresenter/include_spanish
```

Request body:
```json
{
  "text": "Your English song lyrics here"
}
```

Response:
```json
{
  "text_data": "Formatted text with translations",
  "json_data": {
    "songs": [
      {
        "title": "Song Title",
        "verses": [
          {
            "lines": [
              {
                "english": "English line",
                "spanish": "Spanish translation"
              }
            ],
            "type": "VERSE"
          }
        ]
      }
    ]
  }
}
```

#### 2. Upload ProPresenter Files

```
POST /propresenter/upload_exported_files
```

Upload ProPresenter exported files as form data.

Response:
```json
{
  "file_id": "unique-file-id"
}
```

#### 3. Download Processed File

```
GET /propresenter/download_importable_file/{file_id}
```

Downloads the processed file with Spanish translations that can be imported into ProPresenter.

### Batch Processing

The application also supports batch processing of files. Place your ProPresenter exported files in the `app/data/unprocessed` directory and use the `process_files` function in the service module to process them.

## Project Structure

- `app/`: Main application directory
  - `server.py`: FastAPI application setup
  - `router.py`: API endpoints
  - `service.py`: Business logic for translation and file processing
  - `schema.py`: Pydantic models for data validation
  - `settings.py`: Application settings
  - `data/`: Directory for storing files
    - `unprocessed/`: Directory for files to be processed
    - `processed/`: Directory for processed files

## Dependencies

- FastAPI: Web framework for building APIs
- Google Genai: Google's Generative AI client library
- Pydantic: Data validation and settings management
- Uvicorn: ASGI server for running the FastAPI application

## Configuration

The application is configured using environment variables or a `.env` file. The following settings are available:

- `environment`: The environment (local, production, etc.)
- `genai_client_api_key`: Google Gemini API key
- `port`: The port to run the server on (default: 9000)
- `allowed_origins`: CORS allowed origins (pipe-separated list)

## Testing

The project includes a comprehensive test suite using pytest. Tests are organized in the `tests` directory.

### Running Tests

You can run tests using one of the following methods:

#### Using the test script:

```bash
# Run all tests with coverage report
./scripts/run_tests.sh
```

#### Using make commands:

```bash
# Run all tests
make test

# Run tests with verbose output
make test-verbose

# Run tests with coverage report
make test-coverage

# Run tests with detailed coverage report
make test-with-coverage
```

#### Using pytest directly:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Generate a coverage report
pytest --cov=app
```

For more information about the tests, see the [tests/README.md](tests/README.md) file.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
