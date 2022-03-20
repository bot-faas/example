FROM node:16-alpine

WORKDIR /bot-faas

COPY . .

RUN npm i && \
	cd function && \
	npm i

CMD ["node","index.js"]
