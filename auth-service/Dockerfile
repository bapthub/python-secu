FROM python:3.10.7-bullseye
RUN pip install --upgrade pip
RUN apt update

RUN useradd -ms /bin/bash flask
USER flask
WORKDIR /app

COPY auth-service/ /app
RUN pip install -r ./requirements.txt

# EXPOSE 5000
# EXPOSE 27017

ENV FLASK_APP=src.server
# ENV FLASK_ENV=development
ENV FLASK_DEBUG=true

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
