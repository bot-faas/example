<?php

namespace App;

use BotFaas\QQGuild\DTO\Message;
use BotFaas\QQGuild\DTO\MessageToCreate;
use BotFaas\QQGuild\OpenAPI as QQOpenAPI;
use MongoDB\Database;
use Pkg\Db\Mongo;
use Pkg\OpenAPI;

/**
 * Class Handler
 * @package App
 */
class Handler
{

    public QQOpenAPI $openapi;
    public Database $mongodb;

    public function __construct()
    {
        $this->openapi = OpenAPI::OpenAPI();
        $this->mongodb = Mongo::MongoDB();
    }

    public function handle(Message $msg)
    {
        $col = $this->mongodb->count;
        $row = $col->findOne(['uid' => $msg->author->id]);
        if ($row) {
            $col->updateOne(['uid' => $msg->author->id], ['$inc' => ['count' => 1]]);
            $row['count']++;
        } else {
            $col->insertOne(['uid' => $msg->author->id, 'count' => 1]);
            $row['count'] = 1;
        }
        return $this->openapi->MessageAPI()->PostMessage($msg->channel_id, new MessageToCreate([
            'content' => "<@!{$msg->author->id}>这是第{$row['count']}条消息",
            'msg_id' => $msg->id,
        ]));
    }
}
