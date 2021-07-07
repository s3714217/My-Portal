from flask_restful import Resource


class Todo(Resource):
  def get(self, text):
    return text, 200
    #return "Item not found for the id: {}".format(id), 404
