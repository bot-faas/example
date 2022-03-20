import json
from function import handler
from flask import request, Flask


app = Flask(__name__)


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict2obj(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    d = Dict()
    for k, v in dictObj.items():
        d[k] = dict2obj(v)
    return d


@app.route("/handle", methods=['POST'])
def handle():
    json_data = request.get_json()
    data = json.loads(json_data['data'])
    handler.handle(dict2obj(data))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
