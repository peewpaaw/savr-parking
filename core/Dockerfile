FROM python:3.11.3-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/

# CMD ["fastapi", "run", "main.py", "--port", "80"]
