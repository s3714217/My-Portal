from flask import *
from flask_restful import Api
from resources.db import Database
from resources.todo import Todo
from datetime import datetime
app = Flask(__name__)
api = Api(app)

api.add_resource(Todo, "/todo/<string:text>/")

@app.route("/")
def index():
  title = "My App"
  return render_template("index.html",title=title)

@app.route("/guestbook")
def guestbook():
  message = Database().get_guestbook_message()
  if len(message) < 1:
    return render_template("guestbook.html", empty=True)
  else:
    return render_template("guestbook.html", empty=False, message=message)

@app.route("/guestbook", methods=['POST'])
def parse_request():
    new_message = []
    new_message.append(datetime.now())
    if request.method == 'POST':
      if request.form['name'] == '':
        new_message.append("Unknow user")
      else:
        new_message.append(request.form['name']) 
      new_message.append(request.form['message'])
    Database().new_guestbook_message(new_message)
    return render_template("guestbook.html", empty=False,message=Database().get_guestbook_message())


if __name__ == "__main__":
  app.run(debug=True)