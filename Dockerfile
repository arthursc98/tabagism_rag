FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /app

CMD ["fastapi", "run", "/app/app.py", "--port", "8000"]