FROM python:3.10.4-slim-bullseye
RUN pip3 install flask flask-wtf email_validator requests flask-login flask-sqlalchemy .
COPY app app
CMD python ./app/app.py
