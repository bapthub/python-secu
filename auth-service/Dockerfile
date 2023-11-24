FROM python:3.10.7-bullseye
RUN pip install --upgrade pip
RUN apt update

WORKDIR /app

<<<<<<< Updated upstream:Dockerfile
COPY ./src /app

=======
COPY auth-service/src /app
>>>>>>> Stashed changes:auth-service/Dockerfile
RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 27017

ENV FLASK_APP=front
ENV FLASK_ENV=production

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
