"""Package for exposing validation endpoint and starting rabbit consumer."""

from contextlib import asynccontextmanager
import logging
import traceback

from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.security.api_key import APIKey

from fdk_rdf_parser.classes.exceptions import (
    MissingResourceError,
    MultipleResourcesError,
    ParserError,
)

from fdk_atlas_dcat_service.config import setup_logging

from fdk_atlas_dcat_service.model import resource_type_map
from fdk_atlas_dcat_service.service import ParsedReturnType, parse_resource


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logging.info("Starting app")
    yield


app = FastAPI(
    title="fdk-atlas-dcat-service",
    description="Services that receives RDF graphs and parses them to JSON.",
    lifespan=lifespan,
    version="0.1.0",
)

@app.get("/ping")
def get_ping() -> str:
    """Ping route function."""
    return "OK"


@app.get("/ready")
def get_ready() -> str:
    """Ready route function."""
    return "OK"
