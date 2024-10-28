"""Package for exposing validation endpoint and starting rabbit consumer."""

from contextlib import asynccontextmanager
import logging
import traceback
import os
import requests
import json

from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient, AtlasEntity, AtlasProcess, TypeCategory
from pyapacheatlas.core.typedef import *

from datacatalogtordf import Catalog, Dataset

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

def azuread_auth(tenant_id: str, client_id: str, client_secret: str, resource_url: str):
    """
    Authenticates Service Principal to the provided Resource URL, and returns the OAuth Access Token
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    payload= f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&resource={resource_url}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    access_token = json.loads(response.text)['access_token']
    return access_token
def purview_auth(tenant_id: str, client_id: str, client_secret: str, data_catalog_name: str):
    """
    Authenticates to Atlas Endpoint and returns a client object
    """
    oauth = ServicePrincipalAuthentication(
        tenant_id = tenant_id,
        client_id = client_id,
        client_secret = client_secret
    )
    client = PurviewClient(
        account_name = data_catalog_name,
        authentication = oauth
    )
    return client

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

@app.get("/catalog")
def get_catalog() -> str:
    """Get RDF catalog"""
   
    tenantID = os.getenv("TENANT_ID")
    clientID = os.getenv("CLIENT_ID")
    clientSecret = os.getenv("SECRET")
    resource_url = "https://purview.azure.net"
    datacatalog_name = 'livdevpurview'
    endpoint= "https://livdevpurview.purview.azure.com"
    token = azuread_auth(tenantID, clientID, clientSecret, resource_url)

    endpoint = ""
    atlas_endpoint_typedefs = endpoint + "/catalog/api/atlas/v2/types/typedefs"
    atlas_endpoint_query = endpoint + "/datamap/api/search/query?api-version=2023-09-01"
    atlas_endpoint_entity = endpoint + "/datamap/api/atlas/v2/entity/guid/" + "9169359d-41d8-4854-ae1b-64ec05278266"
    atlas_header = {
            "Authorization": "Bearer "+token,
            "Content-Type": "application/json"
        }

    payload = {
        "keywords": None,
        "limit": 1
    }
    url = atlas_endpoint_entity
    #print(atlas_endpoint)
    response = requests.get(url= url, headers= atlas_header)

    response_json = response.json()
    entity = response_json['entity']
    business_attributes = entity['businessAttributes']
    attr_dcat = business_attributes['dcat_hackathon']


    # Create catalog object
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    catalog.title = {"en": "Helseetaten Katalog"}
    catalog.publisher = "https://example.com/publishers/1"

    # Create a dataset:
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    dataset.title = {"nb": attr_dcat['title'], "en": "incomeAPI"}
    dataset.license = attr_dcat['license'][0]
    dataset.access_rights   =  attr_dcat['accessRights']
    dataset.frequency   = attr_dcat['d_frequency']
    dataset.theme       = {'nb': attr_dcat['d_theme']}

    #
    # Add dataset to catalog:
    catalog.datasets.append(dataset)

    # get rdf representation in turtle (default)
    rdf = catalog.to_rdf(format="turtle")
    return rdf.decode()