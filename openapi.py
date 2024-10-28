"""Generate openapi doc."""

from fastapi.openapi.utils import get_openapi
from fdk_atlas_dcat_service.app import app
import yaml

spec = get_openapi(
    title=app.title,
    version=app.version,
    openapi_version=app.openapi_version,
    description=app.description,
    routes=app.routes,
)

with open("openapi.yml", "w") as f:
    f.write(yaml.dump(spec))
