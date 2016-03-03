from bson import SON
from bson.objectid import ObjectId
import os
import glob
from jinja2 import TemplateNotFound

from app import app, db
from flask import render_template, request

__all__ = [os.path.basename(f)[:-3]
           for f in glob.glob(os.path.dirname(__file__) + "/*.py")]

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/sketch/<url>', methods=['GET'])
def view_sketch(url):
    sketch = db.sketches.find_one({
        'url' : url
    })
    print sketch
    if sketch is not None and sketch.has_key('code'):
        data = {'url': sketch['url'],
            'name': sketch['name'],
            'email': sketch['email'],
            'code': sketch['code']}
        return render_template('index.html', url=data['url'], code=data['code'], name=data['name'], email=data['email'])
    return "Not Found",404

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')