import httpx

from src.api.schemas.profile_completion import PincodeLookupResponse
from src.exceptions import ExternalServiceException, PincodeNotFoundError
from src.settings import settings


class LocationLookupService:
    async def lookup_pincode(self, pincode: str) -> PincodeLookupResponse:
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{settings.pincode.api_url}/{pincode}")
                _ = response.raise_for_status()
            except httpx.HTTPError:
                raise ExternalServiceException(
                    message="Unable to reach pincode lookup service"
                )

        data = response.json()  # pyright: ignore[reportAny]

        if not data or data[0].get("Status") != "Success":  # pyright: ignore[reportAny]
            raise PincodeNotFoundError(message=f"Pincode not found: {pincode}")

        post_offices = data[0]["PostOffice"]  # pyright: ignore[reportAny]

        return PincodeLookupResponse(
            pincode=pincode,
            state=post_offices[0]["State"],  # pyright: ignore[reportAny]
            district=post_offices[0]["District"],  # pyright: ignore[reportAny]
            city=[po["Name"] for po in post_offices],  # pyright: ignore[reportAny]
        )
