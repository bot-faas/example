<?php

namespace App;

use BotFaas\QQGuild\DTO\Message;
use BotFaas\QQGuild\DTO\MessageToCreate;
use BotFaas\QQGuild\OpenAPI as QQOpenAPI;
use Pkg\OpenAPI;

/**
 * Class Handler
 * 请将"bot.icodef.com/api/v1/open/guild/pic"加入qq机器人管理的消息URL配置
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
        $resp = OpenAPI::UploadPic(new \CURLFile("https://bbs.tampermonkey.net.cn/uc_server/avatar.php?uid=4&size=big&ts=1", "image/png", "test.png"));
        if ($resp['code']) {
            return $this->openapi->MessageAPI()->PostMessage($msg->channel_id, new MessageToCreate([
                'content' => "<@!{$msg->author->id}图片发送失败: " . $resp['msg']
            ]));
        }
        return $this->openapi->MessageAPI()->PostMessage($msg->channel_id, new MessageToCreate([
            'image' => $resp['data']['url'],
            'msg_id' => $msg->id,
        ]));
    }
}
