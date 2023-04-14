FROM python:3.9-slim


WORKDIR ./app
COPY config.ini config.ini
COPY app.py app.py
COPY requirements.txt requirements.txt

RUN pip install pip update
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "./app.py"]