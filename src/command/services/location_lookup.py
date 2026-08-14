import httpx

from src.api.schemas.profile_completion import PincodeLookupResponse
from src.exceptions import ExternalServiceException, PincodeNotFoundError
from src.settings import PincodeSettings


class LocationLookupService:
    async def lookup_pincode(self, pincode: str) -> PincodeLookupResponse:
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{PincodeSettings.api_url}/{pincode}")
                response.raise_for_status()
            except httpx.HTTPError:
                raise ExternalServiceException(
                    message="Unable to reach pincode lookup service"
                )

        data = response.json()

        if not data or data[0].get("Status") != "Success":
            raise PincodeNotFoundError(message=f"Pincode not found: {pincode}")

        post_offices = data[0]["PostOffice"]

        return PincodeLookupResponse(
            pincode=pincode,
            state=post_offices[0]["State"],
            district=post_offices[0]["District"],
            city=[po["Name"] for po in post_offices],
        )
