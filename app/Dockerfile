FROM python:3.12-alpine3.21

WORKDIR /usr/src/app

COPY ../requirements/requirements.txt requirements.txt 
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--forwarded-allow-ips", "*"]