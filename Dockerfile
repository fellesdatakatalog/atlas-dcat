FROM python:3.10

RUN pip install --upgrade "pip==24.2"
RUN pip install --no-cache-dir "poetry==1.8.3"

RUN mkdir -p /app
WORKDIR /app

COPY poetry.lock pyproject.toml README.md ./

COPY fdk_atlas_dcat_service/ ./fdk_atlas_dcat_service/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8080

CMD [ "uvicorn", "fdk_atlas_dcat_service.app:app", "--host", "0.0.0.0", "--port", "8080", "--no-use-colors", "--log-level", "warning" ] 
