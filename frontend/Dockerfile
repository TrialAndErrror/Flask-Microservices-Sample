FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir ./frontend
COPY . ./frontend

EXPOSE 8000

# FIXME: Remove this if this isn't needed anymore
CMD ["gunicorn", "--bind", ":8000", "frontend.wsgi:app"]