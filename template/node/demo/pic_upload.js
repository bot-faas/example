"use strict";
const {OpenAPI, UploadPic} = require("../pkg/openapi");
const request = require('request');

/**
 * const bot = require('qq-guild-bot');
 * @var {*} api bot.OpenAPI
 */
let api = OpenAPI();

/**
 * 请将"bot.icodef.com/api/v1/open/guild/pic"加入qq机器人管理的消息URL配置
 * @param {*} msg bot.Message
 * @returns
 */
module.exports = async (msg) => {
    const resp = await UploadPic("test.png", request('https://bbs.tampermonkey.net.cn/uc_server/avatar.php?uid=4&size=big&ts=1'));
    if (resp.code) {
        return await api.messageApi.postMessage(msg.channel_id, {
            content: `<@!` + msg.author.id + `>图片发送失败: ` + resp.msg,
            msg_id: msg.id,
        });
    }
    return await api.messageApi.postMessage(msg.channel_id, {
        image: resp.data.url,
        msg_id: msg.id,
    });
};
