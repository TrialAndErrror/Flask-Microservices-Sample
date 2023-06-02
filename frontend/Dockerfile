FROM python:3.11

WORKDIR /app


#ENV VIRTUAL_ENV=/opt/venv
#RUN python3 -m venv $VIRTUAL_ENV
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir ./frontend
COPY . ./frontend

RUN pip install gunicorn

EXPOSE 8000

# FIXME: Remove this if this isn't needed anymore
CMD ["gunicorn", "--bind", ":8000", "frontend.wsgi:app"]