# Dog API Service - Swagger Testing Guide

This is a complete API service generated from the Dog API OpenAPI specification with integrated Swagger UI for interactive testing.

## 🚀 Quick Start

### Option 1: Run with Both Servers (Full Features)

```bash
python quickstart.py
```

This will:
1. Start a mock Dog API service on `http://localhost:8001`
2. Start the main API service on `http://localhost:8000`
3. Display the Swagger UI URL in the console

**Output:**
```
======================================================================
Dog API Service - Quick Start with Swagger Testing
======================================================================

🚀 Services are running!

📋 API Documentation (Swagger UI):
   http://localhost:8000/docs

📖 Alternative API Documentation (ReDoc):
   http://localhost:8000/redoc

🔧 Mock Dog API Service (for testing):
   http://localhost:8001

💡 Available endpoints to test:
   • GET  /breeds - List all dog breeds
   • GET  /breeds/{id} - Get specific breed by ID
   • GET  /facts - Get random dog facts
   • GET  /groups - List dog breed groups
   • GET  /groups/{id} - Get specific group by ID
   • POST /pets - Create a pet (legacy endpoint)

Press Ctrl+C to stop all services
```

### Option 2: Test with Mocked Services Only

```bash
python -m pytest test_endpoints.py -v
```

This runs automated tests without requiring the servers to be running.

---

## 📋 Testing in Swagger UI

1. **Open Swagger UI:**
   - Navigate to: `http://localhost:8000/docs`

2. **Test an Endpoint:**
   - Click on any endpoint (e.g., `POST /pets`)
   - Click the **"Try it out"** button
   - Fill in the required parameters
   - Click **"Execute"**
   - View the response

### Example Tests

#### 1. Create a Pet (POST /pets)
```json
{
  "content": "Fluffy the cat"
}
```

#### 2. List All Dog Breeds (GET /breeds)
No parameters required - just click Execute

#### 3. Get Random Facts (GET /facts)
No parameters required - just click Execute

---

## 🌐 Available Endpoints

### Pets
- **POST** `/pets` - Create a new pet
  - Request body: `{"content": "pet name"}`
  - Response: 201 Created

### Breeds
- **GET** `/breeds` - List all dog breeds
  - Response: Array of breed objects

- **GET** `/breeds/{id}` - Get a specific breed
  - Path parameter: `id` (breed ID)
  - Response: Single breed object

### Facts
- **GET** `/facts` - Get random dog facts
  - Query parameter: `limit` (optional, 1-5)
  - Response: Array of fact objects

---

## 📁 Project Structure

```
generated/
├── main.py                 # FastAPI app entry point
├── quickstart.py          # Startup script with Swagger UI guide
├── mock_service.py        # Mock API that mimics the Dog API
├── test_endpoints.py      # Unit tests for endpoints
├── config.py              # Configuration settings
├── dependencies.py        # Dependency injection setup
├── middleware.py          # Logging middleware
│
├── routers/               # API route handlers
│   └── pet_router.py
│
├── clients/               # HTTP clients for calling services
│   └── pet_client.py
│
├── models/                # Pydantic data models
│   └── pet.py
│
├── services/              # Business logic
│   └── group_service.py
│
└── app/                   # Alternative app structure (breeds & facts)
    ├── main.py
    ├── api/
    │   ├── breeds.py
    │   └── fact_router.py
    ├── clients/
    ├── models/
    ├── services/
    └── dependencies.py
```

---

## 🛠️ Environment Setup

The `.env` file is automatically created with:
```
PET_SERVICE_BASE_URL=http://localhost:8001
DOGAPI_BASE_URL=http://localhost:8001
```

---

## ✅ All Tests

Run all tests:
```bash
python -m pytest test_endpoints.py -v
```

Test results:
- ✅ test_create_pet_success
- ✅ test_create_pet_empty_content
- ✅ test_create_pet_missing_content
- ✅ test_create_pet_whitespace_only
- ✅ test_openapi_docs
- ✅ test_redoc_docs

---

## 🔗 Documentation URLs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 💡 Tips

1. **Use Swagger UI for interactive testing** - It's much easier than curl!
2. **The mock service returns realistic data** - Perfect for development
3. **All requests are logged** - Check the console for request details
4. **Auto-reload enabled** - Modify code while the server is running

---

## 🎯 Next Steps

1. Run `python quickstart.py`
2. Open http://localhost:8000/docs in your browser
3. Start testing the endpoints interactively!

Enjoy testing your API! 🎉
