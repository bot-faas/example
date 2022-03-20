const mongodb = require("mongodb");

exports.MongoDB = function () {
  return new Promise((resolve, reject) => {
    mongodb.MongoClient.connect(process.env.BOT_FAAS_MONGODB_URI, (err, db) => {
      if (err) {
        return reject(err);
      }
      resolve(db.db(process.env.BOT_FAAS_MONGODB_DBNAME));
    });
  });
};
