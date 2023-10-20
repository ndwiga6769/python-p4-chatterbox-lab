from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods = ['GET','POST'])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by(Message.created_at.asc()).all()

        messages_serialized = [message.to_dict() for message in messages]
        response = make_response(jsonify(messages_serialized),200)

        return response
    elif request.method == "POST":
        message  = request.get_json()
        new_message = Message(
            body=message.get('body'),
            username=message.get('username')
            )
        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(message_dict,201)
        # response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/messages/<int:id>',methods = ['PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == "PATCH":
        message1  = request.get_json()
        for attr in message1:
            setattr(message,attr,message1[attr])
        db.session.add(message)
        db.session.commit()
        bakery_serialized = message.to_dict()

        response = make_response(
            bakery_serialized,
            200
        )
        return response

    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Review deleted."    
        }
        response = make_response(
            jsonify(response_body),
            200
        )

    return response


if __name__ == '__main__':
    app.run(port=5555)