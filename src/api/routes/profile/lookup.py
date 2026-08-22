from typing import Annotated

from fastapi import APIRouter
from pydantic import Field

from src.api.dependencies import (
    CollegeLookupServiceDependency,
    LocationLookupServiceDependency,
)
from src.api.schemas.profile_completion import PincodeLookupResponse
from src.command.commands.college_lookup import CollegeLookupGet

router = APIRouter(prefix="/lookup", tags=["Lookup"])


@router.get("/pincode/{pincode}", status_code=200, response_model=PincodeLookupResponse)
async def get_location_by_pincode(
    pincode: Annotated[str, Field(pattern=r"^\d{6}$")],
    location_service: LocationLookupServiceDependency,
):
    return await location_service.lookup_pincode(pincode)


@router.get("/college/{college_name}", status_code=200)
async def get_college_by_name(
    college_name: str,
    college_lookup_service: CollegeLookupServiceDependency,
):
    return {
        "colleges": await college_lookup_service.get(
            CollegeLookupGet(name=college_name)
        )
    }
