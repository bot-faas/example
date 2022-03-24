FROM composer:2 AS composer

FROM php:7.4-alpine

COPY --from=composer /usr/bin/composer /usr/bin/composer

COPY . .

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.cloud.tencent.com/g' /etc/apk/repositories && \
    apk add git gcc g++ make automake openssl-dev autoconf && \
    chmod +x php-extension.sh && \
    sh ./php-extension.sh


CMD ["php","-S","0.0.0.0:8080","index.php"]
