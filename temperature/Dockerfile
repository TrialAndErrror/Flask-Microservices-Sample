FROM python:3.11

WORKDIR /app

# TODO: SEe if we can cut datetime out of docker
RUN echo "America/New_York" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir ./temperature
COPY . ./temperature

RUN pip install gunicorn

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--reload", "temperature.wsgi:app"]