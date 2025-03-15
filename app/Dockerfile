FROM python:3.12-alpine3.21

WORKDIR /usr/src/app

COPY ../requirements/requirements.txt requirements.txt 
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "app/run.py" ]