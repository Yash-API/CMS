FROM python:3.10

WORKDIR /app

COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./app/requirements.txt /app/requirements.txt
COPY alembic.ini /app/

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
