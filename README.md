# HNG Stage 1 Backend Task - String Analysis API

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-Latest-red.svg)](https://sqlmodel.tiangolo.com/)

A RESTful API built with FastAPI that stores and analyzes string properties with advanced filtering capabilities. This project features natural language query parsing, PostgreSQL database integration, and comprehensive string analysis. Part of the HNG Internship Stage 1 Backend task.

## 🚀 Live Demo

**API Base URL:** [https://hng-1-production-9be2.up.railway.app/](https://hng-1-production-9be2.up.railway.app/)

**Interactive API Documentation (Swagger UI):** [https://hng-1-production-9be2.up.railway.app/docs](https://hng-1-production-9be2.up.railway.app/docs)

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Natural Language Queries](#natural-language-queries)
- [Deployment](#deployment)
- [Error Handling](#error-handling)
- [Testing](#testing)
  

## ✨ Features

- **String Analysis**: Automatically computes string properties (length, palindrome check, unique characters, word count, SHA256 hash, character frequency)
- **PostgreSQL Database**: Persistent storage with SQLModel ORM
- **Advanced Filtering**: Filter strings by multiple criteria (palindrome status, length range, word count, character presence)
- **Natural Language Queries**: Parse human-readable queries like "palindromic strings longer than 10 characters"
- **SHA256 Hashing**: Unique identifier generation for each string
- **Character Frequency Analysis**: Detailed character occurrence mapping
- **CRUD Operations**: Full Create, Read, Update, Delete functionality
- **Async Support**: Asynchronous database operations for optimal performance
- **Auto-Documentation**: Interactive Swagger UI and ReDoc
- **Production Ready**: Deployed on Railway with PostgreSQL

## 📁 Project Structure

```
hng_1/
│
├── src/
│   ├── strings/
│   │   ├── __init__.py          # Package initialization
│   │   ├── models.py            # SQLModel database models
│   │   ├── schemas.py           # Pydantic schemas for validation
│   │   ├── services.py          # Business logic and string analysis
│   │   └── routes.py            # API route definitions
│   │
│   └── db/
│       └── main.py              # Database connection and session management
│
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## 🛠️ Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern, fast web framework for building APIs
- **[Python 3.8+](https://www.python.org/)**: Programming language
- **[SQLModel](https://sqlmodel.tiangolo.com/)**: SQL databases with Python types
- **[PostgreSQL](https://www.postgresql.org/)**: Relational database
- **[Uvicorn](https://www.uvicorn.org/)**: ASGI server for running FastAPI applications
- **[Pydantic](https://docs.pydantic.dev/)**: Data validation using Python type hints
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: Database toolkit
- **[Railway](https://railway.app/)**: Deployment platform

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL database
- Git

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/hng_1.git
cd hng_1
```

2. **Create a virtual environment** (recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/strings_db
```

## 🚀 Running Locally

### Method 1: Using Uvicorn (Recommended)

```bash
uvicorn src.main:app --reload
```

The API will be available at:
- **Base URL**: http://127.0.0.1:8000
- **Swagger Docs**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Method 2: Custom host and port

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8080
```

## 📖 API Documentation

### 1. Add String

**POST** `/`

Adds a new string to the database and returns its computed properties.

#### Request Body

```json
{
  "value": "hello world"
}
```

#### Response (201 Created)

```json
{
  "id": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
  "value": "hello world",
  "properties": {
    "length": 11,
    "is_palindrome": false,
    "unique_characters": 8,
    "word_count": 2,
    "sha256_hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
    "character_frequency_map": {
      "h": 1,
      "e": 1,
      "l": 3,
      "o": 2,
      " ": 1,
      "w": 1,
      "r": 1,
      "d": 1
    }
  },
  "created_at": "2025-10-22T12:34:56.789Z"
}
```

### 2. Get All Strings

**GET** `/`

Retrieves all strings with optional filtering.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `is_palindrome` | boolean | Filter by palindrome status |
| `min_length` | integer | Minimum string length |
| `max_length` | integer | Maximum string length |
| `word_count` | integer | Exact word count |
| `contains_character` | string | Filter strings containing this character |

#### Example Request

```bash
GET /?is_palindrome=true&min_length=5&max_length=20
```

#### Response (200 OK)

```json
{
  "data": [
    {
      "id": "abc123...",
      "value": "racecar",
      "properties": {
        "length": 7,
        "is_palindrome": true,
        "unique_characters": 4,
        "word_count": 1,
        "sha256_hash": "abc123...",
        "character_frequency_map": {
          "r": 2,
          "a": 2,
          "c": 2,
          "e": 1
        }
      },
      "created_at": "2025-10-22T12:00:00.000Z"
    }
  ],
  "count": 1,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5,
    "max_length": 20
  }
}
```

### 3. Filter by Natural Language

**GET** `/filter-by-natural-language`

Parse and execute natural language queries.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Natural language query |

#### Supported Query Patterns

- **Palindromes**: "palindromic strings", "palindrome"
- **Length**: "longer than 10", "shorter than 5", "at least 8", "at most 15", "exactly 12 characters"
- **Word Count**: "single word", "two words", "exactly 3 words"
- **Character**: "containing the letter a", "contains x", "first vowel"

#### Example Request

```bash
GET /filter-by-natural-language?query=palindromic strings longer than 5 characters
```

#### Response (200 OK)

```json
{
  "data": [
    {
      "id": "xyz789...",
      "value": "madam",
      "properties": {
        "length": 5,
        "is_palindrome": true,
        "unique_characters": 3,
        "word_count": 1,
        "sha256_hash": "xyz789...",
        "character_frequency_map": {
          "m": 2,
          "a": 2,
          "d": 1
        }
      },
      "created_at": "2025-10-22T11:00:00.000Z"
    }
  ],
  "count": 1,
  "interpreted_query": {
    "original": "palindromic strings longer than 5 characters",
    "parsed_filters": {
      "is_palindrome": true,
      "min_length": 6
    }
  }
}
```

### 4. Get Single String

**GET** `/{string_value}`

Retrieve a specific string by its value.

#### Response (200 OK)

```json
{
  "id": "abc123...",
  "value": "hello",
  "properties": {
    "length": 5,
    "is_palindrome": false,
    "unique_characters": 4,
    "word_count": 1,
    "sha256_hash": "abc123...",
    "character_frequency_map": {
      "h": 1,
      "e": 1,
      "l": 2,
      "o": 1
    }
  },
  "created_at": "2025-10-22T10:00:00.000Z"
}
```

### 5. Delete String

**DELETE** `/{string_value}`

Delete a string from the database.

#### Response (204 No Content)

No response body.

## 🗄️ Database Schema

### String Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | string (PK) | SHA256 hash of the string value |
| `value` | string | The actual string (indexed) |
| `length` | integer | Total character count |
| `is_palindrome` | boolean | Whether string is a palindrome |
| `unique_characters` | integer | Count of unique characters |
| `word_count` | integer | Number of words |
| `sha256_hash` | string | SHA256 hash of the value |
| `character_frequency_map` | JSONB | Character occurrence mapping |
| `created_at` | timestamp | UTC creation timestamp |

## 🗣️ Natural Language Queries

### Supported Patterns

#### Palindrome Detection
- "palindromic strings"
- "palindrome"

#### Length Filters
- "longer than 10" → min_length = 11
- "shorter than 5" → max_length = 4
- "at least 8" → min_length = 8
- "at most 15" → max_length = 15
- "exactly 12 characters" → min_length = 12, max_length = 12

#### Word Count
- "single word" → word_count = 1
- "two words" → word_count = 2
- "exactly 3 words" → word_count = 3

#### Character Search
- "containing the letter a"
- "contains x"
- "first vowel" → contains_character = 'a'

### Example Queries

```
1. "palindromic strings longer than 5 characters"
2. "single word strings containing the letter e"
3. "strings exactly 10 characters long"
4. "two words shorter than 20 characters"
5. "palindrome strings at least 3 characters"
```

## 🌐 Deployment

This project is deployed on **Railway** with PostgreSQL database.

### Deployment Steps

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Initialize project: `railway init`
4. Add PostgreSQL: `railway add postgresql`
5. Deploy: `railway up`

## ⚠️ Error Handling

The API implements comprehensive error handling:

### HTTP Status Codes

- `200 OK`: Successful GET request
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid natural language query
- `404 Not Found`: String not found in database
- `409 Conflict`: String already exists
- `422 Unprocessable Entity`: Conflicting query filters
- `500 Internal Server Error`: Database or server error

### Error Response Format

```json
{
  "detail": "String already exists in the system"
}
```

## 🧪 Testing

### Manual Testing with cURL

1. **Add a string**:
```bash
curl -X POST "https://hng-1-production-9be2.up.railway.app/" \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'
```

2. **Get all strings**:
```bash
curl "https://hng-1-production-9be2.up.railway.app/"
```

3. **Filter strings**:
```bash
curl "https://hng-1-production-9be2.up.railway.app/?is_palindrome=true&min_length=5"
```

4. **Natural language query**:
```bash
curl "https://hng-1-production-9be2.up.railway.app/filter-by-natural-language?query=palindromic%20strings"
```

5. **Get single string**:
```bash
curl "https://hng-1-production-9be2.up.railway.app/racecar"
```

6. **Delete string**:
```bash
curl -X DELETE "https://hng-1-production-9be2.up.railway.app/racecar"
```

### Using Swagger UI

Visit [https://hng-1-production-9be2.up.railway.app/docs](https://hng-1-production-9be2.up.railway.app/docs) for interactive testing.




**Note**: This project was created as part of the HNG Internship Stage 1 Backend task.
