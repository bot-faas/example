"use strict";
const { MongoDB } = require("../pkg/db/mongo");
const { OpenAPI } = require("../pkg/openapi");

/**
 * const mongodb = require("mongodb");
 * @var {*} mongo mongodb.Db
 */
let mongo;
MongoDB().then((db) => {
  mongo = db;
});

/**
 * const bot = require('qq-guild-bot');
 * @var {*} api bot.OpenAPI
 */
let api = OpenAPI();

/**
 *
 * @param {*} msg bot.Message
 * @returns
 */
module.exports = async (msg) => {
  let data = await mongo.collection("count").findOne({ uid: msg.author.id });
  if (!data) {
    mongo.collection("count").insertOne({ uid: msg.author.id, count: 1 });
    data.count = 1;
  } else {
    mongo
      .collection("count")
      .updateOne({ uid: msg.author.id }, { $inc: { count: 1 } });
    data.count += 1;
  }
  await api.messageApi.postMessage(msg.channel_id, {
    content: `<@!` + msg.author.id + `>这是第` + data.count + "条消息",
    msg_id: msg.id,
  });
};
