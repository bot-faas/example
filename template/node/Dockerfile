FROM node:16-alpine

WORKDIR /bot-faas

COPY . .

RUN npm i && \
	cd function && \
    npm config set registry http://mirrors.cloud.tencent.com/npm/ && \
	npm i

CMD ["node","index.js"]
