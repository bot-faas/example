FROM node:16-alpine

WORKDIR /bot-faas

COPY . .

RUN chmod +x ./function/build_script && \
    ./function/build_script

RUN npm i && \
	cd function && \
	npm i

CMD ["node","index.js"]
