<?php

namespace App;

use BotFaas\QQGuild\DTO\Message;
use BotFaas\QQGuild\DTO\MessageToCreate;
use BotFaas\QQGuild\OpenAPI as QQOpenAPI;
use Pkg\OpenAPI;

/**
 * Class Handler
 * @package App
 */
class Handler
{

    public QQOpenAPI $openapi;

    public function __construct()
    {
        $this->openapi = OpenAPI::OpenAPI();
    }

    public function handle(Message $msg)
    {
        return $this->openapi->MessageAPI()->PostMessage($msg->channel_id, new MessageToCreate([
            'content' => "<@!{$msg->author->id}>ok",
            'msg_id' => $msg->id,
        ]));
    }
}
