# src/services/location_lookup.py
import httpx
from fastapi import HTTPException, status

from src.api.schemas.profile_completion import PincodeLookupResponse

POSTAL_API_BASE = "https://api.postalpincode.in/pincode"


class LocationLookupService:
    async def lookup_pincode(self, pincode: str) -> PincodeLookupResponse:
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{POSTAL_API_BASE}/{pincode}")
                response.raise_for_status()
            except httpx.HTTPError:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Unable to reach pincode lookup service",
                )

        data = response.json()

        if not data or data[0].get("Status") != "Success":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pincode not found",
            )

        post_offices = data[0]["PostOffice"]

        return PincodeLookupResponse(
            pincode=pincode,
            state=post_offices[0]["State"],
            district=post_offices[0]["District"],
            city=[po["Name"] for po in post_offices],
        )
