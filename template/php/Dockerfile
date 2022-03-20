FROM codfrm/bot-faas-php:v0.1

WORKDIR /bot-faas

COPY . .

RUN rm composer.lock && \
    composer install --ignore-platform-reqs

CMD ["php","-S","0.0.0.0:8080","index.php"]
