<?php

namespace Pkg;

use BotFaas\QQGuild\OpenAPI as QQOpenAPI;

class OpenAPI
{

    public static function OpenAPI(): QQOpenAPI
    {
        return new QQOpenAPI(getenv("APP_ID"), getenv("APP_TOKEN"), getenv("SANDBOX_BOT") === "true");
    }

    public static function UploadPic($image)
    {
        $curl = curl_init();
        curl_setopt_array($curl, array(
            CURLOPT_URL => getenv('HOME_URL') . '/api/v1/open/guild/pic',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_ENCODING => '',
            CURLOPT_MAXREDIRS => 10,
            CURLOPT_TIMEOUT => 0,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
            CURLOPT_CUSTOMREQUEST => 'POST',
            CURLOPT_POSTFIELDS => array('pic' => $image),
            CURLOPT_HTTPHEADER => array(
                'X-AppId: ' . getenv("APP_ID"),
                'X-Sandbox: ' . (getenv("SANDBOX_BOT") === "true" ? '1' : ''),
                'X-AppToken: ' . getenv("APP_TOKEN")
            ),
        ));

        $response = curl_exec($curl);

        curl_close($curl);

        return json_decode($response, true);
    }

}
