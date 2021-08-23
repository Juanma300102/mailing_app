# syntax=docker/dockerfile:1

FROM python:3.8
WORKDIR /app

COPY requeriments.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

