FROM python:3.11

WORKDIR /app

ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG POSTGRES_PORT

ENV POSTGRES_USER $POSTGRES_USER
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD
ENV POSTGRES_DB $POSTGRES_DB
ENV POSTGRES_PORT $POSTGRES_PORT

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir ./feeding_calc
COPY . ./feeding_calc

RUN pip install gunicorn

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "feeding_calc.wsgi:app"]