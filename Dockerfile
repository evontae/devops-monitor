FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/ .

CMD [ "python", "-u", "main.py" ]