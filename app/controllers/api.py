import json
from bson import SON
from bson.objectid import ObjectId
from app import app, db
from flask import jsonify, request, Response
import hashlib
from datetime import datetime

@app.route('/api/sketches', methods=['POST'])
def add_sketch():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    code = request.form.get('code', None)

    if not code:
        return 'You forgot to paste your sketch!', 400

    hashUrl = hashlib.sha1((code + name + email).encode("UTF-8")).hexdigest();

    db.sketches.insert({
        'url': hashUrl[:10],
        'name': name,
        'email': email,
        'code': code,
        'ip': request.remote_addr,
        'date': datetime.now(),
        'status':"waiting"
    })

    return hashUrl[:10]

@app.route('/api/sketches/<url_str>', methods=['GET'])
def get_sketch_by_url(url_str):
    sketch = db.sketches.find_one({
        'url': url_str
    })
    if (sketch is not None):
        data = {'url': sketch['url'],
                'filename': sketch['filename'],
                'description': sketch['description'],
                'code': sketch['code']
        }
    else:
        data = {}

    return jsonify(**data)


from bson import json_util
@app.route('/api/dashboard', methods=['GET'],)
def get_dashboard():
    sketch = db.sketches.find({}).sort('date')

    data = [{"status":i["status"], "name":i["name"]} for i in sketch]
    return Response(json.dumps(data, default=json_util.default), mimetype='application/json')
