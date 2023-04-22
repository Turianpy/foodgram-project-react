FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /app/api_foodgram

ENV PYTHONPATH .

CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000", "--workers", "3" "--reload"]

EXPOSE 8000