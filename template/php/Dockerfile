FROM codfrm/bot-faas-php:v0.1

WORKDIR /bot-faas

COPY . .

RUN composer config -g repos.packagist composer https://mirrors.cloud.tencent.com/composer/ && \
    composer install --ignore-platform-reqs

RUN cd function && \
    composer config -g repos.packagist composer https://mirrors.cloud.tencent.com/composer/ && \
    composer install --ignore-platform-reqs

CMD ["php","-S","0.0.0.0:8080","index.php"]
