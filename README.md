# Language Detection API

A fast and accurate language detection API built with FastAPI. This API can identify the language of any text input, providing both the primary detected language and alternative possibilities with confidence scores.

## Features

- 🌐 Detects over 50 languages with high accuracy
- 📊 Provides confidence scores for each detection
- 📋 Lists alternative language possibilities
- 🔍 Returns both language codes and full language names
- 📖 Interactive API documentation with Swagger UI
- 🛠️ Dockerized for easy deployment
- ⚡ Fast and lightweight

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository
```bash
git clone https://github.com/jeanneoo420/language-detection-api.git
cd language-detection-api
```

2. Start the service
```bash
docker-compose up -d
```

3. Access the API at http://localhost:8000
   - Interactive docs at http://localhost:8000/docs

### Manual Setup

1. Clone the repository
```bash
git clone https://github.com/jeanneoo420/language-detection-api.git
cd language-detection-api
```

2. Create and activate a virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Access the API at http://localhost:8000

## API Endpoints

### GET /
Welcome message and basic information

### GET /health
Health check endpoint for monitoring

### POST /detect
Detects the language of provided text

**Request Body:**
```json
{
  "text": "Your text to analyze"
}
```

**Response:**
```json
{
    "detected_language": "English",
    "language_code": "en",
    "confidence": 1.0,
    "all_languages": [
        {
            "language": "English",
            "code": "en",
            "probability": 1.0
        }
    ]
}
```

### GET /supported-languages
Lists all supported languages

## Example Usage

### Python
```python
import requests
import json

url = "http://localhost:8000/detect"
payload = {"text": "Hello, how are you doing today?"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

### cURL
```bash
curl -X 'POST' \
  'http://localhost:8000/detect' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"text": "Hello, how are you doing today?"}'
```

## Supported Languages

The API supports detection of over 50 languages including: English, Spanish, French, German, Chinese, Japanese, Russian, Arabic, and many more. Use the `/supported-languages` endpoint to see the complete list.

## Performance and Limitations

- Requires at least 20-50 characters for reliable detection
- Short texts may have lower confidence scores
- Similar languages (like Norwegian and Danish) may occasionally be confused
- Performs best with clean, natural text (not code, abbreviations, etc.)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.