from fastapi import HTTPException, status
import httpx
from zeep import Client
from schemas.group import GroupResponse


class GroupService:
    def __init__(self):
        # SOAP client (kept)
        try:
            self.soap_client = Client("http://www.dneonline.com/calculator.asmx?WSDL")
        except Exception as e:
            raise RuntimeError(f"SOAP client init failed: {e}")

        self.base_url = "https://dogapi.dog/api/v2"

    async def fetch_group(self, group_id: str) -> GroupResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/groups")

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail="Failed to fetch from Dog API",
                    )

                data = response.json()

                for item in data.get("data", []):
                    if item.get("attributes", {}).get("name", "").lower() == group_id.lower():

                        # ✅ FIX: wrap into expected schema format
                        wrapped_response = {
                            "data": item,
                            "links": data.get("links", {"self": ""})
                        }

                        return GroupResponse.model_validate(wrapped_response)

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Group not found",
                )

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            )