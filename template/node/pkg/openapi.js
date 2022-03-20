const bot = require('qq-guild-bot');
const request = require('request');
const fs = require('fs');

exports.OpenAPI = function () {
    return bot.createOpenAPI({
        appID: process.env.APP_ID,
        token: process.env.APP_TOKEN,
        sandbox: process.env.SANDBOX_BOT === "true",
    });
}

exports.UploadPic = function (name, file) {
    return new Promise(resolve => {
        const options = {
            'method': 'POST',
            'url': process.env.HOME_URL + '/api/v1/open/guild/pic',
            'headers': {
                'X-AppId': process.env.APP_ID,
                'X-Sandbox': process.env.SANDBOX_BOT === "true" ? '1' : '',
                'X-AppToken': process.env.APP_TOKEN,
            },
            formData: {
                'pic': {
                    'value': file,
                    'options': {
                        'filename': name,
                        'contentType': "image/png"
                    }
                }
            }
        };
        request(options, function (error, response) {
            if (error) throw new Error(error);
            resolve(JSON.parse(response.body));
        });
    });
}