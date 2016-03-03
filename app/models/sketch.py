import datetime
from bson import SON
from bson.objectid import ObjectId
from app import db
from mongokit import Document
#
# @db.register
# class Sketch(Document):
#
#     __collection__ = 'sketches'
#     __database__ = 'devday'
#
#     structure = {
#         'url': unicode,
#         'email': unicode,
#         'name': unicode,
#         'code': unicode,
#         'date': long,
#         '_id': ObjectId
#     }
#
#     required_fields = ['url','name','code']
#     default_values = {
#         'url': u''
#         'name': u''
#         'email': u''
#         'code': u''
#         'date': 1L
#     }
#     use_dot_notation = True
