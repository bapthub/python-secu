all:
	docker compose up -d --build

restart:
	docker compose down
	docker compose up -d --build

run:
	docker build -t cryptomail-app .
	docker run -d -p 5000:5000 -p 27017:27017 --name cryptomail-app cryptomail-app

kill:
	docker stop cryptomail-app
	docker rm cryptomail-app

down:
	docker compose down
