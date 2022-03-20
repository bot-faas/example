'use strict'
const {OpenAPI} = require("../pkg/openapi");

/**
 * const bot = require('qq-guild-bot');
 * @var {*} api bot.OpenAPI
 */
const api = OpenAPI();

/**
 *
 * @param {*} msg bot.Message
 * @returns
 */
module.exports = async (msg) => {
    return await api.messageApi.postMessage(msg.channel_id, {
        content: `<@!` + msg.author.id + `>ok`,
        msg_id: msg.id,
    });
}
