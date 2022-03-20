<?php

namespace Pkg\Db;


use MongoDB\Client;
use MongoDB\Database;

class Mongo
{
    public static function MongoDB(): Database
    {
        $db = new Client(getenv('BOT_FAAS_MONGODB_URI'));
        return $db->selectDatabase(getenv('BOT_FAAS_MONGODB_DBNAME'));
    }

}
