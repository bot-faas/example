"use strict";

import { IMessage } from "qq-guild-bot";
import { OpenAPI } from "../pkg/openapi";

// ts还没支持,先写在这里了

/**
 * const bot = require('qq-guild-bot');
 * @var {*} api bot.OpenAPI
 */
let api = OpenAPI();

export function handle(msg: IMessage) {
  api.messageApi.postMessage(msg.channel_id, {
    content: `<@!` + msg.author.id + `>ok`,
    msg_id: msg.id,
  });
}
