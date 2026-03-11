"""
Simple test server to mock the external Dog API Service.
Run this in one terminal, and run the main app in another.
"""
from fastapi import FastAPI, status
from typing import Dict, Any
import json

app = FastAPI(title="Mock Dog API Service", version="1.0.0")

# Mock data
MOCK_BREEDS = {
    "data": [
        {
            "id": "f9643a80-af1d-422a-9f15-18d466822053",
            "type": "breed",
            "attributes": {
                "name": "Caucasian Shepherd Dog",
                "description": "The Caucasian Shepherd dog is a serious guardian breed and should never be taken lightly.",
                "hypoallergenic": False,
                "life": {"min": 15, "max": 20},
                "male_weight": {"min": 50, "max": 100},
                "female_weight": {"min": 50, "max": 100}
            }
        },
        {
            "id": "dc5e84f8-9151-4624-836c-25b4e313118b",
            "type": "breed",
            "attributes": {
                "name": "Bouvier des Flandres",
                "description": "They don't build 'em like this anymore.",
                "hypoallergenic": False,
                "life": {"min": 10, "max": 14},
                "male_weight": {"min": 30, "max": 40},
                "female_weight": {"min": 25, "max": 35}
            }
        }
    ],
    "meta": {"pagination": {"current": 1, "records": 2}},
    "links": {
        "self": "https://dogapi.dog/api/v2/breeds",
        "current": "https://dogapi.dog/api/v2/breeds?page[number]=1"
    }
}

MOCK_BREED_DETAIL = {
    "data": {
        "id": "f9643a80-af1d-422a-9f15-18d466822053",
        "type": "breed",
        "attributes": {
            "name": "Caucasian Shepherd Dog",
            "life": {"min": 15, "max": 20},
            "male_weight": {"min": 50, "max": 100},
            "female_weight": {"min": 50, "max": 100},
            "description": "The Caucasian Shepherd dog is a serious guardian breed and should never be taken lightly.",
            "hypoallergenic": False
        }
    },
    "links": {
        "self": "https://dogapi.dog/api/v2/breeds/f9643a80-af1d-422a-9f15-18d466822053"
    }
}

MOCK_FACTS = {
    "data": [
        {
            "id": "1cd1a16d-6fe1-40ea-9dd2-c21dd0f7c24e",
            "type": "fact",
            "attributes": {
                "body": "Many foot disorders in dogs are caused by long toenails."
            }
        }
    ]
}

MOCK_GROUPS = {
    "data": [
        {
            "id": "02124eb6-1baa-410c-90ea-6b8629fb0837",
            "type": "group",
            "attributes": {"name": "Foundation Stock Service"},
            "relationships": {
                "breeds": {
                    "data": [
                        {"id": "b0b6810c-fb88-4987-ad0a-ae0440b04634", "type": "breed"},
                        {"id": "38e06144-2ac3-43c0-981c-f8598eabc902", "type": "breed"}
                    ]
                }
            }
        }
    ],
    "links": {
        "self": "https://dogapi.dog/api/v2/groups",
        "current": "https://dogapi.dog/api/v2/groups?page[number]=1"
    }
}

MOCK_GROUP_DETAIL = {
    "data": {
        "id": "02124eb6-1baa-410c-90ea-6b8629fb0837",
        "type": "group",
        "attributes": {"name": "Foundation Stock Service"},
        "relationships": {
            "breeds": {
                "data": [
                    {"id": "b0b6810c-fb88-4987-ad0a-ae0440b04634", "type": "breed"},
                    {"id": "4bc90a09-5406-4739-96c6-ac2161fbfa4e", "type": "breed"}
                ]
            }
        }
    },
    "links": {
        "self": "https://dogapi.dog/api/v2/groups/02124eb6-1baa-410c-90ea-6b8629fb0837"
    }
}


@app.get("/breeds")
async def list_breeds():
    """Mock endpoint for listing breeds."""
    return MOCK_BREEDS


@app.get("/breeds/{breed_id}")
async def get_breed(breed_id: str):
    """Mock endpoint for getting a specific breed."""
    return MOCK_BREED_DETAIL


@app.get("/facts")
async def list_facts(limit: int = 1):
    """Mock endpoint for listing facts."""
    return MOCK_FACTS


@app.get("/groups")
async def list_groups():
    """Mock endpoint for listing groups."""
    return MOCK_GROUPS


@app.get("/groups/{group_id}")
async def get_group(group_id: str):
    """Mock endpoint for getting a specific group."""
    return MOCK_GROUP_DETAIL


@app.post("/pets", status_code=status.HTTP_201_CREATED)
async def create_pet(payload: dict):
    """Mock endpoint that always succeeds."""
    print(f"Mock service received: {payload}")
    return {"id": 1, "message": "Pet created successfully"}


if __name__ == "__main__":
    import uvicorn
    print("Starting mock Dog API Service on http://localhost:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
