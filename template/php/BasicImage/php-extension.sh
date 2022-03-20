#!/bin/sh

echo "Installing PHP extensions"
docker-php-ext-install pdo_mysql

pecl install mongodb

echo "extension=mongodb.so" > $PHP_INI_DIR/conf.d/mongo.ini

