FROM python:3.10-slim


WORKDIR ./app
COPY config.ini config.ini
COPY app.py app.py
COPY requirements.txt requirements.txt

RUN pip install pip update
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]