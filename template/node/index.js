const express = require('express');
const app = express();
const handler = require('./function/handler');

app.post('/handle', express.json(), function (req, res) {
    let data = JSON.parse(req.body.data);
    handler(data);
    res.end();
})

app.listen(8080, () => {
    console.log(`node16 listening on port: 8080`)
});
