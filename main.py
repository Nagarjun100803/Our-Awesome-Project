from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from src.api.exception_registry import exception_registry
from src.api.routes.authentication import auth_router
from src.api.routes.profile_completion import profile_completion_router
from src.dependencies import db
from src.exceptions import DomainException


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_pool()
    yield
    await db.close_pool()


app = FastAPI(
    title="Scholarship Project API",
    version="1.0.0",
    description="API for the Scholarship Project - VRNeXGen Technologies",
    lifespan=lifespan,
)

api_prefix = "/api"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="some-secret-key")

app.include_router(router=auth_router, prefix=api_prefix)
app.include_router(router=profile_completion_router, prefix=api_prefix)


@app.get(f"{api_prefix}/")
async def root():
    return {"message": "Hello, World!"}


@app.exception_handler(DomainException)
def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR  # default status code = 500

    for exception_type, status in exception_registry.items():
        if isinstance(exc, exception_type):
            status_code = status
            break

    return JSONResponse(
        status_code=status_code,
        content={
            "sucess": False,
            "error": {"message": exc.message, "type": exc.__class__.__name__},
        },
    )
